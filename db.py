import os
from typing import Dict

from dotenv import load_dotenv, find_dotenv
from pymongo import MongoClient

load_dotenv(find_dotenv())

DB_PASS = os.getenv("DB_PASSWORD")
CONNECTION_STRING = os.getenv("MONGO_DB_URI").format(DB_PASS)


def get_database():
    """
    returns DB client to query database

    :return: db_client with database reference
    """
    db_name = os.getenv("DB_NAME")
    mongo_client = MongoClient(CONNECTION_STRING)
    database_client = mongo_client.get_database(db_name)
    return database_client


db_client = get_database()


def store_document(collection_name: str, document: Dict):
    """
    store document or record in database

    :param collection_name: name of table or collection to store in it
    :param document: document or record to store in db

    :return: document or record storage id
    """
    collection = db_client.get_collection(collection_name)
    document_store_id = collection.insert(document)
    return document_store_id


def get_all_documents(collection_name: str, doc_filter: Dict = None, sort: list = None) -> Dict:
    """
    Retrieve all documents or records or rows from a table or collection

    :param sort: sorting tuple to sort on certain fields
    :param doc_filter: record or document filter dict
    :param collection_name: name of table or collection

    :return: fetch all documents on basis of filter and sorting
    """
    collection = db_client.get_collection(collection_name)
    return collection.find(doc_filter).sort(sort)


def get_least_before(collection_name: str, doc_filter: Dict, sort: list) -> Dict:
    """
    get last record or document from collection or table

    :param collection_name: name of collection or table
    :param doc_filter: document filter or conditions to select record
    :param sort: sort tuple to sort on certain fields

    :return: fetch single record from collection
    """
    collection = db_client.get_collection(collection_name)
    collection_obj = collection.find(doc_filter, limit=1).sort(sort)
    return collection_obj.next()
