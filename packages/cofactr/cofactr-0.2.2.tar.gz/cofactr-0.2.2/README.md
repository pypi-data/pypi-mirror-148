# Cofactr

Python client library for accessing Cofactr.

## Example

```python
from cofactr.graph import GraphAPI
from cofactr.cursor import first

g = GraphAPI()

cursor = g.get_products(
    query="esp32",
    fields=["mpn", "assembly"],
    batch_size=10,  # Data is fetched in batches of 10 products.
    limit=10,  # `list(cursor)` would have at most 10 elements.
    external=False,
)

data = first(cursor, 2)

# To send to web app.
response = {
    "data": data,
    # To get the next 10 after the 2 in `data`.
    "paging": cursor.paging,
}
```