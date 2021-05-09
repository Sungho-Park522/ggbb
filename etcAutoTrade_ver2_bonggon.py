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
 
# myToken = "xoxb-2058296221329-2045897155603-WlHbwGwE2jjkESXcjMtiznOw"
 
# post_message(myToken,"#kimauto","dd")

# BONGGON
access_upbit = "
secret_upbit = "

access_binance = '
secret_binance = '

binance = ccxt.binance({
    'apiKey': access_binance,
    'secret': secret_binance
})

upbit = pyupbit.Upbit(access_upbit, secret_upbit)
binance.nonce = lambda: binance.milliseconds() - 1000  # this line is only needed once in the beginning of your program
all_balance = binance.fetch_balance()

print("autotrade start")

base_price = 1120.5


enter_kimp = 0.09
end_kimp = 0.118

current_state = 0

trade_coin = "DOGE"
coin_name_upbit = "KRW-" + trade_coin
coin_name_binance = trade_coin + "/USDT"

while True:
    try:
        order_tf_binance = True
        order_tf_upbit = True
 
        balance_binance = binance.fetch_balance(params={'type': 'future'})
        current_balance_binance = float(balance_binance['USDT']['free'])

        etc_binance = binance.fetch_ticker(coin_name_binance)
        price_coin_binance = float(etc_binance['info']['lastPrice'])
        
        current_balance_upbit = float(upbit.get_balance(ticker="KRW"))
        price_etc_upbit = float(pyupbit.get_current_price(coin_name_upbit))
        buy_price_binance = 0
        if current_balance_binance < 0.1*price_coin_binance :
            current_state = 1
        cal_kimp = (price_etc_upbit-price_coin_binance*base_price)/(price_coin_binance*base_price)
        print(cal_kimp)
        if cal_kimp <= enter_kimp and current_state==0:
            balance_binance = binance.fetch_balance(params={'type': 'future'})
            current_balance_binance = float(balance_binance['USDT']['free'])
            order_number_binance = round(current_balance_binance/price_coin_binance,1)-100
            
            order_info_binance = binance.create_market_sell_order(
            symbol=coin_name_binance, 
            amount=order_number_binance,
            params={'type': 'future'}
            )
            while order_tf_binance :
                if order_info_binance['status']!='open' :
                    order_tf_binance=False
            
            enter_price_binance = float(order_info_binance['info']['avgPrice'])
            enter_number_binance = float(order_info_binance['info']['origQty'])
            order_number_upbit = enter_price_binance * enter_number_binance * base_price
            
            upbit.buy_market_order(coin_name_upbit, order_number_upbit)
            while order_tf_upbit :
                enter_number_upbit = upbit.get_balance(ticker=coin_name_upbit)
                if enter_number_upbit !=0 :
                    order_tf_upbit=False
                    current_state=1
            print("Enter!")
            
            # buy_price_total = order_number_upbit * 2
            # real_enter_kimp = round(((order_number_upbit/enter_number_upbit)-(enter_price_binance*base_price))/(enter_price_binance*base_price),2)

            # post_message(myToken,"#kimauto","enter kimp:" + str(float(real_enter_kimp)*100) + "%\nTotal buy price:" + str(buy_price_total) + "KRW")

            order_tf_binance = True
            order_tf_upbit = True
        elif cal_kimp >= end_kimp and current_state==1:
            binance.create_market_buy_order(
                symbol=coin_name_binance, 
                amount=enter_number_binance,
                params={'type': 'future'}
                )
            while order_tf_binance :
                if order_info_binance['status']!='open' :
                    order_tf_binance = False
            upbit.sell_market_order(coin_name_upbit,enter_number_upbit)
            while order_tf_upbit :
                etc_number_upbit = upbit.get_balance(ticker=coin_name_upbit)
                if etc_number_upbit == 0 :
                    order_tf_upbit = False
                    current_state=0
            print("End!")
            # balance_binance = binance.fetch_balance(params={'type': 'future'})
            # after_balance_binance = float(balance_binance['USDT']['free'])
            # after_balance_upbit = float(upbit.get_balance(ticker="KRW"))
            # profit_binance = (after_balance_binance-current_balance_binance)*base_price
            # profit_upbit = (after_balance_upbit-current_balance_upbit)
            # profit_total = profit_binance + profit_upbit
            # ror_total = profit_total/buy_price_total
            # post_message(myToken,"#kimauto","total profit:" + str(profit_total) + "KRW\nROR:" + str(ror_total))
    except Exception as e:
        print(e)
        time.sleep(1)

