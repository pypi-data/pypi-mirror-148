# async-polygon
This is an unofficial asynchronous version of [Official Polygon Api(REST API)](https://github.com/polygon-io/client-python)
---
# **Getting Started**

## Client example
```
import asyncio
from async_polygon import RestAsyncClient


async def main():
    api_key = 'API KEY'
    async with RestAsyncClient(api_key) as requestor:
        requestor: RestAsyncClient
        _from: str = '2022-03-29'
        _to: str = '2022-04-26'
        _timespan: str = 'hour'
        data = await requestor.aggregate_bars('AAPL', 1, _timespan, _from, _to)
        
        print(data)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

In near future I'll expand the functionality of the library
