from enum import IntEnum

#############
## ANYSWAP ##
#############

ANYSWAP_ROUTER_ADDRESS = "0x6b7a87899490EcE95443e979cA9485CBE7E71522"


#############
## SYNAPSE ##
#############

SYNAPSE_ROUTER_ADDRESS = "0x2796317b0fF8538F253012862c06787Adfb8cEb6"

SYNAPSE_BRIDGE_URL = 'https://syn-explorer-api.metagabbar.xyz'


#############
## UNISWAP ##
#############

UNISWAP_ROUTER_ADDRESS = "0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D"


###############
## SUSHISWAP ##
###############

SUSHISWAP_ROUTER_ADDRESS = "0xD9E1CE17F2641F24AE83637AB66A2CCA9C378B9F"


##########
## MISC ##
##########


USDC = "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48".lower()
USDT = "0xdAC17F958D2ee523a2206206994597C13D831ec7".lower()
DAI = "0x6B175474E89094C44Da98b954EedeAC495271d0F".lower()
MIM = "0x99D8a9C45b2ecA8864373A26D1459e3Dff1e17F3".lower()
NUSD = "0x1B84765dE8B7566e4cEAF4D0fD3c5aF52D3DdE4F".lower()
WETH = "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2".lower()
SUSHI = "0x6b3595068778dd592e39a122f4f5a5cf09c90fe2".lower()
STABLECOINS = [USDC, USDT, DAI, MIM, NUSD]


##########
## MISC ##
##########

class Network(IntEnum):
    Arbitrum = 42161
    Aurora = 1313161554
    Avalanche = 43114
    Bittorrent = 199
    Boba = 288
    BSC = 56
    Cronos = 25
    DFK = 53935
    EOS = 59
    Fantom = 250
    Görli = 5
    Harmony = 1666600000
    Heco = 128
    IoTex = 4689
    Kcc = 321
    Kovan = 42
    Mainnet = 1
    Metis = 1088
    Moonbeam = 1284
    Moonriver = 1285
    RSK = 30
    Rinkeby = 4
    Okex = 66
    Optimism = 10
    Polygon = 137
    xDai = 100

CHAIN_NETWORK_MAP = {
    'arbitrum':Network.Arbitrum,
    'aurora':Network.Aurora,
    'avax':Network.Avalanche,
    'bittorrent':Network.Bittorrent,
    'boba':Network.Boba,
    'bsc':Network.BSC,
    'cronos':Network.Cronos,
    'defi kingdoms':Network.DFK,
    'eth':Network.Mainnet,
    'eos':Network.EOS,
    'ftm':Network.Fantom,
    'heco':Network.Heco,
    'harmony':Network.Harmony,
    'iotex':Network.IoTex,
    'kucoin':Network.Kcc,
    'matic':Network.Polygon,
    'metis':Network.Metis,
    'moonbeam':Network.Moonbeam,
    'moonriver':Network.Moonriver,
    'okex':Network.Okex,
    'optimism':Network.Optimism,
    'rsk':Network.RSK,
    'xdai':Network.xDai,
}

NETWORK_ID_CHAIN_MAP = {id:chain for chain,id in CHAIN_NETWORK_MAP.items()}