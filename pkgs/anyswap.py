from pkgs.constants import ANYSWAP_ROUTER_ADDRESS
from pkgs.web3_tools.contract_events import get_logs
from pkgs.web3_tools.abis import fetch_abi
from pkgs.web3_tools.blocktime import str_date_to_timestamp, get_block_from_timestamp
from pkgs.web3_tools.common import init_contract
from pkgs.utils import run_multithreader

ANYSWAP_ROUTER_ABI = fetch_abi(ANYSWAP_ROUTER_ADDRESS)
ANYSWAP_ERC20_ABI = fetch_abi("anyswapErc20")


def get_underlying(token_address):
    contract = init_contract(token_address,ANYSWAP_ERC20_ABI)
    return contract.functions.underlying().call()

def get_token_underlying(token_list):
    token_list = list(set(token_list))
    result = run_multithreader(get_underlying,token_list)
    return dict(zip(token_list,result))

def get_outflow_events(start_date,end_date = None):
    """
    :param start_date: str 2022-5-2
    :param end_date: optional: str 2022-5-5
    :return: synapse router withdrawal logs
    """
    start_date = str(start_date)
    end_date = str(end_date) if end_date else None
    start_timestamp = str_date_to_timestamp(start_date)
    end_timestamp = str_date_to_timestamp(end_date) if end_date else None
    start_block = get_block_from_timestamp(start_timestamp)
    end_block = get_block_from_timestamp(end_timestamp) if end_timestamp else None
    logs = get_logs("LogAnySwapOut",ANYSWAP_ROUTER_ABI,ANYSWAP_ROUTER_ADDRESS,from_block=start_block, to_block=end_block)
    result_list = [{
        "block_number":x['block_number'],
        "from":x["data"]["from"],
        "token":x["data"]["token"].lower(),
        "amount":x["data"]["amount"],
        "to_chain":x["data"]["toChainID"]
    } for x in logs]
    token_list = [x['token'] for x in result_list]
    underlyings = get_token_underlying(token_list)
    for x in result_list:
        x['token'] = underlyings[x['token']]
    return result_list

