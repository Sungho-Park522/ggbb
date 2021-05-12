import time
import pyupbit
import datetime
import ccxt
import pprint
import pandas as pd
import requests
 
# def post_message(token, channel, text):
#     response = requests.post("https://slack.com/api/chat.postMessage",
#         headers={"Authorization": "Bearer "+token},
#         data={"channel": channel,"text": text}
#     )
#     print(response)
 
# myToken = "xoxb-2058296221329-2045897155603-prnOBZh7Y9UmIVqzfhxC5OuU"
 
# post_message(myToken,"#kimauto","dd")

# MINE
access_upbit = "Xyhp80U4xbUkOoSCStKPZS4qsZxdmontflOxuCuv"
secret_upbit = "e2xSzgw8p78ruXVLCIUGFPbovmwZxxrmDixPqSrY"

access_binance = 'P2tMl6D9ecFV6qdWoMj204w9ILbAoCjxvvQgjiShYXi3KND0IEuaBRRGalq04ZeV'
secret_binance = 'bHESyrqCNgBqDv5uzNe8hzxNJNd1PEXoAlN9EMpBgKoRvk9xIDG3pdECvpby5vdX'

binance = ccxt.binance({
    'apiKey': access_binance,
    'secret': secret_binance,
})
# binance.verbose = True
# balance = binance.fetch_balance({'recvWindow': 10000000})
# binance.nonce = lambda: binance.milliseconds() - 1000  # this line is only needed once in the beginning of your program
# all_balance = binance.fetch_balance()

upbit = pyupbit.Upbit(access_upbit, secret_upbit)

print("autotrade start")

base_price = 1125.5

# 건들지 말 것
enter_kimp = 0
end_kimp = 0
changed_end_kimp = 0

enter_kimp_gap_with_btc = 0.01
end_kimp_gap_with_btc = 0.01

current_state = 0

# input coin name that want to trade
trade_coin = ["DOGE","ETH","ETC", "XRP","EOS","XLM","TRX","QTUM"]

current_trading_coin = 0


coin_name_upbit = []
coin_name_binance = []
coin_name_binance_leverage = []
count_coin_number = 0
while count_coin_number < len(trade_coin):
    coin_name_upbit.append("KRW-" + trade_coin[count_coin_number])
    coin_name_binance.append(trade_coin[count_coin_number] + "/USDT")
    coin_name_binance_leverage.append(trade_coin[count_coin_number] + "USDT")
    count_coin_number = count_coin_number + 1

