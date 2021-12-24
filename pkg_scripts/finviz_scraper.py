import pandas as pd,os
import numpy as np
from datetime import datetime as dt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class FinvizScraper:
    def __init__(self,**kwargs):
        
        # Initialize kwargs
        self.date_val = kwargs.get('date_val')
        self.html = kwargs.get('html')
        self.symbol = kwargs.get('symbol')
        
        # run methods
        self.insider = self.get_insider()          
        self.fundamentals = self.get_fundamentals()        
        self.news = self.get_news()
        
        # Initialize filename string
        filename = f'finviz_scraper_{self.symbol}_{self.date_val.strftime("%m_%d_%Y_%H%M%S")}.xlsx'
        
        # If "output" folder does not exist in `BASE_DIR`, create it.
        if not os.path.isdir(os.path.join(BASE_DIR,'output')):
            os.mkdir(os.path.join(BASE_DIR,'output'))
            
        # Initialize XlsxWriter object
        writer = pd.ExcelWriter(os.path.join(BASE_DIR,'output',filename))
        
        # Send dataframes to XlsxWriter
        self.insider.to_excel(writer,sheet_name='insiders',index=False)        
        self.fundamentals.to_excel(writer,sheet_name='fundamentals',index=False)
        self.news.to_excel(writer,sheet_name='news',index=False)

        # Save xlsx workbook
        writer.save()
        
    def get_fundamentals(self):
        try:
            # Find fundamentals table
            fundamentals = pd.read_html(str(self.html), attrs = {'class': 'snapshot-table2'})[0]
            
            # Clean up fundamentals dataframe
            fundamentals.columns = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
            colOne = []
            colLength = len(fundamentals)
            for k in np.arange(0, colLength, 2):
                colOne.append(fundamentals[f'{k}'])
            attrs = pd.concat(colOne, ignore_index=True)
        
            colTwo = []
            colLength = len(fundamentals)
            for k in np.arange(1, colLength, 2):
                colTwo.append(fundamentals[f'{k}'])
            vals = pd.concat(colTwo, ignore_index=True)
            
            fundamentals = pd.DataFrame()
            fundamentals['Attributes'] = attrs
            fundamentals['Values'] = vals
            return fundamentals

        except Exception as e:
            return e
        
    def get_news(self):
        try:
            # Find news table
            news = pd.read_html(str(self.html), attrs = {'class': 'fullview-news-outer'})[0]
            links = []
            for a in self.html.find_all('a', class_="tab-link-news"):
                links.append(a['href'])
            
            # Clean up news dataframe
            news.columns = ['Date', 'News Headline']
            news['Article Link'] = links
            
            return news

        except Exception as e:
            return e

    def get_insider(self):
        try:
            # Find insider table
            insider = pd.read_html(str(self.html), attrs = {'class': 'body-table'})[0]
            
            # Clean up insider dataframe
            insider = insider.iloc[1:]
            insider.columns = ['Trader', 'Relationship', 'Trade Date', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'SEC Form 4 Date']
            insider['Symbol'] = self.symbol
            insider = insider[['Symbol', 'Trader', 'Relationship', 'Transaction', 'Cost', '# Shares', 'Value ($)', '# Shares Total', 'Trade Date', 'SEC Form 4 Date']]
         
            # Format SEC Form 4 date field
            insider['SEC Form 4 Date'] = insider['SEC Form 4 Date'].apply(lambda x: dt.strptime(x,'%b %d %H:%M %p').strftime("%m/%d/%Y").replace('1900',self.date_val.strftime("%Y")))

            # Format Trade Date
            insider['Trade Date'] = insider['Trade Date'].apply(lambda x: dt.strptime(x,'%b %d').strftime("%m/%d/%Y").replace('1900',self.date_val.strftime("%Y")))
            
            # Format values
            for col in ['Cost', '# Shares', 'Value ($)', '# Shares Total']:
                insider[col] = insider[col].apply(lambda x: "{:,}".format(float(x)))
                
            return insider

        except Exception as e:
            return e