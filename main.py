# https://www.youtube.com/watch?v=txKBWtvV99Y
# https://free.currencyconverterapi.com/
# shttps://stackoverflow.com/questions/6528117/keep-only-n-last-records-in-sqlite-database-sorted-by-date
from locale import currency
from pprint import PrettyPrinter, pprint
import json, requests

API_URL = "http://free.currconv.com/"
API_KEY = "Your_API_key"
printer = PrettyPrinter() # nice format of get JSON from API

    
def unpackAPIcurrnecies():
    '''endpoint = "api/v7/currencies?apiKey=%s" % (API_KEY)'''
    endpoint = f"api/v7/currencies?apiKey={API_KEY}"
    url = API_URL + endpoint
    data = requests.get(url).json()['results']
    '''
    data_str = data.text
    json.loads(data_str)
    data = list(data.items())
    data.sort()
    '''
    data = list(data.items())
    #data.sort()
    
    return data # key 'result' which has python dictionary for every single currency 

def listCurrencies(data):
    for name, currency in data:
        name = currency['currencyName']
        identification_number = currency['id']
        symbol = currency.get("currencySymbol", "") # if empty key 'currencySymbol' return empty string
        print(f"{identification_number} - {name} - {symbol}")        


def exchangeRate(currency1, currency2):
    endpoint = f"api/v7/convert?q={currency1}_{currency2}&compact=ultra&apiKey={API_KEY}"
    url = API_URL + endpoint
    data = requests.get(url).json() # return dictionary {"curr1 -> curr 2 =" : rate}
    if len(data) == 0:
        print("Invalid.")
        return
    rate = list(data.values())[0]
    print(f"{currency1} => {currency2} = {rate}")
    return rate

def convert(currency1, currency2, amount):
    rate = exchangeRate(currency1, currency2)
    if rate is None: # Invalid currency
        return
    try: 
        amount = float(amount)
    except:
        print("Invalid currency")
        return
    converted_amount = rate * amount
    print(f"{amount} {currency1} is equal to {converted_amount} {currency2}")
    return converted_amount

# data = get_currencies()
# # printer.pprint(data)
# printing(data)
# rate = exchange_rate("USD", "CAD")
# print(rate)


if __name__ == "__main__":
    currencies = unpackAPIcurrnecies()
    print("Currency conversion")
    print("LIST => lists currencies")
    print("CONVERT => converts between currencies")
    print("RATE => gets the exchange rate")
    print()

    while True:
        command = input("Enter command, q to quit:")
        if command == "q":
            print("GOOD BYE")
            break
        elif command == "LIST":
            listCurrencies(currencies)
        elif command == "CONVERT":
            currency1 = input("Base currency: ").upper()
            amount = input(f"amount in {currency1}: ")
            currency2 = input("Convert to: ").upper()
            convert(currency1, currency2, amount)
        elif command == "RATE":
            currency1 = input("Base currency: ").upper()
            currency2 = input("Convert to: ").upper()
            exchangeRate(currency1, currency2)
        else:
            print("INVALID INPUT!")

