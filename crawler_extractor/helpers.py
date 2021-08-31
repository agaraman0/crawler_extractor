import os
import yaml
from datetime import datetime
from requests_html import HTMLSession
from typing import Dict, Optional, List, Any

from constant import PROXY_DIR, REQUEST_HEADERS, PRODUCT_COLLECTION, HTML_COLLECTION
from db import get_database, store_document, get_all_documents, get_least_before

db_client = get_database()

session = HTMLSession()


def crawl_html(web_url: str) -> str:
    """
    crawls web page using web url address

    :param web_url: address of web page

    :return: web page html source
    """
    html_src = session.request(url=web_url, proxies=PROXY_DIR, method='get', headers=REQUEST_HEADERS)
    return html_src.text


def extract_product_details(product_ref: str, product_destination: str) -> (bool, Dict):
    """
    extract product details from product page

    :param product_destination:
    :param product_ref: product SKU id or product url

    :return: product details in following dict format
            {
                 “title” : “Kellogg's Corn Flakes Original, 1.2 kg: Amazon.in: Amazon Pantry”,
                 “offerPrice” : “299.00”,
                 “description”:”Don't compromise on morning nourishment when you have a balanced,
                                great-tasting breakfast that is high in iron, vitamin b1, b2, b3,
                                b6 and vitamin c, it is quick to eat and gives you energy even
                                after 3 hours”,
                 “ratingsMap” : {
                    “overallCount” : “5548”,
                    “5star” : “68%”,
                    “4star”: “23%”,
                    “3star”: “5%”,
                    “2star”: “1%”,
                    “1star”: “3%”
                 }
            }
    """
    html_src = session.request(url=product_ref, proxies=PROXY_DIR, method='get', headers=REQUEST_HEADERS)
    with open("selectors.yaml", 'r') as stream:
        try:
            selectors = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            raise exc
    if selectors.get(product_destination):
        selector_list = selectors.get(product_destination)
        product_details = parse_selectors(selector_list, html_src)
        return True, product_details
    return False, None


def parse_selectors(selectors_collection: list, html_src):
    """
    constructs a product_details dict and returns it

    :param selectors_collection: configurable selectors collection object which is design flexible and extensible for
                                future reference
    :param html_src: HTMLResponse object which parse css selectors to extract product details

    :return: {
                "description": "Style Name:Chilli Garlic  |  Size:75 g (Pack of 5)\nNow prepare authentic and
                                restaurant style fried rice at home in just 3 easy steps using the
                                your choice and turn steamed rice into your family's favourite fried rice dish
                                everyday within 5 minutes! Maggi fried rice spice mix share bag contains 5
                                single serve sachets to ensure that you get a fresh taste & flavour every time
                                you use them and each sachet helps prepare fried rice to serve four.",
                "offerPrice": "₹60.00",
                "ratingsMap": {
                                "1star": "10%",
                                "2star": "5%",
                                "3star": "12%",
                                "4star": "21%",
                                "5star": "53%",
                                "overallCount": "348 global ratings"
                            }
                "title": "Maggi Fried Rice Masala, Chilli Garlic, 75g Pouch (5 Sachets), Restaurant Style",
    """
    dict_details = {}
    for collection in selectors_collection:
        if collection.get('key') and collection.get('selector'):
            key = collection.get('key')
            selector = collection.get('selector')
            val = html_src.html.find(selector, first=True)
            if val is None:
                continue
            val = val.text
            dict_details[key] = val
        elif collection.get('key') and collection.get('child'):
            key = collection.get('key')
            child_collection = collection.get('child')
            dict_details[key] = parse_selectors(child_collection, html_src)
    return dict_details


def store_html(web_url: str) -> str:
    """
    "Store html document into db by crawling from web

    :param web_url: web address to crawl for web page

    :return: web page html document storage id
    """
    html_src = session.request(url=web_url, proxies=PROXY_DIR, method='get', headers=REQUEST_HEADERS)
    html_src = html_src.text
    html_dict = {
        "timestamp": datetime.now(),
        "html": html_src
    }
    html_storage_ref = store_document(HTML_COLLECTION, html_dict)
    return str(html_storage_ref)


