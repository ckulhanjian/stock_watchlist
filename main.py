from bs4 import BeautifulSoup
import requests

def main():
    # watchlist = open("watchlist.txt", "a")
    # watchlist
    while True:
        print('\nStock Options')
        menu_options= ['1. Check stock price', '2. Add stock to watchlist', '3. Remove stock from watchlist',
                       '4. Display Watchlist','5. Quit']
        for x in menu_options:
            print(x)
        choice = int(input('\nEnter menu option: '))

        if choice == 1:
            stock_name = input('\nCompany Name? ')
            check_stock(stock_name)
            add = input('\nWould you like to add this to your watchlist (y/n): ')
            if add == 'y':
                cw = check_watchlist(stock_name)
                if cw == False:
                    print('Stock already in watchlist.')
                if cw == True:
                    add_to_watch(stock_name)
                    print('Added to watchlist.')

        if choice == 2:
            stock_name = input('Which company would you like to watch: ')
            cw = check_watchlist(stock_name)
            if cw == False:
                print('Stock already in watchlist.')
            if cw == True:
                add_to_watch(stock_name)
                print('Added to watchlist.')

        if choice == 3:
            stock_name = input('Which company would you like to remove: ')
            cw = check_watchlist(stock_name)
            if cw == False:
                # remove 
            if cw == True:
                print('This stock is not in your watchlist.')

        if choice == 4:
            print('Watchlist:')
            watchlist = open("watchlist.txt", "r")
            for x in watchlist:
                symbol = get_stock_ticker(x)
                price = stock_price(symbol)
                print(f"{x.capitalize().strip()} {symbol} ${price}")
            watchlist.close()
        if choice == 5:
            print('Goodbye')
            break
    return

def check_watchlist(stock_name):
    # check if stock is already in watchlist
    watchlist = open("watchlist.txt", "r")
    for x in watchlist:
        if x.strip() == stock_name.lower():
            return False
    watchlist.close()
    return True
    

def add_to_watch(stock_name):
    watchlist = open("watchlist.txt", "a")
    watchlist.write(stock_name.lower())
    watchlist.write('\n')
    watchlist.close()
    return

def check_stock(stock_name):
    symbol = get_stock_ticker(stock_name)
    price = stock_price(symbol)
    print(f"\nStock Name: {stock_name.capitalize()} \nTicker: {symbol} \nPrice: ${price}")
    return
    
def get_stock_ticker(stock_name):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; \ Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \ Chrome/84.0.4147.105 Safari/537.36'}
    url = f"https://www.google.com/search?q={stock_name}+stock"
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        soup = BeautifulSoup(html.content, 'html.parser')
        # text = soup.find('div', class_='GyAeWb EyBRub')
        # text2 = soup.find('div', class_='XqFnDf')
        text3 = soup.find('div', class_='iAIpCb PZPZlf')
        p = (text3.text).find(':')
        symbol = text3.text[p+2:]
    else:
        print('Error.')
    return symbol

def stock_price(symbol):
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; \ Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \ Chrome/84.0.4147.105 Safari/537.36'}
    url = f"https://www.marketwatch.com/investing/stock/{symbol}"
    html = requests.get(url, headers=headers)
    if html.status_code == 200:
        # beautiful soup parser
        soup = BeautifulSoup(html.content, 'html.parser')
        s = soup.find('div', class_='intraday__data')
        content=s.find('bg-quote', class_='value')
    else:
        print('Error.')
    return content.text

if __name__ == "__main__":
    main()