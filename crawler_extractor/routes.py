import json
from typing import Tuple

from bson import json_util
from flask import jsonify, Response, Blueprint, make_response
from flask.globals import request
from threading import Thread
from dotenv import load_dotenv, find_dotenv

from crawler_extractor.helpers import *
from constant import FAILURE_RESPONSE, SUCCESS_RESPONSE, NULL_CONTAINER, SERVER_ERROR

load_dotenv(find_dotenv())

product_source = os.getenv("PRODUCT_REF")

crawl_extract = Blueprint("crawler_extractor", __name__, url_prefix="/product/v1")


@crawl_extract.errorhandler(Exception)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    print(_error)
    return make_response(jsonify(SERVER_ERROR), 500)


@crawl_extract.route('/get_html', methods=["GET"])
def get_html() -> Tuple[Response, int]:
    """
    returns status code and success response and stores html

    :return -> Dict()
    """
    query_args = request.args
    if query_args.get("sku"):
        url = build_url(query_args.get('sku'))
    else:
        return jsonify(FAILURE_RESPONSE), 400
    thread = Thread(target=store_html, args=(url,))
    thread.start()
    return jsonify(SUCCESS_RESPONSE), 200


@crawl_extract.route('/get_product_details', methods=["GET"])
def get_product_details() -> Response:
    """
    returns status code and product details and store it in DB

    :return: -> Dict
        {
            data: {
                    “title” : “Kellogg's Corn Flakes Original, 1.2 kg: Amazon.in: Amazon Pantry”,
                    “offerPrice” : “299.00”,
                    “description”:”Don't compromise on morning nourishment when you have a balanced, great-tasting
                                   breakfast that is high in iron, vitamin b1, b2, b3, b6 and vitamin c,
                                   it is quick to eat and gives you energy even after 3 hours”,
                    “ratingsMap” : {
                        “overallCount” : “5548”,
                        “5star” : “68%”,
                        “4star”: “23%”,
                        “3star”: “5%”,
                        “2star”: “1%”,
                        “1star”: “3%”
                        }
                },
            status_code: 200,
            message: success
        }

    """
    query_args = request.args
    if query_args.get("sku"):
        sku = query_args.get('sku')
        url = build_url(sku)
    else:
        return make_response(jsonify(FAILURE_RESPONSE), 400)
    check, product_details = check_in_last_60_minutes(sku)
    if check:
        data = json.loads(json_util.dumps(product_details))
        response = {
            "status_code": 200,
            "message": "success",
            "data": data
        }
        return make_response(jsonify(response), 200)
    flag, product_details = extract_product_details(url, product_source)
    null_product = all(value in NULL_CONTAINER for value in product_details.values())
    if flag and not null_product:
        data = json.loads(json_util.dumps(product_details))
        response = {
            "status_code": 200,
            "message": "success",
            "data": data
        }
        thread = Thread(target=store_product, args=(product_details, sku))
        thread.start()
        return make_response(jsonify(response), 200)
    return make_response(jsonify(FAILURE_RESPONSE), 400)


@crawl_extract.route('/get_product_details_history', methods=['GET'])
def get_product_details_history() -> Response:
    """
    return product stored in DB before last date

    :return:
    {
        "_id": {
            "$oid": "6114e5d096bf585c177e8deb"
        },
        "description": "To take your favourite Masala taste experience to the next level",
        "offerPrice": "₹162.00",
        "ratingsMap": {
            "1star": "4%",
            "2star": "3%",
            "3star": "9%",
            "4star": "23%",
            "5star": "62%",
            "overallCount": "13,271 global ratings"
        },
        "timestamp": {
            "$date": 1628779304429
        },
        "title": "Maggi 2-Minute Special Masala Instant Noodles, 70g (Pack of 12)",
        "unique_sku": "B07JQNB7QG"
    }
    """
    query_args = request.args
    if query_args.get("sku") and query_args.get("timestamp"):
        sku = query_args.get('sku')
        timestamp = query_args.get('timestamp')
    else:
        return make_response(jsonify(FAILURE_RESPONSE), 400)
    try:
        product_details = retrieve_last_before(sku, timestamp)
        response = {
            "status_code": 200,
            "message": "success",
            "data": json.loads(json_util.dumps(product_details))
        }
        status_code = 200
    except Exception:
        response = FAILURE_RESPONSE
        status_code = 400
    return make_response(jsonify(response), status_code)


@crawl_extract.route('/list_all_products', methods=['GET'])
def list_all_products() -> Response:
    """
    fetches all details and records from product dir

    :return:
            {
                "data": [
                            {
                                "_id": {
                                    "$oid": "611555c0ebaa78c4bf941d74"
                                },
                                "ratingsMap": {},
                                "timestamp": {
                                    "$date": 1628807960568
                                },
                                "unique_sku": "B0991MJLN"
                            },
                            {
                                "_id": {
                                    "$oid": "611552cfb15a98c0025a6242"
                                },
                                "description": "This slim, ultra-portable HP 14 laptop delivers reliable performance.",
                                "ratingsMap": {
                                    "4star": "100%",
                                    "overallCount": "1 global rating"
                                },
                                "timestamp": {
                                    "$date": 1628807207292
                                },
                                "title": "HP 14 Ryzen 5 3500U 14-inch(35.6 cm) Thin & Light Laptop(8GB RAM/256GB SSD)
                                "unique_sku": "B0991MJLN2"
                            }
                    ],
                "message": "ok",
                "status_code": 200
            }

    """

    data = retrieve_all_products()
    response = {
        "status_code": 200,
        "message": "ok",
        "data": json.loads(json_util.dumps(data))
    }
    return make_response(jsonify(response), 200)


@crawl_extract.route('/price_trend', methods=['GET'])
def price_trend() -> Response:
    """

    :return:
        {
            "data": [
                        {
                            "price": "₹162.00",
                            "timestamp": "2021-08-12T14:41:44Z"
                        },
                        {
                            "price": "₹162.00",
                            "timestamp": "2021-08-12T12:42:04Z"
                        },
                        {
                            "price": "₹162.00",
                            "timestamp": "2021-08-12T12:37:37Z"
                        }
                    ],
            "message": "ok",
            "status_code": 200
        }
    """
    query_args = request.args
    if query_args.get("sku"):
        sku = query_args.get('sku')
    else:
        return make_response(jsonify(FAILURE_RESPONSE), 400)
    data = retrieve_price_trends(sku)
    response = {
        "status_code": 200,
        "message": "ok",
        "data": json.loads(json_util.dumps(data))
    }
    return make_response(jsonify(response), 200)
