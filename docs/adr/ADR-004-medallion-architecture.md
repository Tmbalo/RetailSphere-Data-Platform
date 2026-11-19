# ADR-004: Medallion Architecture Layer Design

| | |
|---|---|
| **Status** | Approved, 01 June 2026 (rewritten in MADR format, 19 Nov 2026) |
| **Decision-maker** | T. Mbalo (DSA) |
| **Approver** | N. Mahlangu (CDO) |
| **Consulted** | Johan van der Merwe (Finance), Priya Naidoo (CRM & Loyalty) |
| **Informed** | Domain stakeholders |
| **Register** | ADR-REG-001 (index of all ADRs) |

## Context and problem statement
RetailSphere extracts data from about 10 source systems, each with a different data structure. Finance needs an audit trail, and the platform must be able to reprocess data without going back to the source systems. What layered architecture should the platform use?

## Decision drivers
- Audit trail and reprocessing without re-extracting (Johan)
- Data governance and POPIA (Priya)
- 10 sources with different structures
- Incremental loads: process only what has changed
- A design a small team can build and run

## Considered options
1. Inmon (stage → enterprise data warehouse → data marts)
2. Kimball (stage → data marts)
3. Data Vault (stage → raw vault → business vault → data marts)
4. Medallion layers with a Kimball star schema in Gold (Bronze → Silver → Gold)

## Decision outcome
Chosen option: **4**, because it keeps a raw copy in Bronze for audit and reprocessing, gives Silver a clear home for quality and POPIA rules, and delivers Kimball star schemas in Gold that the business can query, all without needing specialist skills.

### Consequences
- Good, because data can be reprocessed from Bronze without touching the source systems.
- Good, because quality and POPIA rules have one clear place to live (Silver).
- Good, because Gold is a star schema that business users and Power BI understand.
- Bad, because the same data is held up to three times.
- Bad, because each layer adds pipelines to build, schedule and monitor.

### Confirmation
- The dbt project is organised into Bronze, Silver and Gold folders, and each layer reads only from the layer before it, which can be checked in the dbt lineage graph.
- Every change runs through the CI gate (`dbt build` plus the documentation checks) before it can merge.
- Each layer reconciles to a known answer key (row counts and control totals).

## Pros and cons of the options

### Inmon
- Good, because it gives one integrated enterprise model.
- Bad, because the large model has to be built up front before any business value arrives.

### Kimball (stage → marts)
- Good, because it's the fastest route to reports, with the fewest layers.
- Bad, because there's no persistent raw copy, so reprocessing means going back to the source systems.

### Data Vault
- Good, because it handles many sources and change well, with full history.
- Bad, because it needs people who know the method.
- Bad, because it creates many more tables, and still needs a star schema on top for reporting.

### Medallion with Kimball Gold
- Good, because it's simple to understand and keeps a raw copy.
- Bad, because the same data is held up to three times.

## More information
- ADR-REG-001 v3.0 (pending): records the move to MADR format for all ADRs; the remaining ADRs will be converted once the team template is confirmed.
- Template: MADR (Markdown Architecture Decision Records), adr.github.io/madr