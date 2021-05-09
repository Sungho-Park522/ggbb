import time
import pyupbit
import datetime
import ccxt
import pprint

access_upbit = ""
secret_upbit = ""

access_binance = ''
secret_binance = ''

binance = ccxt.binance({
    'apiKey': access_binance,
    'secret': secret_binance
})

upbit = pyupbit.Upbit(access_upbit, secret_upbit)
print("autotrade start")

base_price = 1120.5


enter_kimp = 0.06
end_kimp = 0.085


current_state = 0

while True:
    try:
        order_tf_binance = True
        order_tf_upbit = True
 
        balance_binance = binance.fetch_balance(params={'type': 'future'})
        current_balance_binance = float(balance_binance['USDT']['free'])

        etc_binance = binance.fetch_ticker("ETC/USDT")
        price_etc_binance = float(etc_binance['info']['lastPrice'])
        
        balance_upbit = upbit.get_balances()
        price_etc_upbit = float(pyupbit.get_current_price("KRW-ETC"))
        buy_price_binance = 0
        if current_balance_binance < 0.1*price_etc_binance :
            current_state = 1
        cal_kimp = (price_etc_upbit-price_etc_binance*base_price)/(price_etc_binance*base_price)
        print(cal_kimp)
        if cal_kimp <= enter_kimp and current_state==0:
            
            balance_binance = binance.fetch_balance(params={'type': 'future'})
            current_balance_binance = float(balance_binance['USDT']['free'])
            order_number_binance = round(current_balance_binance/price_etc_binance,1)-0.01
            
            order_info_binance = binance.create_market_sell_order(
            symbol='ETC/USDT', 
            amount=order_number_binance,
            params={'type': 'future'}
            )
            while order_tf_binance :
                if order_info_binance['status']!='open' :
                    order_tf_binance=False
            
            enter_price_binance = float(order_info_binance['info']['avgPrice'])
            enter_number_binance = float(order_info_binance['info']['origQty'])
            order_number_upbit = enter_price_binance * enter_number_binance * base_price
            
            upbit.buy_market_order("KRW-ETC", order_number_upbit)
            while order_tf_upbit :
                enter_number_upbit = upbit.get_balance(ticker="KRW-ETC")
                if enter_number_upbit !=0 :
                    order_tf_upbit=False
                    current_state=1
            print("Enter!")
            order_tf_binance = True
            order_tf_upbit = True
        elif cal_kimp >= end_kimp and current_state==1:
            binance.create_market_buy_order(
                symbol='ETC/USDT', 
                amount=enter_number_binance,
                params={'type': 'future'}
                )
            while order_tf_binance :
                if order_info_binance['status']!='open' :
                    order_tf_binance = False
            upbit.sell_market_order("KRW-ETC",enter_number_upbit)
            while order_tf_upbit :
                etc_number_upbit = upbit.get_balance(ticker="KRW-ETC")
                if etc_number_upbit == 0 :
                    order_tf_upbit = False
                    current_state=0
            print("End!")
    except Exception as e:
        print(e)
        time.sleep(1)

