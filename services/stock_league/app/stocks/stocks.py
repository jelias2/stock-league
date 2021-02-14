import yfinance as yf


class Stock:

    __slots__ = (
        'stock_ticker', 'stock_ticker_obj', 
        'period', 'interval'
    )

    def __init__(self, stock_ticker: str, period='1d', interval='5m') -> None:
        self.stock_ticker = stock_ticker
        self.stock_ticker_obj = yf.Ticker(stock_ticker)
        self.period = period
        self.interval = interval
        self._validate_price_period(self.period)
        self._validate_interval_period(self.interval)

    @staticmethod
    def _validate_price_period(period='1d'):

        if not isinstance(period, str):
            raise TypeError(f"'period' should a {str}")

        valid_price_periods = {
            '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y',
            '5y', '10y', 'ytd', 'max'
        }
        if period not in valid_price_periods:
            raise ValueError(
                ' '.join(
                    f"Invalid input - period={period} is not supported."
                    f"Valid intervals: {list(valid_price_periods)}"
                )
            )

    @staticmethod
    def _validate_interval_period(interval='5m'):

        if not isinstance(interval, str):
            raise TypeError(f"'interval' should a {str}")

        valid_price_intervals = {
            '1m', '2m', '5m', '15m', '30m', '60m', '90m', 
            '1h', '1d', '5d', '1wk', '1mo', '3mo'
        }
        if interval not in valid_price_intervals:
            raise ValueError(
                ' '.join(
                    f"Invalid input - period={interval} is not supported."
                    f"Valid intervals: {list(valid_price_intervals)}"
                )
            )

    @staticmethod
    def _validate_price_type(price_type="Close"):

        if not isinstance(price_type, str):
            raise TypeError(f"'price_type' should a {str}")

        valid_price_types = {
            "Open", "Close",
            "High", "Low"
        }
        if price_type not in valid_price_types:
            raise ValueError(
                ' '.join(
                    f"price_type={price_type} is not supported."
                    f"Valid intervals: {list(valid_price_types)}"
                )
            )

    # @lru_cache(maxsize=128, typed=True)
    def _fetch_stock_history(self, period='1d', interval='1m'):
        return self.stock_ticker_obj.history(
            period=period,
            interval=interval
        )

    def _get_price(self, price_type='Close') -> float:

        self._validate_price_type(price_type)

        # TODO: Memoize the call to `self.stock_ticker_obj.history` function
        # using a TTL (Time-To-Live) expiration set to self.interval.
        # Make sure to profiling the _get_price method before caching the method call
        df = self._fetch_stock_history(self.period, self.interval)
        return round(df[price_type][-1], 2)

    def get_percentage_daily_change(self):
        df = self._fetch_stock_history(self.period, self.interval)
        morning_open_price = round(df['Open'][0], 2)
        evening_closing_price = round(df['Close'][-1], 2)
        daily_percent_change = (evening_closing_price - morning_open_price) / morning_open_price
        return round(daily_percent_change, 5) * 100

    def get_closing_price(self):
        return self._get_price('Close').item()

    def get_opening_price(self):
        return self._get_price('Open').item()
    
    def get_lowest_price(self):
        return self._get_price('Low').item()

    def get_highest_price(self):
        return self._get_price('High').item()

    def get_trading_volume(self):
        df = self._fetch_stock_history(self.period, self.interval)
        return df['Volume'][-1].item()


# TODO: Apply LRU Caching of result for this method
def get_stock_ticker_details(stock_ticker=None, period='1d', interval='1m'):
    # TODO: Validate if the stock_ticker is valid
    # TODO: Make a request to an external API about a stock ticker details
    stock = Stock(stock_ticker)
    open = stock.get_opening_price()
    close = stock.get_closing_price()
    high = stock.get_highest_price()
    low = stock.get_lowest_price()
    trading_volume = stock.get_trading_volume()
    daily_percent_change = stock.get_percentage_daily_change()

    return {
        "close": close,
        "open": open,
        "high": high,
        "low": low,
        "volume": trading_volume,
        "daily_percentage_change": daily_percent_change
    }
