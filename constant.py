HTML_COLLECTION = "product_web_html"
PRODUCT_COLLECTION = "product_details"

PROXY_SERVERS = ["103.250.158.21:6666", "194.163.132.232:3128", "43.224.8.12:6666"]

# Request Headers of the requests
REQUEST_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Referer": "",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 \
    Safari/537.36"
}

NULL_CONTAINER = [[], (), {}, "", 0]

# proxies in case if website is blocked for one server
PROXY_DIR = None
#     {
#     "https": PROXY_SERVERS[random.randint(0, len(PROXY_SERVERS) - 1)]
# }

FAILURE_RESPONSE = {"status_code": 400, "message": "Bad Request"}

SUCCESS_RESPONSE = {'status_code': 200, 'message': 'success'}

PATH_NOT_FOUND = {"status_code": 404, "message": "path not found"}

SERVER_ERROR = {"status_code": 500, "message": "server error"}
