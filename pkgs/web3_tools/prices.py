from pkgs.constants import UNISWAP_ROUTER_ADDRESS, SUSHISWAP_ROUTER_ADDRESS, USDC, WETH, SUSHI, STABLECOINS
from pkgs.web3_tools.config import get_web3
from pkgs.web3_tools.erc20 import get_decimals
from pkgs.web3_tools.abis import fetch_abi
from pkgs.utils import run_multithreader
from pkgs.web3_tools.common import init_contract

ROUTER_ABI = fetch_abi(UNISWAP_ROUTER_ADDRESS)

web3 = get_web3()

ROUTERS = {"uniswap":UNISWAP_ROUTER_ADDRESS, "sushiswap":SUSHISWAP_ROUTER_ADDRESS}

SPECIAL_PATHS = {'sushi': {'0x6102407f07029892eb5ff02164adfafb85f4d222': ['0x6102407f07029892eb5ff02164adfafb85f4d222', '0xdac17f958d2ee523a2206206994597c13d831ec7'],
                           '0x85034b3b2e292493d029443455cc62ab669573b3': ['0x85034b3b2e292493d029443455cc62ab669573b3', '0x1f9840a85d5af5bf1d1762f925bdaddc4201f984', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'],
                           '0xb220d53f7d0f52897bcf25e47c4c3dc0bac344f8': ['0xb220d53f7d0f52897bcf25e47c4c3dc0bac344f8', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'],
                           '0x383518188c0c6d7730d91b2c03a03c837814a899': ['0x383518188c0c6d7730d91b2c03a03c837814a899', '0x6b175474e89094c44da98b954eedeac495271d0f'],
                           '0xafce9b78d409bf74980cacf610afb851bf02f257': ['0xafce9b78d409bf74980cacf610afb851bf02f257', '0x2260fac5e5542a773aa44fbcfedf7c193bc2c599', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'],
                           '0x62b9c7356a2dc64a1969e19c23e4f579f9810aa7': ['0x62b9c7356a2dc64a1969e19c23e4f579f9810aa7', '0xd533a949740bb3306d119cc777fa900ba034cd52', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'],
                           '0xef69b5697f2fb0345cc680210fd39b593a2f9684': ['0xef69b5697f2fb0345cc680210fd39b593a2f9684', '0x6b3595068778dd592e39a122f4f5a5cf09c90fe2', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'],
                           '0xbf2179859fc6d5bee9bf9158632dc51678a4100e': ['0xbf2179859fc6d5bee9bf9158632dc51678a4100e', '0xc28e27870558cf22add83540d2126da2e4b464c2', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'],
                           '0x3166c570935a7d8554c8f4ea792ff965d2efe1f2': ['0x3166c570935a7d8554c8f4ea792ff965d2efe1f2', '0x4954db6391f4feb5468b6b943d4935353596aec9', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'],
                           '0xe6279e1c65dd41b30ba3760dcac3cd8bbb4420d6': ['0xe6279e1c65dd41b30ba3760dcac3cd8bbb4420d6', '0x87f5f9ebe40786d49d35e1b5997b07ccaa8adbff', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'],
                           '0x4954db6391f4feb5468b6b943d4935353596aec9': ['0x4954db6391f4feb5468b6b943d4935353596aec9', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'],
                           '0x1e18821e69b9faa8e6e75dffe54e7e25754beda0': ['0x1e18821e69b9faa8e6e75dffe54e7e25754beda0', '0xef69b5697f2fb0345cc680210fd39b593a2f9684', '0x6b3595068778dd592e39a122f4f5a5cf09c90fe2', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'],
                           '0xfc1e690f61efd961294b3e1ce3313fbd8aa4f85d': ['0xfc1e690f61efd961294b3e1ce3313fbd8aa4f85d', '0xba100000625a3754423978a60c9317c58a424e3d', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'],
                           '0xba50933c268f567bdc86e1ac131be072c6b0b71a': ['0xba50933c268f567bdc86e1ac131be072c6b0b71a', '0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2', '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48']},
                 'uniswap': {},
                 }

def get_amounts_out(router,amount_in,path,block):
    path = [web3.toChecksumAddress(x) for x in path]
    router_contract = init_contract(router,ROUTER_ABI)
    quote = router_contract.functions.getAmountsOut(amount_in, path).call(block_identifier=block)
    return quote


def get_price_from_uniswap(token_in, token_out=USDC, router="uniswap", block='latest', paired_against=WETH):
    """
    Calculate a price based on Uniswap Router quote for selling one `token_in`.
    Always uses intermediate WETH pair if `[token_in,weth,token_out]` swap path available.
    """
    token_in = token_in.lower()
    tokens = [str(token) for token in [token_in, token_out]]
    amount_in = 10 ** get_decimals(tokens[0])
    if str(token_in) in STABLECOINS:
        return 1
    elif str(paired_against) in STABLECOINS and str(token_out) in STABLECOINS:
        path = [token_in, paired_against]
    elif WETH in (token_in, token_out):
        path = [token_in, token_out]
    elif paired_against == SUSHI and token_out != SUSHI:
        path = [token_in,SUSHI,WETH,token_out]
    elif str(token_in) in SPECIAL_PATHS[router].keys() and str(token_out) in STABLECOINS:
        path = SPECIAL_PATHS[router][str(token_in)]
    else:
        path = [token_in, paired_against, token_out]
    fees = 0.997 ** (len(path) - 1)
    if router in ROUTERS:
        router = ROUTERS[router]
    try:
        quote = get_amounts_out(router,amount_in,path,block)
        amount_out = quote[-1] / 10 ** get_decimals(str(path[-1]))
        return amount_out / fees
    except ValueError as e:
        return 0

def get_prices(token,block):
    return get_price_from_uniswap(token,block=block)


def get_prices_multithread(contract_list,block_list):
    prices = run_multithreader(get_prices,contract_list,block_list)
    return list(zip(contract_list,block_list,prices))