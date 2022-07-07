from web3._utils.filters import construct_event_filter_params
from pkgs.utils import flatten_list, run_multithreader
from typing import Iterable, List, Optional, Union
from eth_typing import BlockNumber, HexAddress
from pkgs.web3_tools.abis import get_topic_map
from web3.datastructures import AttributeDict
from web3._utils.events import get_event_data
from pkgs.web3_tools.config import get_web3
from eth_abi.codec import ABICodec
import json


def create_block_intervals(
        from_block: int,
        to_block: int = None,
        step: int = 10000,
        end_block: int = None):
    start_intervals = [from_block] + list(range(from_block+1,end_block,step))[1:]
    end_intervals = list(range(from_block,end_block,step))[1:]
    intervals = list(map(list,zip(start_intervals,end_intervals)))
    if not to_block:
        intervals.append([intervals[-1][-1]+1,None])
    else:
        intervals.append([intervals[-1][-1]+1,to_block])
    return intervals

def format_log_data(log):
    web3 = get_web3()
    result_log = {
        "address":log['address'].lower(),
        "block_number":log['blockNumber'],
        "log_index":log['logIndex'],
        "tx_hash":web3.toHex(log['transactionHash']),
        "tx_index":log['transactionIndex'],
        "data":dict(log['args'])
    }
    return result_log

def fetch_logs(event_filter_params):
    web3 = get_web3()
    logs = web3.eth.get_logs(event_filter_params)
    return logs

def fetch_logs_multithreader(filter_list):
    result_logs = flatten_list(run_multithreader(fetch_logs,filter_list))
    return result_logs

def build_log_filter_params(address, from_block, to_block, codec, argument_filters = None, topics = None, event_abi = None):
    if event_abi:
        data_filter_set, event_filter_params = construct_event_filter_params(
            event_abi,
            codec,
            address=address,
            argument_filters=argument_filters,
            topics=topics,
            fromBlock=from_block,
            toBlock=to_block
        )
    else:
        event_filter_params = {
            'address':address,
            'fromBlock':from_block,
            'toBlock':to_block,
        }
        if topics:
            event_filter_params['topics']=topics
    event_filter_params = {k:v for k,v in event_filter_params.items() if v}
    return event_filter_params

def get_logs(
        event_name: Optional[str] = None,
        abi:Optional[str]=None,
        address: Optional[Union[HexAddress,List[HexAddress]]] = None,
        argument_filters: Optional[dict] = None,
        topics: Optional[Union[List[str],List[List[str]]]] = None,
        from_block: Optional[BlockNumber] = None,
        to_block: Optional[BlockNumber] = None,
        step: int = 2048,
        formatted: bool = True ) -> Iterable[AttributeDict]:
    web3 = get_web3()
    event_abi = web3.eth.contract(abi=abi).events[event_name]._get_event_abi() if event_name else None
    codec: ABICodec = web3.codec
    if from_block is None:
        from_block = 1
    end_block = web3.eth.get_block_number() if to_block is None else to_block
    filter_list = []
    if end_block - from_block > step:
        block_intervals = create_block_intervals(from_block,to_block,step,end_block)
        for item in block_intervals:
            event_filter_params = build_log_filter_params(address,item[0],item[-1],codec,argument_filters,topics,event_abi)
            filter_list.append(event_filter_params)
        logs = fetch_logs_multithreader(filter_list)
    else:
        event_filter_params = build_log_filter_params(address,from_block,to_block,codec,argument_filters,topics,event_abi)
        logs = fetch_logs(event_filter_params)
    all_events = []
    if logs:
        if not event_name:
            topic_map = {k:v for k,v in get_topic_map(json.loads(abi)).items()} if topics else get_topic_map(json.loads(abi)).items()
            for log in logs:
                try:
                    event_abi = web3.eth.contract(abi=abi).events[topic_map[web3.toHex(log['topics'][0])]['name']]._get_event_abi()
                    evt = get_event_data(codec, event_abi, log)
                    all_events.append(evt)
                except:
                    pass
        else:
            for log in logs:
                try:
                    event_abi = web3.eth.contract(abi=abi).events[event_name]._get_event_abi()
                    evt = get_event_data(codec, event_abi, log)
                    all_events.append(evt)
                except:
                    pass
        if formatted:
            all_events = [format_log_data(x) for x in all_events]
    return all_events