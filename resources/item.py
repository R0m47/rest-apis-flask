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
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @item_blueprint.arguments(ItemUpdateSchema)
    @item_blueprint.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()
        return item


@item_blueprint.route("/item")
class ItemList(MethodView):
    @item_blueprint.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

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
