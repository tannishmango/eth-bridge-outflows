from pkgs import anyswap
from pkgs import synapse
from pkgs.web3_tools.blocktime import get_block_time_multithread
from pkgs.web3_tools.prices import get_prices_multithread
from pkgs.web3_tools.erc20 import get_decimals_multithreader, get_symbols_multithreader
from pkgs.constants import NETWORK_ID_CHAIN_MAP
from datetime import datetime
import pandas as pd
import os


def get_all_eth_outflows(start_date, end_date=None):
    result_list = anyswap.get_outflow_events(start_date, end_date)
    result_list.extend(synapse.get_outflow_events(start_date, end_date))
    block_numbers = [x['block_number'] for x in result_list]
    block_times = get_block_time_multithread(block_numbers)
    for x in result_list:
        x['timestamp'] = block_times[x['block_number']]
    return result_list


def price_eth_outflows(outflow_list):
    tokens = [x['token'] for x in outflow_list]
    blocks = [x['block_number'] for x in outflow_list]
    result = get_prices_multithread(tokens,blocks)
    decimals = get_decimals_multithreader(tokens)
    symbols = get_symbols_multithreader(tokens)
    for i,price_row in enumerate(result):
        token = price_row[0].lower()
        price = price_row[2]
        outflow_list[i]['amount_usd'] = price * outflow_list[i]['amount']/10**decimals[token]
        outflow_list[i]['symbol'] = symbols[token]
    return outflow_list


def save_data(df):
    path = os.getcwd() + "/data/bridge_data.csv"
    df.to_csv(path,index=False)


def get_bridge_data(start_date):
    outflow_list = get_all_eth_outflows(start_date)
    outflow_list = price_eth_outflows(outflow_list)
    df = pd.DataFrame(outflow_list)
    df['date'] = df['timestamp'].apply(lambda x: datetime.utcfromtimestamp(x))
    df['to_chain'] = df['to_chain'].map(NETWORK_ID_CHAIN_MAP)
    save_data(df)
    print("bridge_data complete")
    return df

