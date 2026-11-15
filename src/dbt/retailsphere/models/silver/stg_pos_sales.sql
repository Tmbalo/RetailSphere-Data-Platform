-- Silver: cleaned POS sales lines, one row per order line.
-- Column names follow STM-001's FactSales mapping.
with source as (
    select * from {{ ref('pos_sales') }}
)

select
    transaction_id                          as order_id,
    line_number,
    transaction_timestamp                   as sales_timestamp,
    cast(transaction_timestamp as date)     as sales_date,
    store_id,
    barcode                                 as pos_barcode,
    customer_id,
    customer_id is null                     as is_anonymous,
    quantity,
    unit_price,
    discount_amount,
    quantity * unit_price                   as sales_value,
    case
        when quantity * unit_price = 0 then 0
        else round(discount_amount / (quantity * unit_price) * 100, 2)
    end                                     as discount_pct,
    1                                       as source_system_code
from source