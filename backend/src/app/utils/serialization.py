from bson.objectid import ObjectId
from datetime import datetime


class Serialization:
    @staticmethod
    def obj_to_str(obj):
        if isinstance(obj, ObjectId):
            return str(obj)

        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return obj

    @staticmethod
    def serialize_document(document):
        """Convert MongoDB document (dict) to JSON serializable format."""
        if not document:
            return None

        return {key: Serialization.obj_to_str(value) for key, value in document.items()}

    @staticmethod
    def serialize_list(documents):
        """Convert a list of MongoDB documents to JSON serializable format."""
        return [Serialization.serialize_document(doc) for doc in documents]