def store_product(product_details: Dict, product_sku) -> str:
    """
    process product_details and store in db
    
    :param product_sku: product sku id which is unique to every product
    :param product_details: product details which needs to processed and store

    :return: product details document storage id
    """
    product_details['timestamp'] = datetime.now()
    product_details["unique_sku"] = product_sku
    product_storage_id = store_document(PRODUCT_COLLECTION, product_details)
    return str(product_storage_id)


def retrieve_all_products() -> List:
    """
    fetch all products from db and occurrence details

    :return:
        List of products and with all details of products
        [
            {
                "_id": {
                    "$oid": "611552cfb15a98c0025a6242"
                },
                "description": "This slim, ultra-portable HP 14 laptop delivers reliable performance.,
                "ratingsMap": {
                    "4star": "100%",
                    "overallCount": "1 global rating"
                },
                "timestamp": {
                    "$date": 1628807207292
                },
                "title": "HP 14 Ryzen 5 3500U 14-inch(35.6 cm) FHD Thin & Light Laptop(8GB RAM/256GB SSD + 1TB,
                "unique_sku": "B0991MJLN2"
            },
            {
                "_id": {
                    "$oid": "61151df48d90c3f674a96c2f"
                },
                "description": "This slim, ultra-portable HP 14 laptop delivers reliable performance.",
                "ratingsMap": {
                    "4star": "100%",
                    "overallCount": "1 global rating"
                },
                "timestamp": {
                    "$date": 1628793676504
                },
                "title": "HP 14 Ryzen 5 3500U 14-inch(35.6 cm) FHD Thin & Light Laptop(8GB RAM/256GB SSD + 1TB",
                "unique_sku": "B0991MJLN2"
            }
        ]
    """
    data = []
    sort = [("timestamp", -1)]
    products = get_all_documents(PRODUCT_COLLECTION, sort=sort)
    for product in products:
        data.append(product)
    return data


def retrieve_price_trends(product_sku: str) -> List[Dict[str, Optional[Any]]]:
    """
    fetch price and timestamps for product to analyze price trends

    :param product_sku: product unique sku identifier

    :return: price trends of product
            [
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
            ]
    """
    price_trend = []
    sort = [("timestamp", -1)]
    doc_filter = {"unique_sku": product_sku}
    products = get_all_documents(PRODUCT_COLLECTION, doc_filter=doc_filter, sort=sort)
    for product in products:
        timestamp = product.get("timestamp").strftime("%Y-%m-%dT%H:%M:%SZ") if product.get("timestamp") else None
        price_trend.append({"timestamp": timestamp, "price": product.get("offerPrice")})
    return price_trend


def build_url(product_sku: str) -> str:
    """
    create url from product sku id

    :param product_sku: product unique sku identifier

    :return:
    """
    product_web_address = os.getenv('PRODUCT_WEB_PAGE_INITIAL_URL')
    return product_web_address.format(product_sku)


def retrieve_last_before(product_sku: str, time: str) -> Dict:
    """
    retrieve last recent record of a product less then a timestamp

    :param product_sku: product unique sku identifier
    :param time: timestamp for which to extract

    :return:
        product details or None
    """
    datetime_obj = datetime.strptime(time, "%Y-%m-%d")
    document_filter = {'unique_sku': product_sku, 'timestamp': {"$lt": datetime_obj}}
    sort_by = [('timestamp', -1)]
    return get_least_before(PRODUCT_COLLECTION, document_filter, sort_by)


def check_in_last_60_minutes(product_sku: str) -> (bool, Dict):
    """
    check if any request made for same product in last 60 minutes

    :param product_sku: product unique sku identifier

    :return:
        Tuple of bool and product details
    """
    datetime_obj = datetime.now()
    document_filter = {'unique_sku': product_sku, 'timestamp': {"$lte": datetime_obj}}
    sort_by = [('timestamp', -1)]
    try:
        last_extracted_product = get_least_before(PRODUCT_COLLECTION, document_filter, sort_by)
    except StopIteration:
        return False, None
    last_extracted_product_time = last_extracted_product.get('timestamp')
    time_difference = datetime_obj - last_extracted_product_time
    time_difference_in_minutes = time_difference.total_seconds()//60
    if time_difference_in_minutes <= 60:
        return True, last_extracted_product
    return False, None
