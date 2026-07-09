from .config import MD_REGION_START, MD_REGION_END


def render_item_block(it):
    title = it.get("title") or it.get("primary_domain") or it.get("author")
    url = it.get("primary_url")
    site = f"**Site:** [{it.get('primary_domain') or url}]({url})  \n" if url else ""
    prof = it.get("author_profile") or ""
    tweet = it.get("tweet") or ""
    tags = " ".join(f"`{t}`" for t in it.get("tags", []))
    text = (it.get("text") or "").strip().replace("\n", " ")
    if len(text) > 200:
        text = text[:200] + "…"
    return (
        f"### {title}\n\n"
        f"{site}"
        f"**Author:** [@{it.get('author')}]({prof})  \n"
        f"**Source:** [tweet]({tweet}) · {it.get('date')}  \n"
        f"**Tags:** {tags}  \n\n"
        + (f"> {text}\n" if text else "")
    )


def render_region_body(items):
    header = "## Auto-ingested (newest first)\n\n_Appended automatically from X bookmark exports. Move into curated sections by hand._\n\n"
    blocks = "\n".join(render_item_block(i) for i in items)
    return header + blocks


def splice_region(md_text, region_body):
    block = f"{MD_REGION_START}\n{region_body}\n{MD_REGION_END}"
    if MD_REGION_START in md_text and MD_REGION_END in md_text:
        pre = md_text.split(MD_REGION_START)[0]
        post = md_text.split(MD_REGION_END, 1)[1]
        return pre + block + post
    sep = "" if md_text.endswith("\n") else "\n"
    return md_text + sep + "\n" + block + "\n"
