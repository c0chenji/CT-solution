from pycoingecko import CoinGeckoAPI

import pandas as pd
import datetime
import time
import ccxt
import _thread
#  Coinbase api
#  Remember to enter key and secret
coinbase = ccxt.coinbase(
    {
        'apiKey': '',
        'secret': '',
    })

# coin gecko api
cg = CoinGeckoAPI()

def convert_time(d):
    
    return (datetime.date.fromtimestamp(d/1000.0))

def symbol_name_map():
    temp_dic = {}
    target = cg.get_coins_markets("usd")
    for item in target:
        k, v = item["symbol"], item["id"]
        temp_dic[k] = v
    return temp_dic


def convert_id(id):
    
    return symbol_name_map()[id.lower()]
    


# Input should be "bitcoin" format not symbol
def current_price(id, currency="usd"):
    target = cg.get_price(ids=id, vs_currencies=currency)
    target_price = target[id][currency]
    return target_price


def current_market_cap(id, currency="usd"):

    target = cg.get_price(ids=id, vs_currencies=currency,
                        include_market_cap="true")
    target_format = currency+"_market_cap"

    return target[id][target_format]


def current_vol(id, currency="usd"):
    target = cg.get_price(ids=id, vs_currencies=currency,
                        include_24hr_vol='true')
    target_format = currency+"_24h_vol"
    return target[id][target_format]


# check price, market_cap, vol by single  id with format "btc","ltd"
def check_price_by_id(id, currency="usd"):
    id = convert_id(id)
    return current_price(id, currency)


def check_market_cap_by_id(id, currency="usd"):
    id = convert_id(id)
    return current_market_cap(id, currency)


def check_vol_by_id(id, currency="usd"):
    id = convert_id(id)
    return current_vol(id, currency)


# def export_price(id, currency="usd"):
#     # rootPath = r"D:\Programming\wamp\www\Python\api_request\coinGecko"
#     global btc_price

#     coin_price = cg.get_price(ids=id, vs_currencies=currency, include_market_cap='true',
#                             include_24hr_vol='true', include_24hr_change='true', include_last_updated_at='true')
#     if(isinstance(id, list)):
#         temp_list = []
#         for i in id:

#             temp_list.append({
#                 "Asset": i.capitalize(),
#                 "Ticker": i.upper()+"/"+currency.upper(),
#                 "Token price": coin_price[i]["usd"],
#                 "Market Cap": coin_price[i]["usd_market_cap"],
#                 "24h_volume": coin_price[i]["usd_24h_vol"],
#                 "24h_change": coin_price[i]["usd_24h_change"],
#                 "last_updated_at": coin_price[i]["last_updated_at"]

#             })
#         result = pd.DataFrame.from_records(temp_list)
#         result.to_csv(rootPath+"\\"+"coin_list"+"_price_" +
#                     datetime.datetime.now().strftime('%Y-%m-%d')+".csv", index=True, header=True)

#     else:
#         new_dict = {
#             "Asset": id.capitalize(),
#             "Ticker": id.upper()+"/"+currency.upper(),
#             "Token price": coin_price[id]["usd"],
#             "Market Cap": coin_price[id]["usd_market_cap"],
#             "24h_volume": coin_price[id]["usd_24h_vol"],
#             "24h_change": coin_price[id]["usd_24h_change"],
#             "last_updated_at": coin_price[id]["last_updated_at"]
#         }
#         temp_btc_price = coin_price[id]["usd"]
#         # print(btc_price)
#         result = pd.DataFrame.from_records([new_dict])
#         result.to_csv(rootPath+"\\"+id+"_price_"+datetime.datetime.now().strftime(
#             '%Y-%m-%d')+".csv", index=True, header=True)


