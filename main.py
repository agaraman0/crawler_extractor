from flask import Flask, jsonify, make_response

from crawler_extractor.routes import crawl_extract
from constant import PATH_NOT_FOUND, SERVER_ERROR, FAILURE_RESPONSE

app = Flask(__name__)
app.register_blueprint(crawl_extract)


@app.errorhandler(400)
def handle_400_error(_error):
    """Return a http 400 error to client"""
    return make_response(jsonify(FAILURE_RESPONSE), 400)


@app.errorhandler(404)
def handle_404_error(_error):
    """Return a http 404 error to client"""
    return make_response(jsonify(PATH_NOT_FOUND), 404)


@app.errorhandler(500)
def handle_500_error(_error):
    """Return a http 500 error to client"""
    return make_response(jsonify(SERVER_ERROR), 500)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app.run(port=5000, debug=True)
