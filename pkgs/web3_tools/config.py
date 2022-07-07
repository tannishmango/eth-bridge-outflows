from web3 import Web3
import os

def set_rpc_url():
    key_value = input("Enter the RPC URL:")
    os.environ.setdefault('RPC_URL', key_value)
    print("RPC {} set".format(key_value))

def get_rpc_url():
    rpc_url = os.environ.get('RPC_URL')
    if not rpc_url:
        set_rpc_url()
    return os.environ.get('RPC_URL')

def set_etherscan_api_key():
    key_value = input("Enter the ETHERSCAN API KEY:")
    os.environ.setdefault('ETHERSCAN', key_value)
    print("ETHERSCAN {} set".format(key_value))

def get_etherscan_api_key():
    etherscan_key = os.environ.get('RPC_URL')
    if not etherscan_key:
        key_value = input("Enter the ETHERSCAN API KEY:")
        os.environ.setdefault('ETHERSCAN', key_value)
        print("ETHERSCAN API KEY {} set".format(key_value))
    return os.environ.get('ETHERSCAN')

def get_web3():
    rpc_url = get_rpc_url()
    web3 = Web3(Web3.HTTPProvider(rpc_url,request_kwargs={'timeout': 1800000}))
    #if network in [Network.BSC,Network.Polygon,Network.Avalanche]:
    #    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3



