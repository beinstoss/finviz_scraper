import pandas as pd, json, os, sys
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
from datetime import datetime as dt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,BASE_DIR)
from pkg_scripts import mail, finviz_scraper

# Pull in config file
with open(os.path.join(BASE_DIR,'config','config.json')) as f:
    config = json.load(f)
    config_path = config['FilePaths']

# Pull in ticker symbol list
try:
    symbol_mapping = pd.read_csv(os.path.join(BASE_DIR,'mapping_tables','stock_symbol_list.csv'))
except:
    raise ValueError(f'Unable to read Ticker Symbol Mapping Table. Create csv file as follows: {os.path.join(BASE_DIR,"mapping_tables","stock_symbol_list.csv")}')

# List of tickeers within mapping table
symbol_list = list(set([sym.upper() for sym in symbol_mapping.iloc[:,0].dropna()]))

# List of invalid symbols within mapping table (more or less than 4 characters)
invalid_symbol_list = [sym for sym in symbol_list if len(sym) != 4]

# Catch invalid symbols
if len(invalid_symbol_list) > 0:
    raise ValueError(f'Invalid Symbol within Ticker Symbol List: {invalid_symbol_list}')

# Dict of Symbol:finviz url
url_dict = {symbol:config_path['finviz_url'].format(arg=symbol.lower()) for symbol in symbol_list}

# DF holding all relevant insider data for date_val
all_insider_data = pd.DataFrame()
        
# Iterate through url dict and pass arguments into FinvizScraper class
for symbol,url in url_dict.items():
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    html = soup(webpage, "html.parser")
    
    # Default date of today
    date_val = dt.today()
    
    # Initialize scraper class
    scraper = finviz_scraper.FinvizScraper(date_val=date_val,html=html,symbol=symbol)
    all_insider_data = all_insider_data.append(scraper.insider)
    
# Filter insider data for today
all_insider_data_today = all_insider_data.loc[all_insider_data['SEC Form 4 Date'].isin([date_val.strftime("%m/%d/%Y")])]

# Send email
if len(all_insider_data_today) > 0:   
    # Initialize html string/table
    output_dir = f"Output Directory: {os.path.join(BASE_DIR,'output')}</br></br>"
    html = output_dir + all_insider_data_today.to_html(index=False)
    
    # Send email notification
    mail.send_mail(config['Credentials']['email'],[config['Credentials']['email']],subject=f'FinViz Scraper {date_val.strftime("%m/%d/%Y")}',html=html,config=config)