while True:
    try:
        order_tf_binance = True
        order_tf_upbit = True
        
        count_coin_number_2 = 0
        count_coin_number_3 = 0
        count_coin_number_4 = 0
        coin_binance = []
        price_coin_binance = []
        price_coin_upbit = []
        cal_kimp = []


        # 거래할 코인들 시세 조회
        while count_coin_number_2 < len(trade_coin):
            coin_binance.append(binance.fetch_ticker(coin_name_binance[count_coin_number_2]))
            price_coin_binance.append(coin_binance[count_coin_number_2]['info']['lastPrice'])
            price_coin_upbit.append(float(pyupbit.get_current_price(coin_name_upbit[count_coin_number_2])))
            count_coin_number_2 =  count_coin_number_2 + 1
        
        # 비트코인 시세 조회
        btc_binance = binance.fetch_ticker("BTC/USDT")
        price_btc_binance = float(btc_binance['info']['lastPrice'])
        price_btc_upbit = float(pyupbit.get_current_price("KRW-BTC"))

        # 잔고 조회
        # balance_binance = binance.fetch_balance(params={'type': 'future'})
        # current_balance_binance = float(balance_binance['USDT']['free'])
        # current_balance_upbit = float(upbit.get_balance(ticker="KRW"))

        # etc_binance = binance.fetch_ticker(coin_name_binance)
        # price_coin_binance = float(etc_binance['info']['lastPrice'])
        # price_etc_upbit = float(pyupbit.get_current_price(coin_name_upbit))
        
        # 현재 진입 전인지 후인지 판단
        # if current_balance_binance < 10 :
        #     current_state = 1

        # 거래코인 김프 계산
        while count_coin_number_3 < len(trade_coin) :
            cal_kimp.append((float(price_coin_upbit[count_coin_number_3])-float(price_coin_binance[count_coin_number_3])*base_price)/(float(price_coin_binance[count_coin_number_3])*base_price))
            print(trade_coin[count_coin_number_3] + " : " + str(round(cal_kimp[count_coin_number_3], 5)*100) + "%")
            count_coin_number_3 = count_coin_number_3 + 1
        
        # 비트코인 김프 계산
        cal_kimp_btc = (price_btc_upbit-price_btc_binance*base_price)/(price_btc_binance*base_price)
        print("BTC : " + str(round(cal_kimp_btc,5)*100) + "%")

        enter_kimp = cal_kimp_btc - enter_kimp_gap_with_btc
        # changed_end_kimp = cal_kimp + end_kimp_gap_with_btc

        while count_coin_number_4 < len(trade_coin):
            if cal_kimp[count_coin_number_4] <= enter_kimp and current_state==0:
                balance_binance = binance.fetch_balance(params={'type': 'future'})
                current_balance_binance = float(balance_binance['USDT']['free'])
                current_balance_upbit = float(upbit.get_balance(ticker="KRW"))
                order_number_binance = round((current_balance_binance-0)/float(price_coin_binance[count_coin_number_4]))
                binance.fapiPrivate_post_leverage({
                    "symbol": coin_name_binance_leverage[count_coin_number_4],
                    "leverage": 1,
                    })
                order_info_binance = binance.create_market_sell_order(
                symbol=coin_name_binance[count_coin_number_4], 
                amount=order_number_binance,
                params={'type': 'future'}
                )
                while order_tf_binance :
                    if order_info_binance['status']!='open' :
                        order_tf_binance=False
                
                enter_price_binance = float(order_info_binance['info']['avgPrice'])
                enter_number_binance = float(order_info_binance['info']['origQty'])
                order_number_upbit = enter_price_binance * enter_number_binance * base_price
                
                upbit.buy_market_order(coin_name_upbit[count_coin_number_4], order_number_upbit)
                while order_tf_upbit :
                    enter_number_upbit = upbit.get_balance(ticker=coin_name_upbit[count_coin_number_4])
                    if enter_number_upbit !=0 :
                        order_tf_upbit=False
                        current_state=1
                print("Enter!")
                
                buy_price_total = order_number_upbit * 2
                real_enter_kimp = round(((order_number_upbit/enter_number_upbit)-(enter_price_binance*base_price))/(enter_price_binance*base_price),2)

                # post_message(myToken,"#kimauto","enter kimp:" + str(float(real_enter_kimp)*100) + "%\nTotal buy price:" + str(buy_price_total) + "KRW")

                order_tf_binance = True
                order_tf_upbit = True
                end_kimp = cal_kimp_btc + end_kimp_gap_with_btc
                current_trading_coin = count_coin_number_4
            
            elif cal_kimp[count_coin_number_4] <=0.06:
                balance_binance = binance.fetch_balance(params={'type': 'future'})
                current_balance_binance = float(balance_binance['USDT']['free'])
                current_balance_upbit = float(upbit.get_balance(ticker="KRW"))
                order_number_binance = round((current_balance_binance-0)/float(price_coin_binance[count_coin_number_4]))
                binance.fapiPrivate_post_leverage({
                    "symbol": coin_name_binance_leverage[count_coin_number_4],
                    "leverage": 1,
                    })
                order_info_binance = binance.create_market_sell_order(
                symbol=coin_name_binance[count_coin_number_4], 
                amount=order_number_binance,
                params={'type': 'future'}
                )
                while order_tf_binance :
                    if order_info_binance['status']!='open' :
                        order_tf_binance=False
                
                enter_price_binance = float(order_info_binance['info']['avgPrice'])
                enter_number_binance = float(order_info_binance['info']['origQty'])
                order_number_upbit = enter_price_binance * enter_number_binance * base_price
                
                upbit.buy_market_order(coin_name_upbit[count_coin_number_4], order_number_upbit)
                while order_tf_upbit :
                    enter_number_upbit = upbit.get_balance(ticker=coin_name_upbit[count_coin_number_4])
                    if enter_number_upbit !=0 :
                        order_tf_upbit=False
                        current_state=1
                print("Enter!")
                
                buy_price_total = order_number_upbit * 2
                real_enter_kimp = round(((order_number_upbit/enter_number_upbit)-(enter_price_binance*base_price))/(enter_price_binance*base_price),2)

                # post_message(myToken,"#kimauto","enter kimp:" + str(float(real_enter_kimp)*100) + "%\nTotal buy price:" + str(buy_price_total) + "KRW")

                order_tf_binance = True
                order_tf_upbit = True
                end_kimp = 12
                current_trading_coin = count_coin_number_4
                
            elif cal_kimp[current_trading_coin] >= end_kimp and current_state==1 :
                binance.create_market_buy_order(
                    symbol=coin_name_binance[current_trading_coin],
                    amount=enter_number_binance,
                    params={'type': 'future'}
                    )
                while order_tf_binance :
                    if order_info_binance['status']!='open' :
                        order_tf_binance = False
                upbit.sell_market_order(coin_name_upbit[current_trading_coin],enter_number_upbit)
                while order_tf_upbit :
                    etc_number_upbit = upbit.get_balance(ticker=coin_name_upbit)
                    if etc_number_upbit == 0 :
                        order_tf_upbit = False
                        current_state=0
                print("End!")
                balance_binance = binance.fetch_balance(params={'type': 'future'})
                after_balance_binance = float(balance_binance['USDT']['free'])
                after_balance_upbit = float(upbit.get_balance(ticker="KRW"))
                profit_binance = (after_balance_binance-current_balance_binance)*base_price
                profit_upbit = (after_balance_upbit-current_balance_upbit)
                profit_total = profit_binance + profit_upbit
                ror_total = profit_total/buy_price_total
                data = pd.read_csv('trading_info.txt', sep = "\t", engine='python', encoding = "cp949")
                df = pd.DataFrame(data)
                dt_now = datetime.datetime.now()
                df = df.append({'date':dt_now.strftime('%Y-%m-%d %H:%M:%S'), 'enter_kimp':str(round(enter_kimp,5)*100) + "%", 'total_seed':str(round(buy_price_total,2)) + "KRW", 'end_kimp':str(round(end_kimp,5)*100) + "%", 'profit_upbit':str(round(profit_upbit,2)) + "KRW", 'profit_binance':str(round(profit_binance,2))+"KRW", 'profit_total':str(round(profit_total,2)) + "KRW", 'ror':str(round(ror_total,4))+"%"}, ignore_index=True)
                print(df)
                df.to_csv('trade_info.txt',index=False, sep="\t")
                # post_message(myToken,"#kimauto","total profit:" + str(profit_total) + "KRW\nROR:" + str(round(ror_total,2) + "%"))
                break

            if current_state == 1 :
                break

            count_coin_number_4 = count_coin_number_4 + 1
                
    except Exception as e:
        print(e)
        time.sleep(1)

