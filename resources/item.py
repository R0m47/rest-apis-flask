import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores

item_blueprint = Blueprint("Items", __name__, description="Operations on items")


@item_blueprint.route("/item/<string:item_id>")
class Item(MethodView):
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted."}
        except KeyError:
            abort(404, message="Item not found.")

    def put(self, item_id):
        item_Data = request.get_json()
        if (
            "price" not in item_Data
            or item_Data["price"] <= 0
            or "name" not in item_Data
        ):
            abort(
                400,
                message="Bad request. Ensure 'price' and 'name' are included in the JSON payload.",
            )
        try:
            item = items[item_id]
            item |= item_Data
            return item
        except KeyError:
            abort(404, message="Item not found.")


@item_blueprint.route("/item")
class ItemList(MethodView):
    def get(self):
        return {"items": list(items.values())}

    def post(self):
        item_data = request.get_json()
        if (
            ("price" not in item_data)
            or (item_data["price"] <= 0)
            or ("store_id" not in item_data)
            or ("name" not in item_data)
        ):
            abort(
                400,
                message="Bad request. Ensure 'price', 'store_id', and 'name' are included in the JSON payload.",
            )
        for item in items.values():
            if (
                item["name"] == item_data["name"]
                and item["store_id"] == item_data["store_id"]
            ):
                abort(400, message="Item with that name already exists.")
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found.")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201
