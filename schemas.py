from marshmallow import Schema, fields

class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True) # remember price is a Float value here

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True) # load_only means we need to ask this store_id value for this item while we retrieve item data for that store
    store = fields.Nested(PlainStoreSchema(), dump_only=True) # here we will have only 1 store associated hence only PLainStoreSchema object within it
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))

# We may not update both name and price so we ewon't have required=true here
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

# we will have multiple items as a list within a store hence we will be using fields.List
class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True) # load_only means we need to ask this store_id value for this item while we retrieve tag data for that store
    store = fields.Nested(PlainStoreSchema(), dump_only=True) # here we will have only 1 store associated hence only PLainSchema object within it
    items = fields.List(fields.Nested(PlainItemSchema(), dump_only=True))

class ItemsTagsSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class UserRegisterSchema(UserSchema):
    email = fields.Str(required=True)