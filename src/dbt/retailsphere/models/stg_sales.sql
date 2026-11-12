select
    order_id,
    line_number,
    cast(sale_date as date) as sale_date,
    store_id,
    product_id,
    quantity,
    unit_price,
    quantity * unit_price as sales_value
from {{ ref('raw_sales') }}