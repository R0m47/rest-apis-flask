import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import items, stores
from schemas import ItemSchema, ItemUpdateSchema

item_blueprint = Blueprint("Items", __name__, description="Operations on items")


@item_blueprint.route("/item/<string:item_id>")
class Item(MethodView):
    @item_blueprint.response(200, ItemSchema)
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

    @item_blueprint.arguments(ItemUpdateSchema)
    @item_blueprint.response(200, ItemSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found.")


@item_blueprint.route("/item")
class ItemList(MethodView):
    @item_blueprint.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @item_blueprint.arguments(ItemSchema)
    @item_blueprint.response(201, ItemSchema)
    def post(self, item_data):
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
