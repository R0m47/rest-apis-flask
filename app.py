from flask import Flask, request

app = Flask(__name__)

stores = [
    {
        "name": "My store",
        "items": [{"name": "Chair", "price": 15.99}],
    }
]


@app.get("/store")
def get_stores():
    return {"stores": stores}


@app.get("/store/<string:store_name>")
def get_store(store_name):
    for store in stores:
        if store["name"] == store_name:
            return store
    return {"message": "Store not found"}, 404


@app.get("/store/<string:store_name>/item")
def get_store_items(store_name):
    for store in stores:
        if store["name"] == store_name:
            return {"items": store["items"]}
    return {"message": "Store not found"}, 404


@app.post("/store")
def create_store():
    request_data = request.get_json()
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return new_store, 201


@app.post("/store/<string:store_name>/item")
def create_item(store_name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == store_name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return new_item, 201
    return {"message": "Store not found"}, 404
