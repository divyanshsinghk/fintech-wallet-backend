from bson import ObjectId

def serialize_mongo(doc: dict):
    for key, value in list(doc.items()):
        if isinstance(value, ObjectId):
            doc[key] = str(value)
    return doc
