from tools.ingest.harvest import deep_external_urls, split_primary

RECORD = {
    "full_text": "See it https://t.co/abc",
    "metadata": {"legacy": {"entities": {"urls": [
        {"expanded_url": "http://ditther.com"},
        {"expanded_url": "https://twitter.com/x/status/1"},
    ]}}, "bio": "links: https://linktr.ee/me and http://blurr.design"},
}

def test_deep_external_urls_dedups_and_drops_twitter():
    urls = deep_external_urls(RECORD)
    assert "http://ditther.com" in urls
    assert "http://blurr.design" in urls
    assert "https://linktr.ee/me" in urls
    assert not any("twitter.com" in u or "t.co" in u for u in urls)

def test_deep_external_urls_is_ordered_and_unique():
    urls = deep_external_urls(RECORD)
    assert len(urls) == len(set(urls))

def test_split_primary_demotes_denylisted():
    primary, _all = split_primary(["https://linktr.ee/me", "http://blurr.design"])
    assert primary == ["http://blurr.design"]

def test_split_primary_falls_back_to_all_when_only_utility():
    primary, _all = split_primary(["https://linktr.ee/me"])
    assert primary == []