def export_coin_history_by_id(coinId, currency="usd", date=datetime.datetime.now()):
    temp_list = []
    if(isinstance(coinId, str)):
        try:
            coinId = convert_id(coinId)
            temp_result_today = cg.get_coin_history_by_id(
                coinId, date.strftime('%d-%m-%Y'))
            # print("Today is {}".format(date.strftime('%d-%m-%Y')))

            temp_result_7_day = cg.get_coin_history_by_id(
                coinId, (date-datetime.timedelta(7)).strftime('%d-%m-%Y'))
            # print("last 7 day is {}".format(
            #     (date-datetime.timedelta(7)).strftime('%d-%m-%Y')))

            temp_result_30_day = cg.get_coin_history_by_id(
                coinId, (date-datetime.timedelta(30)).strftime('%d-%m-%Y'))
            # print("last 30 day is {}".format(
            #     (date-datetime.timedelta(30)).strftime('%d-%m-%Y')))

            # print("7 DAY VOLUME IS {}".format(
            #     temp_result_7_day["market_data"]["total_volume"][currency]))
            # print("30 DAY VOLUME IS {}".format(
            #     temp_result_30_day["market_data"]["total_volume"][currency]))
            temp_list.append({
                "Asset": temp_result_today["name"],
                "Ticker": temp_result_today["symbol"].upper()+"/"+currency.upper(),

                "Current Token Price": current_price(coinId, currency),
                "Current Market Cap": current_market_cap(coinId, currency),
                "Volume 24-hour": current_vol(coinId, currency),

                "Price 7-Day": temp_result_7_day["market_data"]["current_price"][currency],
                "Market Cap 7-Day": temp_result_7_day["market_data"]["market_cap"][currency],
                "Volume 7-Day": temp_result_7_day["market_data"]["total_volume"][currency],

                "Price 30-Day": temp_result_30_day["market_data"]["current_price"][currency],
                "Market Cap 30-Day": temp_result_30_day["market_data"]["market_cap"][currency],
                "Volume 30-Day": temp_result_30_day["market_data"]["total_volume"][currency]
            })

            result = pd.DataFrame.from_records(temp_list)
            result.to_csv(rootPath+"\\"+"coin_history_single_input"+"_"+datetime.datetime.now(
            ).strftime('%Y-%m-%d-%H-%M')+".csv", index=True, header=True)
        except:
            print("data loading error str")
    if(isinstance(coinId, list)):
        temp_list = []
        for item in coinId:
            try:
                # covert id inputs btc--->bitcoin
                item = convert_id(item)
                temp_result_today = cg.get_coin_history_by_id(
                    item, date.strftime('%d-%m-%Y'))
                # print("Today is {}".format(date.strftime('%d-%m-%Y')))

                temp_result_7_day = cg.get_coin_history_by_id(
                    item, (date-datetime.timedelta(7)).strftime('%d-%m-%Y'))
                # print("last 7 day is {}".format(
                #     (date-datetime.timedelta(7)).strftime('%d-%m-%Y')))

                temp_result_30_day = cg.get_coin_history_by_id(
                    item, (date-datetime.timedelta(30)).strftime('%d-%m-%Y'))
                # print("last 30 day is {}".format(
                #     (date-datetime.timedelta(30)).strftime('%d-%m-%Y')))

                temp_list.append({
                    "Asset": temp_result_today["name"],
                    "Ticker": temp_result_today["symbol"].upper()+"/"+currency.upper(),

                    "Current Token Price": current_price(item, currency),
                    "Current Market Cap": current_market_cap(item, currency),
                    "Volume 24-hour": current_vol(item, currency),

                    "Price 7-Day": temp_result_7_day["market_data"]["current_price"][currency],
                    "Market Cap 7-Day": temp_result_7_day["market_data"]["market_cap"][currency],
                    "Volume 7-Day": temp_result_7_day["market_data"]["total_volume"][currency],

                    "Price 30-Day": temp_result_30_day["market_data"]["current_price"][currency],
                    "Market Cap 30-Day": temp_result_30_day["market_data"]["market_cap"][currency],
                    "Volume 30-Day": temp_result_30_day["market_data"]["total_volume"][currency]
                })
                result = pd.DataFrame.from_records(temp_list)
                result.to_csv(rootPath+"\\"+"coin_history_multi_inputs"+"_"+datetime.datetime.now(
                ).strftime('%Y-%m-%d-%H-%M')+".csv", index=True, header=True)
            except:
                print("data loading error")


