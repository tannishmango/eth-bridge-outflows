from pkgs.constants import SYNAPSE_ROUTER_ADDRESS
from pkgs.web3_tools.contract_events import get_logs
from pkgs.web3_tools.abis import fetch_abi
from pkgs.web3_tools.blocktime import str_date_to_timestamp, get_block_from_timestamp

SYNAPSE_ROUTER_ABI = fetch_abi(SYNAPSE_ROUTER_ADDRESS)

def get_withdrawals(start_date,end_date = None):
    """
    :param start_date: str 2022-5-2
    :param end_date: optional: str 2022-5-5
    :return: synapse router withdrawal logs
    """
    start_timestamp = str_date_to_timestamp(start_date)
    end_timestamp = str_date_to_timestamp(end_date) if end_date else None
    start_block = get_block_from_timestamp(start_timestamp)
    end_block = get_block_from_timestamp(end_timestamp) if end_timestamp else None
    logs = get_logs("TokenWithdraw",SYNAPSE_ROUTER_ABI,SYNAPSE_ROUTER_ADDRESS,from_block=start_block, to_block=end_block)
    return logs


def get_outflow_events(start_date,end_date = None):
    """
    :param start_date: str 2022-5-2
    :param end_date: optional: str 2022-5-5
    :return: synapse router withdrawal logs
    """
    start_timestamp = str_date_to_timestamp(start_date)
    end_timestamp = str_date_to_timestamp(end_date) if end_date else None
    start_block = get_block_from_timestamp(start_timestamp)
    end_block = get_block_from_timestamp(end_timestamp) if end_timestamp else None
    logs = get_logs("TokenDepositAndSwap",SYNAPSE_ROUTER_ABI,SYNAPSE_ROUTER_ADDRESS,from_block=start_block, to_block=end_block)
    result_list = [{
        "block_number":x['block_number'],
        "from":x["data"]["to"],
        "token":x["data"]["token"],
        "amount":x["data"]["amount"],
        "to_chain":x["data"]["chainId"]
    } for x in logs]
    return result_list



logs = get_outflow_events("2022-7-4")
