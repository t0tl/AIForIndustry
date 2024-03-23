### Build LanceDB database
import lancedb

uri = "data_storage"
db = lancedb.connect(uri)

tbl = db.create_table("my_table",
                data=[{"vector": [3.1 for _ in range(1536)], "item": "foo", "price": 10.0},
                      {"vector": [5.9 for _ in range(1536)], "item": "bar", "price": 20.0}])
