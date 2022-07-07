from pkgs.web3_tools.config import get_web3

web3 = get_web3()

def init_contract(address,abi):
    addr = web3.toChecksumAddress(address)
    contract = web3.eth.contract(address=addr, abi=abi)
    return contract

def call_function(contract_address,abi,fx_name):
    contract = init_contract(contract_address,abi)
    return contract.functions[fx_name]().call()
