# Glossary of Terms

Plain-English definitions of the technical terms used throughout this repository. Written for anyone reviewing this project without a data engineering background — recruiters, hiring managers, or curious stakeholders.

---

## Architecture & Platform

**Medallion Architecture**
A way of organizing a data platform into three progressively cleaner layers — Bronze, Silver, and Gold. Data gets more refined and trustworthy as it moves through each layer, the way ore gets refined into metal.

**Bronze Layer**
The raw landing zone. Data arrives here exactly as it came from the source system — no cleaning, no reshaping. This is the "as received" copy, kept for traceability if anything downstream needs to be recomputed.

**Silver Layer**
Cleaned and conformed data. Duplicate records are resolved, data types are standardized, and business rules are applied. This is where raw source data starts becoming trustworthy.

**Gold Layer**
The final, business-ready layer — the star schema (see below) that reports and dashboards actually query. Optimized for business questions, not for how the source system happened to store the data.

**dbt (data build tool)**
A tool that manages the SQL transformations moving data from Bronze → Silver → Gold. Rather than writing ad-hoc scripts, dbt lets you define transformations as version-controlled, testable code — and it's also where this project enforces data quality rules (like uniqueness or "this value should never be NULL") that the target database itself doesn't enforce.

**ADF (Azure Data Factory)**
Microsoft's cloud tool for scheduling and orchestrating data pipelines — the "when does data move, and in what order" layer. Think of it as the conductor that tells each piece (extract, load, transform) when to run.

**Microsoft Fabric Warehouse**
The cloud database platform hosting this project's Gold layer. It stores data using the Delta Lake format (see below) and is queried using standard T-SQL.

**Delta Lake**
An open storage format (built on Parquet files) that adds database-like reliability — consistent reads, version history, ability to roll back — to data stored in a data lake. Fabric Warehouse uses this format under the hood.

**V-Order**
A write-time optimization Fabric applies to Delta Lake files, reorganizing how data is physically stored to make later reads faster. Roughly equivalent in *purpose* to a database index, though it works completely differently under the hood.

**OneLake**
Fabric's single, shared storage layer. Every Fabric tool (Warehouse, Power BI, notebooks) reads from the same underlying storage, so there's no need to copy data between tools.

---

## Data Modeling (Kimball / Dimensional Modeling)

**Kimball Methodology**
A widely used approach to designing data warehouses, built around star schemas (see below) organized by business process. Named after Ralph Kimball, who popularized it. This project follows Kimball conventions throughout.

**Star Schema**
The Gold layer's table layout: one central **fact table** (the events/measurements) surrounded by several **dimension tables** (the descriptive context) — visually resembling a star when diagrammed.

**Fact Table**
A table recording something that happened or a measurement at a point in time — a sale, a stock count, a purchase order. Mostly numbers and foreign keys pointing to dimension tables.

**Dimension Table**
A table providing descriptive context for a fact — who the customer was, which product, which store. Mostly text attributes used for filtering and grouping in reports.

**Grain**
The precise definition of what one row in a table represents — e.g., "one row per product, per store, per day." Getting the grain right is the single most important decision in designing any fact table.

**Surrogate Key**
An internally generated, meaningless ID (usually a simple integer) used as a table's primary key, instead of relying on a business identifier that might change or collide.

**Degenerate Dimension**
A business identifier (like an order number) stored directly on a fact table rather than in its own dimension table, because it has no other descriptive attributes worth modeling separately.

**Conformed Dimension**
A dimension table (like Date or Product) shared consistently across multiple fact tables, so "date" always means the same thing everywhere in the platform.

**SCD Type 2 (Slowly Changing Dimension, Type 2)**
A technique for preserving history when a dimension record changes — instead of overwriting the old value, a new row is added and the old one is marked as expired. Lets you answer "what did this look like at the time," not just "what does it look like now."

**Transaction Fact Table**
A fact table where each row is created once, at the moment an event happens, and is never modified afterward. Example: `FactSales`.

**Periodic Snapshot Fact Table**
A fact table that captures a recurring state at fixed intervals (e.g., daily stock levels), rather than individual events.

**Accumulating Snapshot Fact Table**
A fact table tracking something that moves through a defined set of stages over time (e.g., a purchase order: raised → approved → shipped → received), where the same row gets updated as it progresses.

**Role-Playing Dimension**
The same physical dimension table (usually Date) joined multiple times in one query, each join representing a different meaning — e.g., "order date" vs. "ship date," both pointing to the same underlying Date table.

---

## Governance & Process

**ADR (Architecture Decision Record)**
A short document capturing a significant design decision, the reasoning behind it, and the alternatives considered — creating a permanent, defensible record of *why* the platform is built the way it is.

**POPIA**
South Africa's Protection of Personal Information Act — the data privacy law governing how personal customer data can be collected, stored, and used. Similar in spirit to Europe's GDPR.

**Data Mart**
A subset of the Gold layer scoped to one business domain (e.g., the Sales data mart) — a smaller, focused piece of the overall platform.
