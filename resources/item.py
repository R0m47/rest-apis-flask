import uuid
from flask import request
from flask.views import MethodView
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from models import ItemModel

item_blueprint = Blueprint("Items", __name__, description="Operations on items")


@item_blueprint.route("/item/<string:item_id>")
class Item(MethodView):
    @item_blueprint.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Delete an item is not implemented yet.")

    @item_blueprint.arguments(ItemUpdateSchema)
    @item_blueprint.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get_or_404(item_id)
        raise NotImplementedError("Updating an item is not implemented yet.")


@item_blueprint.route("/item")
class ItemList(MethodView):
    @item_blueprint.response(200, ItemSchema(many=True))
    def get(self):
        return items.values()

    @item_blueprint.arguments(ItemSchema)
    @item_blueprint.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")
        return item
