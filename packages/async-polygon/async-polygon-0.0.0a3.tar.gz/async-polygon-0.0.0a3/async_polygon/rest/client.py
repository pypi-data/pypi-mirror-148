from typing import Union
from aiohttp import ClientResponse, ClientSession
import pandas as pd
from async_polygon.rest.dataclasses import pretty_json


class RestAsyncClient:

    POLY_BASIC: str = 'api.polygon.io'

    def __init__(self, auth_key: str) -> None:
        self.auth_key = auth_key
        self.url = 'https://' + self.POLY_BASIC
        self.session = Union[None, ClientSession]

    async def __aenter__(self):
        self.session = ClientSession()
        return self

    async def __aexit__(self, *args):
        await self.session.close()
    
    async def close(self):
        self.session.close()
    
    async def _handle_request(self, _reqName: str, _url_for_data: str):
        response: ClientResponse = await self.session.get(url=_url_for_data)
        if response.status == 200:
            response = await response.json()
            return pretty_json.to_pretty_json(_reqName, response)
        else:
            response.raise_for_status()

    async def aggregate_bars(
        self, ticker: str, multiplier: int, timespan: str, 
        _from: str, _to: str, adjusted: bool = True, sort: str = 'asc', limit: int = 50000) -> pd.DataFrame:
        """
    Get aggregate bars for a stock
    
    Args
    ----------
        tickers: str, list
            List of tickers to download.
        multiplier: int
            Valid multipliers: from 1 to 9999
            The size of the timespan multiplier. For example, if timespan = ‘minute’ and multiplier = ‘5’ then 5-minute bars will be returned.
            Default is 1
        timespan: str
            Valid timespans: minute, hour, day, week, month, quarter, year.
            The size of the time window.
            Defult is day
        start: str
            The start of the aggregate time window.
            Default is 2 years ago date
        end: str
            The end of the aggregate time window.
            Default is current date
        adjusted: None, bool
            Whether or not the results are adjusted for splits. By default, results are adjusted. Set this to false to get results that are NOT adjusted for splits.
        sort: str
            Sort the results by timestamp. asc will return results in ascending order (oldest at the top), desc will return results in descending order (newest at the top).
            Default is asc
        limit: int
            Limits the number of base aggregates queried to create the aggregate results. Max 50000 and Default 5000. Read more about how limit is used to calculate aggregate 
            results in our article on Aggregate Data API Improvements(https://polygon.io/blog/aggs-api-updates/)
    """

        url_for_req = f'{self.url}/v2/aggs/ticker/{ticker}/range/{multiplier}/{timespan}/{_from}/{_to}?adjusted={adjusted}&sort={sort}&limit={limit}&apiKey={self.auth_key}'
        aggregated = await self._handle_request('AggregateBars', url_for_req)
        return aggregated

    async def previous_close(self, ticker: str, adjusted: bool = True) -> pd.DataFrame:
        """Get the previous day's open, high, low, and close (OHLC) for the specified stock ticker.

        Args:
        -----
            ticker (str): The ticker symbol of the stock/equity.
            adjusted (bool, optional): Whether or not the results are adjusted for splits. By default, results are adjusted. 
                Set this to false to get results that are NOT adjusted for splits.. Defaults to True.

        Returns:
        --------
            _type_: _description_
        """

        url_for_req = f'{self.url}/v2/aggs/ticker/{ticker}/prev?adjusted={adjusted}&apikey={self.auth_key}'
        return await self._handle_request('PreviousClose', url_for_req)

    async def last_trade(self, ticker: str) -> pd.DataFrame:
        """Get the most recent trade for a given stock.

        Args:
        -----
            ticker (str)
        """

        url_for_req = f'{self.url}/v2/last/trade/{ticker}?apiKey={self.auth_key}'
        return await self._handle_request('LastTrade', url_for_req)
    
    async def crypt_previous_close(self, ticker: str, adjusted: bool = True) -> pd.DataFrame:
        """Get the previous day's open, high, low, and close (OHLC) for the specified cryptocurrency pair.

        Args:
        -----
            ticker (str): Input following format BTCUSD or BTC-USD, crypto with currency without separates
            adjusted (bool, optional): Whether or not the results are adjusted for splits. 
                By default, results are adjusted. Set this to false to get results that are NOT adjusted for splits.. Defaults to True.
        """
        if '-' in ticker:
            ticker = ticker.replace('-', '')
        url_for_req = f'{self.url}/v2/aggs/ticker/X:{ticker}/prev?adjusted={adjusted}&apiKey={self.auth_key}'
        return await self._handle_request('PreviousClose', url_for_req)