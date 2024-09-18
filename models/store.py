from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete") # creates a new field within store model called "items" that stores all items info using ItemModel that match store_id primary key
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")
 # cascade="all, delete" signifies that if we happen to delete a store, all it's items should also be deleted as the items would remain orphan if store gets deleted