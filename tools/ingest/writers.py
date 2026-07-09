def merge_items(doc, enriched_items, source_export, ingested_at):
    existing = {i["id"] for i in doc.get("items", [])}
    for it in enriched_items:
        if it["id"] in existing:
            continue
        row = dict(it)
        row["source_export"] = source_export
        row["ingested_at"] = ingested_at
        # teardown_domains is enricher-internal; not part of the item record
        row.pop("teardown_domains", None)
        doc.setdefault("items", []).append(row)
        existing.add(it["id"])
    return doc


def merge_site_designs(doc, site_designs):
    reg = doc.setdefault("site_designs", {})
    for domain, payload in (site_designs or {}).items():
        if domain in reg:
            continue  # never overwrite an existing teardown
        reg[domain] = payload
    return doc