def export_coins_markets(id, currency="usd"):
    if(isinstance(id, str)):
        try:
            temp_source = cg.get_coins_markets(currency)
            for item in temp_source:
                if item["symbol"] == id:
                    # convert result into dataframe if found item
                    result = pd.DataFrame.from_records([item])
                    result.to_csv(rootPath+"\\"+"coins_markets_single_input"+"_"+datetime.datetime.now(
                    ).strftime('%Y-%m-%d-%H-%M')+".csv", index=True, header=True)
                    break
        except:
            print("error:string input")

    # loop over dict when input is list
    if(isinstance(id, list)):
        try:
            temp_list = []
            temp_source = cg.get_coins_markets(currency)
            for key in id:
                for item in temp_source:
                    if item["symbol"] == key:
                        temp_list.append(item)
            result = pd.DataFrame.from_records(temp_list)
            result.to_csv(rootPath+"\\"+"coins_markets_multi_inputs"+"_"+datetime.datetime.now(
            ).strftime('%Y-%m-%d-%H-%M')+".csv", index=True, header=True)
        except:
            print("error: list input")


def export_balance():
    target = coinbase.fetch_balance()["info"]["data"]
    temp_list = []
    for item in target:
        temp_dict = {
            "id": item["id"],
            "name": item["name"],
            "currency_code": item["currency"]["code"],
            "currency_name": item["currency"]["name"],
            "sort_index": item["currency"]["sort_index"],
            "balance_amount": item["balance"]["amount"],
            "balance_currency": item["balance"]["currency"]

        }
        temp_list.append(temp_dict)
    result = pd.DataFrame.from_records(temp_list)
    result.to_csv(rootPath+"\\"+"balance"+"_"+datetime.datetime.now(
    ).strftime('%Y-%m-%d-%H-%M')+".csv", index=True, header=True)


def process_price_update(id):
    # single input
    if(len(id) == 1):
        # inital export for single input
        export_coin_history_by_id(id[0])
        export_coins_markets(id[0])
        temp_price = check_price_by_id(id[0])
        export_balance()
        
        print("\n Inital price is {}".format(check_price_by_id(id[0])))
        while True:
            # update price value in csv files
            if check_price_by_id(id[0]) != temp_price:
                #wait for data synchrozie
                time.sleep(3)
                print("\n updated price is {}".format(check_price_by_id(id[0])))
                temp_price = check_price_by_id(id[0])
                export_coin_history_by_id(id[0])
                export_coins_markets(id[0])
    # multiple inputs
    if(len(id) > 1):
        temp_price_list = [check_price_by_id(i) for i in id]
        print("\n Inital price list is {}".format(temp_price_list))
        export_balance()
        export_coin_history_by_id(id)
        export_coins_markets(id)
        while True:
            # update price value in csv files
            if [check_price_by_id(i) for i in id] != temp_price_list:
                #wait for data synchrozie
                time.sleep(3)
                print("\n updated price list is {}".format([check_price_by_id(i) for i in id]))
                temp_price_list = [check_price_by_id(i) for i in id]
                export_coin_history_by_id(id)
                export_coins_markets(id)

def throw_tasks(a):
    temp_a=[i.lower() for i in a]
    task_name = "-".join(temp_a)    
    # print("task name {}".format(task_name))
    try:
        _thread.start_new_thread(process_price_update, (a,))
    except:
        print ("Error: unable to start thread")


if __name__ == "__main__":
    rootPath = r"the directory you want to export outputs"
    # testd history
    # export_coin_history_by_id("btc")
    # export_coin_history_by_id(["btc","ltc"],"eur")

    # # tested  markets
    # export_coins_markets("btc")
    # # export_coins_markets(["btc","ltc"],"eur")

    # ##tested balance from ccxt
    # export_balance()

    ## convert time from old data version
    # d=coinbase.fetchTime()
    # print(convert_time(d)) 

    # Testd
    while True:
        temp_input=list(map(str,input(f"Enter ID :").split()))
        throw_tasks(temp_input)