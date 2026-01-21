# Serve webpage
import flask

server = flask.Flask(__name__)

@server.route('/<path:path>')
def serve_page(path):
    return 