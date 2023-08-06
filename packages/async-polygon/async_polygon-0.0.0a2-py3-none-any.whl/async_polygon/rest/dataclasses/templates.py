from typing import Dict, Union
import pandas as pd

class Template:

    _results: Union[str, None] = 'results'
    _keys_to_work: Dict[str, str]


    def make_pretty_json(self, resp_json: dict):
        if self._results is not None:
            _row_data = resp_json[self._results]
            if isinstance(_row_data, list):
                result = pd.DataFrame(resp_json[self._results])
                result = result.loc[:, self._keys_to_work].rename(columns={k:v for k,v in self._keys_to_work.items()})
            elif isinstance(_row_data, dict):
                #TODO tests
                _row_data = {k:v for k,v in _row_data.items() if k in self._keys_to_work.keys()}
                result = pd.DataFrame.from_dict(_row_data, orient='index').T
                result = result.loc[:, self._keys_to_work].rename(columns={k:v for k,v in self._keys_to_work.items()})
        return result


class AggregateBars(Template):

    _keys_to_work = {
        'c': 'Close',
        'h': 'High',
        'l': 'Low',
        'n': 'Transactions',
        'o': 'Open',
        't': 'Timestamp',
        'v': 'Volume',
        'vw': 'AVG_Price_Volume',
    }


class PreviousClose(Template):

    _keys_to_work = {
        'T': 'Ticker',
        'c': 'Close',
        'h': 'High',
        'l': 'Low',
        'o': 'Open',
        't': 'Timestamp',
        'v': 'Volume',
        'vw': 'AVG_Price_Volume',
    }


class LastTrade(Template):

    _keys_to_work = {
        'T': 'Ticker',
        'p': 'Price',
        's': 'Volume'
    }


class LastTradeCryptoPair(Template):

    _results = 'last'
    _keys_o_work = {
        'price': 'Price',
        'size': 'Volume',
        'timestamp': 'Timestamp',
    }