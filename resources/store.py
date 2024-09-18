from db import db
from models import StoreModel
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operation on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)

        db.session.delete(store)
        db.session.commit()
        
        return {"message": "Store successfully deleted."}

@blp.route("/store")
class StoreList(MethodView):
    # use blp.arguments to fetch marshmallow validation using StoreSchema and enforce them by passing store_data object to the post method.
    # remember that store_data will be always the first parameter in this method
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        store = StoreModel(**store_data)

        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Store by this name already exists in the database.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while adding store to database.")
        
        return store

    # returns all the stores when storeschema is set to many=True indicating a list of stores can be returned
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()



