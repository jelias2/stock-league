from flask import Flask
from os import environ


# from .dummy.routes import routes_blueprint
from .stocks.views import stocks_blueprint


app = Flask(__name__)
app.url_map.strict_slashes = False

# Register Endpoints (Views)
# app.register_blueprint(routes_blueprint)
app.register_blueprint(stocks_blueprint)


flask_port = int(environ.get("FLASK_PORT", 8080))
if __name__=='__main__':
    app.run(threaded=True, host="0.0.0.0", port=flask_port, debug=True)