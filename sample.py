import asyncio
from pywebio.input import file_upload
from pywebio.output import put_html, put_loading, put_table, put_markdown, use_scope
from pywebio import start_server, config
from pywebio.session import defer_call, run_js, info as session_info
import time
import redis

redis_client = redis.Redis(host='localhost', port=6379, db=0)

@config(theme="dark")
async def app():
    put_markdown("## VVS VS crypto.com")
    await show_spread()

async def show_spread():
    while True:
        with use_scope('spread', clear=True):  # enter the existing scope and clear the previous content
            put_table(get_spreads())
        await asyncio.sleep(3)

def get_spreads():
    spreads = [['VVS Buy', 'VVS Sell', 'Crypto Price', 'Diff', 'Action']]
    for currency in ["CRO", "WBTC", "ETH"]:
        spread = redis_client.get(currency)
        if spread:
            spreads.append(spread.decode('UTF-8').split('-'))
    return spreads

if __name__=='__main__':
    start_server(app, port=37791, debug=True)