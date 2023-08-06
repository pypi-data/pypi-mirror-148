import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import matplotlib.pyplot as plt
from termcolor import colored as cl

class Stock():

    def __init__(self, stockname, data = None):
        self.stockname = stockname
        self.data = data


    def stock_price(self):
        """
        checks the ticker
        :param stock_name: A ticker
        :return: stock price
        """
        link = ('https://finance.yahoo.com/quote/') + self.stockname + ('?p=') + self.stockname + ('&.tsrc=fin-srch')
        # checks to see if link is valid
        # requests.get(gets all the data from link
        r = requests.get(link)
        # creates parse tree from page source code so now we can extract data
        web_content = BeautifulSoup(r.text, 'lxml')
        # we find the data we are looking for from the website
        web_content = web_content.find('fin-streamer', class_='Fw(b) Fz(36px) Mb(-4px) D(ib)').text
        # from main data we get price from website
        return web_content

    def up_or_down(self):
        """
        up or down
        :param stock_name : self
        :return percent stock is up or down by float
        """
        link = 'https://www.marketwatch.com/investing/stock/' + self.stockname

        r = requests.get(link)
        # creates parse tree from page source code so now we can extract data
        web_content = BeautifulSoup(r.text, 'lxml')

        # we find the data we are looking for from the website
        web_content = web_content.find('div', class_="intraday__data")
        # from main data we get price from website
        web_content = web_content.find('span', class_='change--percent--q').text
        web_content1 = web_content.replace(web_content[-1], '')
        if float(web_content1) > 0:
            print(self.stockname, 'is up', web_content, end=' ')
        else:
            print(self.stockname, 'is down', web_content, end=' ')

    def hist_data(self, interval, period1, period2):
        """
        :Parameters:
            period1 : str
                (MM-DD-YYYY)
            period2 : str
                (MM-DD-YYYY)
            interval : str
                Valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
                Intraday data cannot extend last 60 days
        """
        #converts time from date to seconds to put into url
        period1 = int(time.mktime(time.strptime(str(period1), '%m-%d-%Y')))
        period2 = int(time.mktime(time.strptime(str(period2), '%m-%d-%Y')))

        query = f"https://query1.finance.yahoo.com/v7/finance/download/{self.stockname}?period1={period1}&period2="\
                f"{period2}&interval={interval}&events=history&includeAdjustedClose=true"

        df = pd.read_csv(query)
        self.data = df
        return df

    def plot_data(self):
        self.data.plot('Date', ["Open", "High", "Low", "Close"])
        plt.title(self.stockname)
        plt.show()

    def get_stock_news(self):
        """
        :param: stockname
        :return: news about stock
        """
        url = f'https://eodhistoricaldata.com/api/news?api_token=625d997dd034e6.55225744&s={self.stockname}'
        news_json = requests.get(url).json()

        news = []

        for i in range(10):
            title = news_json[-i]['title']
            news.append(title)
            print(cl('{}. '.format(i + 1), attrs=['bold']), '{}'.format(title))

        return news
