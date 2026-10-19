"""Clustering mechanics: nesting, symmetry, determinism, naming.

These test the properties the vault renderer will depend on, with synthetic vectors
whose right answer is known — no embedding provider, no network.
"""
import numpy as np
import pytest

from tools.ingest import cluster as cl


def three_blobs(per=6, dim=8, sep=10.0):
    """Three well-separated groups. Any sane clustering must recover them."""
    rng = np.random.RandomState(0)
    vecs, truth = [], []
    for g in range(3):
        center = np.zeros(dim)
        center[g] = sep
        for _ in range(per):
            vecs.append(center + rng.normal(0, 0.1, dim))
            truth.append(g)
    return np.array(vecs), truth


def test_cosine_sim_is_symmetric_with_unit_diagonal():
    vecs, _ = three_blobs()
    s = cl.cosine_sim(vecs)
    assert np.allclose(s, s.T)
    assert np.allclose(np.diag(s), 1.0)


def test_clustering_recovers_obvious_groups():
    vecs, truth = three_blobs()
    labels = cl.cut_levels(cl.dendrogram(vecs), len(vecs), (3,))[0]
    # same truth group => same label, different truth group => different label
    for i in range(len(truth)):
        for j in range(len(truth)):
            assert (labels[i] == labels[j]) == (truth[i] == truth[j])


def test_dendrogram_is_deterministic():
    """The pipeline rebuilds every artifact each run; clustering must not drift."""
    vecs, _ = three_blobs()
    a = cl.cut_levels(cl.dendrogram(vecs), len(vecs), (3, 6))
    b = cl.cut_levels(cl.dendrogram(vecs), len(vecs), (3, 6))
    assert [list(x) for x in a] == [list(y) for y in b]


def test_finer_cuts_strictly_refine_coarser_ones():
    """This is what makes 'clusters within clusters' real rather than hoped for."""
    vecs, _ = three_blobs(per=8)
    coarse, fine = cl.cut_levels(cl.dendrogram(vecs), len(vecs), (3, 8))
    for i in range(len(vecs)):
        for j in range(len(vecs)):
            if fine[i] == fine[j]:
                assert coarse[i] == coarse[j], "a fine cluster spans two coarse ones"


def test_paths_nest_and_share_prefixes():
    vecs, truth = three_blobs()
    levels = cl.cut_levels(cl.dendrogram(vecs), len(vecs), (3, 6))
    ps = cl.paths(levels)
    assert all(len(p.split(".")) == 2 for p in ps)
    for i in range(len(truth)):
        for j in range(len(truth)):
            same_top = ps[i].split(".")[0] == ps[j].split(".")[0]
            assert same_top == (truth[i] == truth[j])


def test_paths_are_stable_across_runs():
    vecs, _ = three_blobs()
    levels = cl.cut_levels(cl.dendrogram(vecs), len(vecs), (3, 6))
    assert cl.paths(levels) == cl.paths(levels)


def test_knn_is_symmetric_and_bounded():
    vecs, _ = three_blobs(per=6)
    doms = [f"s{i}.com" for i in range(len(vecs))]
    nb = cl.knn(cl.cosine_sim(vecs), doms, k=3)
    for d, lst in nb.items():
        for other, _ in lst:
            assert d in [o for o, _ in nb[other]], "edge must exist from both ends"
            assert other != d


def test_knn_prefers_same_blob():
    vecs, truth = three_blobs(per=6)
    doms = [f"s{i}.com" for i in range(len(vecs))]
    nb = cl.knn(cl.cosine_sim(vecs), doms, k=3)
    idx = {d: i for i, d in enumerate(doms)}
    for d, lst in nb.items():
        top = lst[:3]
        assert all(truth[idx[o]] == truth[idx[d]] for o, _ in top)


def test_knn_scores_sorted_descending():
    vecs, _ = three_blobs()
    doms = [f"s{i}.com" for i in range(len(vecs))]
    for lst in cl.knn(cl.cosine_sim(vecs), doms, k=4).values():
        assert [s for _, s in lst] == sorted((s for _, s in lst), reverse=True)


