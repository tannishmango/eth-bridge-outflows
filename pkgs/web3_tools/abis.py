from eth_hash.auto import keccak
from typing import List, Dict
from pkgs.web3_tools.ethscan import get_abi
from pkgs.utils import read_json_file, write_json_file
import json
import re
import os

ABI_FILE_PATH = os.getcwd()
ABI_FILE_PATH = ABI_FILE_PATH.split("pkgs/")[0] + "/pkgs/abis/"

class ABIError(Exception):
    pass


def _params(abi_params: List) -> List:
    types = []
    # regex with 2 capturing groups
    # first group captures whether this is an array tuple
    # second group captures the size if this is a fixed size tuple
    pattern = re.compile(r"tuple(\[(\d*)\])?")
    for i in abi_params:
        tuple_match = pattern.match(i["type"])
        if tuple_match:
            _array, _size = tuple_match.group(1, 2)  # unpack the captured info
            tuple_type_tail = f"[{_size}]" if _array is not None else ""
            types.append(f"({','.join(x for x in _params(i['components']))}){tuple_type_tail}")
            continue
        types.append(i["type"])

    return types


def get_log_topic(event_abi: Dict) -> str:
    """
    Generate an encoded event topic for an event.
    Arguments
    ---------
    event_abi : Dict
        Dictionary from a contract ABI, describing a specific event.
    Returns
    -------
    str
        bytes32 encoded topic for the event.
    """
    if not isinstance(event_abi, dict):
        raise TypeError("Must be a dictionary of the specific event's ABI")
    if event_abi.get("anonymous"):
        raise ABIError("Anonymous events do not have a topic")

    types = _params(event_abi["inputs"])
    key = f"{event_abi['name']}({','.join(types)})".encode()

    return "0x" + keccak(key).hex()


def get_topic_map(abi: List) -> Dict:
    """
    Generate a dictionary of event topics from an ABI.
    This dictionary is required by `decode_log`, `decode_logs`, and
    `decode_traceTransaction`.
    Anonymous events are ignored. The return data is formatted as follows:
        {
            'encoded bytes32 topic': {
                'name':"Event Name",
                'inputs': [abi inputs]
            }
        }
    Arguments
    ---------
    abi : List
        Contract ABI
    Returns
    -------
    Dict
        Mapping of contract events.
    """
    try:
        events = [i for i in abi if i["type"] == "event" and not i.get("anonymous")]
        return {get_log_topic(i): {"name": i["name"], "inputs": i["inputs"]} for i in events}

    except (KeyError, TypeError):
        raise ABIError("Invalid ABI")



def fetch_abi(contract_address: str):
    abi_path = ABI_FILE_PATH + contract_address.lower() + ".json"
    try:
        abi = read_json_file(abi_path)
        abi = json.dumps(abi)
    except FileNotFoundError:
        abi = get_abi(contract_address)
        write_json_file(abi_path,abi)
    return abi

