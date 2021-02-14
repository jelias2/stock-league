from flask import Blueprint, request
from flask.json import jsonify

from app.stocks.stocks import get_stock_ticker_details
from app.stocks.models import StocksDb


stocks_blueprint = Blueprint('stocks', __name__, url_prefix="/stocks")
stocks_db = StocksDb()


@stocks_blueprint.route("/add/<stock_ticker>", methods=["POST"])
def add_stock(stock_ticker: str):
    try:
        stock_ticker_details = get_stock_ticker_details(stock_ticker)
        # print(stock_ticker_details)
        status = stocks_db.insert(
                        stock_ticker,
                        stock_ticker_details
                    )
        return jsonify({"success": status}), 200
    except Exception as e:
        print(e)
        return jsonify({"failure": f"{stock_ticker} insertion failed"}), 400


@stocks_blueprint.route("/list", methods=["GET"])
def get_one_or_more_stocks():
    try:
        stock_ticker = request.args.get('ticker')
        if stock_ticker:
            # Always upsert first and return the latest stock data into the DB
            stock_ticker_details = get_stock_ticker_details(stock_ticker)
            status = stocks_db.insert(
                        stock_ticker,
                        stock_ticker_details
                    )
            return jsonify({stock_ticker: stocks_db.get(stock_ticker)}), 200
        return jsonify({"stocks": [stock for stock in stocks_db.get_all()]})
    except Exception as e:
        return jsonify({"failure": f"Internal Error Occurred"}), 500


def add_stock_to_portfolio():
    """
        Adds a stock to a user's portfolio
    """
    raise NotImplementedError()


def get_portfolio():
    """
        Get all the stocks in a user's portfolio
    """
    raise NotImplementedError()