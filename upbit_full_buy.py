import pyupbit
import ccxt

access_upbit = "Xyhp80U4xbUkOoSCStKPZS4qsZxdmontflOxuCuv"
secret_upbit = "e2xSzgw8p78ruXVLCIUGFPbovmwZxxrmDixPqSrY"

access_binance = 'P2tMl6D9ecFV6qdWoMj204w9ILbAoCjxvvQgjiShYXi3KND0IEuaBRRGalq04ZeV'
secret_binance = 'bHESyrqCNgBqDv5uzNe8hzxNJNd1PEXoAlN9EMpBgKoRvk9xIDG3pdECvpby5vdX'

binance = ccxt.binance({
    'apiKey': access_binance,
    'secret': secret_binance,
})

upbit = pyupbit.Upbit(access_upbit, secret_upbit)

print("Start!")

# 시세 조회
while True :
    coin_binance = binance.fetch_ticker("BTC/USDT")
    price_coin_binance = float(coin_binance['info']['lastPrice'])
    print(price_coin_binance)
    if price_coin_binance <= 42000 :
        upbit.buy_market_order("KRW-LINK", 1500000)
        upbit.buy_market_order("KRW-ETC", 1500000)
        break

print("End!")




