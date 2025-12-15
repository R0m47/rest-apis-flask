from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import uuid
from db import db
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.store import StoreModel
from schemas import StoreSchema


store_blueprint = Blueprint("Stores", __name__, description="Operations on stores")


@store_blueprint.route("/store/<string:store_id>")
class Store(MethodView):
    @store_blueprint.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}


@store_blueprint.route("/store")
class StoreList(MethodView):
    @store_blueprint.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()

    @store_blueprint.arguments(StoreSchema)
    @store_blueprint.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while creating the store.")
        return store
