from models import ItemModel
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from flask_jwt_extended import jwt_required, get_jwt # required to protect the urls. Urls can only be accessed with access token when using jwt_required decorator 

# NOTE: Currently we have added JWT requirement i.e Bearer token requirement for only item and user. We can extend it to other entities such as stores and tags too

blp = Blueprint("items", __name__, description="Operation on Items")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required() # jwt_required forces the url to be accessed only using access token
    # blp.response decorator pf marshmallow returns the items dictionary as ItemSchema
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        return item

    @jwt_required()
    def delete(self, item_id):
        # we will get the jwt where is_admin was stored using add_claims_to_jwt and if is_admin is true only then we will proceed with delete operation,
        # otherwise we will throw error message that admin privilege is required
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privileges required.")
        item = ItemModel.query.get_or_404(item_id)

        db.session.delete(item)
        db.session.commit()

        return {"message": "Item successfully deleted."}

    # use blp.arguments to fetch marshmallow validation using ItemUpdateSchema and enforce them by passing item_data object to the put method.
    # remember that item_data will be always the first parameter in this method
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.name = item_data["name"]
            item.price = item_data["price"]
        else:                 
            item = ItemModel(id=item_id, **item_data) # if item doesn't exist assign the inputted id as the item id and assign itemdata to itemModel as kwarg

        db.session.add(item)
        db.session.commit()

        return item

@blp.route("/item")
class ItemList(MethodView):
    # remember since this is a list endpoint, we would want ItemSchema(many=True) to indicate that many Items are being returned as a list
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    # setting fresh=True to signify that the delete endpoint will require a fresh access token in order to perfrom the operation. No non fresh token would work for this endpoint
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data) # apply item_data as keywrd args to the ItemModel and store it in db

        try:
            db.session.add(item)
            db.session.commit()

        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting item to database.")

        return item


