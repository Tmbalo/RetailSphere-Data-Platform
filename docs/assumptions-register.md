# Tool Assumptions Register

Living register of design claims that depend on tool or source behaviour not yet tested hands-on. Each assumption is verified by a small hands-on test (a spike) before the build depends on it.

**How to use it**
- When an assumption is verified, record the date and source.
- When one turns out wrong, raise a correction to the affected document.
- This is a living file, not a versioned, approved document.

| # | Assumption | Used in | Status | Verify when |
|---|---|---|---|---|
| 1 | dbt unit tests support SQL models only, not snapshots | TST-001 §4 | Verified (dbt docs, Sep 2026) | Done |
| 2 | dbt unit tests run in dev/CI, not production | TST-001 §4 | Verified (dbt docs, Sep 2026) | Done |
| 3 | dbt does not fail builds on missing descriptions by itself; an add-on tool is needed | MET-001 §6, TST-001 §6 | Verified (Oct 2026) | Done; MET-001 v1.1 wording fix owed |
| 4 | The Fabric dbt adapter supports unit tests | TST-001 §4 | Unverified | Step 12, Fabric stage |
| 5 | The all-columns documentation check works with Fabric metadata | TST-001 §6 | Unverified | Step 12, Fabric stage |
| 6 | The `dbt_utils` composite-key test works on Fabric | DID-001 §4, TST-001 §3 | Unverified | Step 12, Fabric stage |
| 7 | dbt `source freshness` works on Fabric Bronze tables | TST-001 §3 | Unverified | Step 13 |
| 8 | ADF can run a Python step for PDF extraction into Silver staging | DID-001 §3-4 | Unverified | Step 13 |
| 9 | dbt snapshots work on Fabric Warehouse for SCD Type 2 | DID-001 §5, TST-001 §4 | Unverified | Step 14 |
| 10 | Fabric Warehouse: no indexes, informational-only constraints, no native partitioning | PDD-001 §6-7 | Verified (Aug 2026) | Recheck at Step 15, as features change |
| 11 | Fabric `CLUSTER BY` clustering is available on Warehouse tables | PDD-001 §7 | Verified (docs, Aug 2026) | Confirm hands-on at Step 15 |
| 12 | GitHub branch protection can apply to administrators | TST-001 §6 | Unverified | Step 12, GitHub setup |
| 13 | Marketing Cloud sends at most one attempt per day per combination | PDD-001 §5.2.5 | Unverified (source behaviour) | Before Step 13 |
| 14 | dbt targets can direct a proving run to a separate schema in the Fabric Test/UAT workspace | TST-001 §8 | Unverified | Step 12, Fabric stage |
