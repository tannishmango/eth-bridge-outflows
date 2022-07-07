from pkgs.web3_tools.abis import fetch_abi
from pkgs.web3_tools.config import get_web3
from pkgs.web3_tools.common import init_contract
from pkgs.utils import run_multithreader


ERC20_ABI = fetch_abi('erc20')

web3 = get_web3()


def get_decimals(contract_address):
    contract = init_contract(contract_address,ERC20_ABI)
    try:
        decimals = contract.functions.decimals().call()
    except Exception as e:
        print("decimals call failed for {}".format(contract_address))
        decimals = 18
    return decimals


def get_decimals_multithreader(contract_list):
    contract_list = list(set([x.lower() for x in contract_list]))
    result = run_multithreader(get_decimals,contract_list)
    return dict(zip(contract_list,result))


def get_symbol(contract_address):
    contract = init_contract(contract_address,ERC20_ABI)
    try:
        symbol = contract.functions.symbol().call()
    except Exception as e:
        print("symbol call failed for {}".format(contract_address))
        symbol = ''
    return symbol


def get_symbols_multithreader(contract_list):
    contract_list = list(set([x.lower() for x in contract_list]))
    result = run_multithreader(get_symbol,contract_list)
    return dict(zip(contract_list,result))