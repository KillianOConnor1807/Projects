# Author - Killian O'Connor
# Date - 03/08/2025
# Description - building a currency converter using an API - intro to APIs - ref 'TechWithTim'

from requests import get
from pprint import PrettyPrinter  # allows a nicer format output w/ json

BASE_URL = "https://api.freecurrencyapi.com/v1/"
API_KEY = "fca_live_PxNUOPJG2MyDquNsBGFHpYYQiwbJhWVsXgB6lZYm"

printer = PrettyPrinter()

def get_currencies():
    endpoint = f"currencies?apikey={API_KEY}" # makes the end of the URL
    url = BASE_URL + endpoint
    data = get(url).json()['data'] # sends a req to the link and gets the data back in Json format - dict in python - ['data'] because the dict with the key as data
    data = list(data.items()) # convert data to a list
    data.sort() # sort by currency name
    
    return data
    # gives a dict that looks like - 'EUR': {'code': 'EUR','decimal_digits': 2,'name': 'Euro','name_plural': 'Euros','rounding': 0,'symbol': '€','symbol_native': '€','type': 'fiat'},

def show_currencies(currencies):
    for code, info in currencies: # because each items list of tuples -  'EUR' : {.....} -  code = eur info = {....}
        name = info['name']
        symbol = info.get('symbol', "")
        print(f"{code} - {name} - {symbol}")
        
def exchangeRate(curr1 , curr2): #uses the currency codes
    endpoint = f"latest?apikey={API_KEY}&currencies={curr2}&base_currency={curr1}"
    url = BASE_URL + endpoint
    response = get(url)

    data = response.json()
    
    if len(data) == 0:
        print("Invalid currency - please try again")
        return
    rate = data["data"][curr2] # only return the exchange rate -- data = {'data': {'USD': 1.08842}}
    print(f"\n{curr1} to {curr2} is {rate}")
    return rate


def symbol(curr , data): # returns the symbol for a currency
    for code, info in data: # because each items list of tuples -  'EUR' : {.....} -  code = eur info = {....}
        if code == curr:
            symbol = info.get('symbol', "")
            return symbol
    return ""
        

    

def convert(curr1, curr2 , amount , data):
    symbol1 = symbol(curr1 , data)
    symbol2 = symbol(curr2 , data)
    rate = exchangeRate(curr1 , curr2)
    if rate is None:
        return -1
    
    # try convert to a float so we can multiply , handles invalid input like strings
    try:
        amount =  float(amount) 
    except:
        print("Invalid amount")
        return  
    
    finalConversion = amount * rate
    print(f"{symbol1}{amount}{curr1}  ->  {symbol2}{finalConversion}{curr2}")
    return finalConversion


def main():
    data = get_currencies()

    while True:
        print("\nWhat would you like to do?")
        print("1. Show all currencies")
        print("2. Convert currency")
        print("3. Exit")

        choice = input("Enter choice (1-3): ")

        if choice == "1":
            show_currencies(data)

        elif choice == "2":
            curr1 = input("enter currency code (e.g EUR): ").upper() #  allows lower case 
            curr2 = input("to currency code: ").upper()
            amount = input("Amount to convert : ")
            convert(curr1, curr2, amount, data)

        elif choice == "3":
            print("Peace Out!")
            break

        else:
            print("Invalid choice. Try again.")


main()

