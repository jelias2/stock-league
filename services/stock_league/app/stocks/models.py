from os.path import dirname, realpath
from typing import Dict
from os.path import realpath, dirname

import firebase_admin
from firebase_admin import credentials, firestore, initialize_app


if not firebase_admin._apps:
    dir_path = dirname(dirname(realpath(__file__)))
    cred = credentials.Certificate(f"{dir_path}/firebase_credentials/service_account_key.json")
    firebase_app = initialize_app(cred)


db = firestore.client()


class StocksDb:

    """
        {
            "stock_ticker": String,
            "open": Float,
            "close": Float,
            "high": Float,
            "low": Float,
            "trading_volume": Int,
            "daily_percent_change": Float
        }
    """

    __slots__ = ('client', 'collection')

    def __init__(self) -> None:
        self.client = firestore.client()
        self.collection = self.client.collection("stocks")

    @staticmethod
    def _validate_data_model(data: Dict) -> bool:
        return True

    def get_all(self):
        for doc in self.collection.stream():
            yield {
                doc.id: doc.to_dict()
            }

    def get(self, stock_ticker):
        try:
            doc_ref = self.collection.document(stock_ticker)
            if doc_ref:
                return doc_ref.get().to_dict()
        # TODO: Create Granular Exceptions
        except Exception as e:
            raise Exception(f"{e}")

    def insert(self, stock_ticker, doc):

        if not self._validate_data_model(doc):
            raise TypeError(f"{doc} is invalid")

        try:
            doc_ref = self.collection.document(stock_ticker)
            status = ""
            if doc_ref.get().exists:
                status = self.update(stock_ticker, doc)
            else:
                doc_ref.set(doc)
                status = f"{stock_ticker} inserted"
            return status
        # TODO: Create Granular Exceptions
        except Exception as e:
            raise Exception(f"{e}")

    def update(self, stock_ticker, doc):

        if not self._validate_data_model(doc):
            raise TypeError(f"{doc} is invalid")

        try:
            doc_ref = self.collection.document(stock_ticker)
            if doc_ref:
                doc_ref.update(doc)
                return f"{stock_ticker} updated"
            raise ValueError(f"{stock_ticker} is not available")
        # TODO: Create Granular Exceptions
        except Exception as e:
            raise Exception(f"{e}")

    def delete(self, stock_price):
        pass


class PortfolioDb:
    
    """
        {
            "stock_count": Int,
            "stock_ticker": String,
            "user_id": Int,
            "purchase_price": Float,
            "current_price": Float,
        }
    """

    __slots__ = ('client', 'db')

    def __init__(self) -> None:
        self.client = firestore.client()
        self.db = self.client.collection('portfolio')
    