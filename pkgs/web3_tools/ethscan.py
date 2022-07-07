from etherscan import Etherscan
from pkgs.web3_tools.config import get_etherscan_api_key

api_key = str(get_etherscan_api_key())
eth = Etherscan(api_key)


def get_abi(contract_address):

    return eth.get_contract_abi(contract_address)