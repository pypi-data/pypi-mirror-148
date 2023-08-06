# Pymongo Paginate

> author: github.com/gabrielmrts/

## Example

```

from pymongo_paginate import PyMongoPaginate

collection = db['your_pymongo_collection']
query = collection.find()

page = 1 ## Current page
pageSize = 10 ## Items per page

pagination = PyMongoPaginate(query, page, pageSize)
paginate = pagination.paginate()

---------------------------------------------------
Output -> dict {
            "page": 1,
            "page_count": 1,
            "item_count": 10,
            "items": []
        }
        

```