def test_name_clusters_picks_distinctive_not_common_terms():
    texts = [
        "marketplace selling templates storefront checkout",
        "marketplace selling icons storefront checkout",
        "marketplace selling fonts storefront checkout",
        "portfolio designer personal resume work",
        "portfolio developer personal resume work",
        "portfolio engineer personal resume work",
    ]
    names = cl.name_clusters(texts, [1, 1, 1, 2, 2, 2])
    assert "marketplace" in names[1] and "portfolio" in names[2]
    assert "marketplace" not in names[2] and "portfolio" not in names[1]


def test_tokenize_drops_stopwords_and_corpus_noise():
    toks = cl.tokenize("The tweet shows a hero section about the site's own meta description")
    assert "tweet" not in toks and "hero" not in toks and "the" not in toks


def test_name_clusters_never_returns_empty():
    names = cl.name_clusters(["the and or", "the and or"], [1, 2])
    assert all(v for v in names.values())


# --- text assembly: what actually gets embedded ---------------------------------

from tools.ingest import embed as em


def test_not_captured_placeholders_are_stripped():
    """Failed teardowns must not make sites look alike.

    Ten sites once formed a cluster named "extracted captured. screenshot" purely
    because their what_it_shows and how_it_works both read "Not captured".
    """
    e = {
        "what_it_is": "A falling-sand physics toy in the browser.",
        "what_it_shows": "Not captured — no screenshot or DOM probe this run (see extracted_via).",
        "how_it_works": "Not captured.",
    }
    text = em.space_text("sandspiel.club", e, "purpose")
    assert "falling-sand" in text
    assert "captured" not in text.lower()


def test_real_text_starting_with_not_is_kept():
    e = {"what_it_is": "Nothing but a single line of type.", "what_it_shows": "",
         "how_it_works": ""}
    assert "Nothing but a single line" in em.space_text("x.com", e, "purpose")


def test_space_text_purpose_and_design_draw_on_different_fields():
    e = {
        "what_it_is": "PURPOSEWORD", "what_it_shows": "", "how_it_works": "",
        "how_its_designed": "DESIGNWORD", "palette": "", "fonts": "",
        "fonts_loaded": [], "headings": [],
    }
    assert "PURPOSEWORD" in em.space_text("x.com", e, "purpose")
    assert "PURPOSEWORD" not in em.space_text("x.com", e, "design")
    assert "DESIGNWORD" in em.space_text("x.com", e, "design")
    assert "DESIGNWORD" not in em.space_text("x.com", e, "purpose")


def test_corpus_skips_sites_with_no_usable_text():
    doc = {"site_designs": {
        "_schema": {"note": "ignored"},
        "good.com": {"what_it_is": "A real description."},
        "empty.com": {"what_it_is": "Not captured.", "what_it_shows": "Not captured."},
    }}
    assert [d for d, _ in em.corpus(doc, "purpose")] == ["good.com"]


def test_pipeline_narration_is_scrubbed_sentence_by_sentence():
    """The noise usually sits inside good prose, so whole-field filtering misses it."""
    e = {"what_it_is": "Radio Garden is an interactive 3D globe of radio stations. "
                       "A WebFetch text-fetch succeeded (no browser needed). "
                       "You drag the globe to tune in.",
         "what_it_shows": "", "how_it_works": ""}
    text = em.space_text("radio.garden", e, "purpose")
    assert "interactive 3D globe" in text and "drag the globe" in text
    assert "webfetch" not in text.lower() and "browser needed" not in text.lower()


def test_scrub_keeps_prose_that_merely_mentions_a_browser():
    assert "browser-based falling-sand" in em._scrub(
        "A browser-based falling-sand simulator you play in the page.")


def test_cluster_names_drop_hostnames():
    texts = ["static.cloudflareinsights.com beacon marketplace templates",
             "static.cloudflareinsights.com beacon marketplace templates",
             "portfolio designer resume", "portfolio designer resume"]
    names = cl.name_clusters(texts, [1, 1, 2, 2])
    assert "cloudflareinsights" not in " ".join(names.values())
    assert "marketplace" in names[1]
