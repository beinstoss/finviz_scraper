Creator: Bryan Einstoss

Summary: Scrape finviz url (https://finviz.com/insidertrading.ashx) to extract insider trading information for tickers selected by the user (inputted into “.\mapping_tables\ticket_symbol_list”). When the scraper is ran, an output containing insider transactions, ticker fundamentals and news will be exported in the form of XLSX into the “.\output” folder. If there is a new insider transaction on “run date”, an email will be delivered to the user containing a summary table with transaction details.

Downloading Python: If a version of Python 3+ is not already installed within the user’s computer, please install the most recent version of Python from the official site (site and Python 3.10 download link below).
-	Official Python Site: https://www.python.org/
-	Python 3.10 download: https://www.python.org/ftp/python/3.10.1/python-3.10.1-amd64.exe

Installing Requirements: To ensure the version of Python being used contains all required modules, open a command prompt (you can search CMD on your Windows Search Bar) and navigate to the finviz_scraper repository. Once within the repository location, pass the following command: “pip install -r requirements.txt”. The requirements.txt file holds commands to install all required modules to successfully run finviz_scraper.
 

Setting up email alerts: Open the JSON configuration file found within “.\config\config.json” and insert email/password credentials for an Office365 email (Gmail based delivery is not supported, can be customized by the user within the “.\pkg_scripts\mail.py” module if desired). Emails will only be generated if there is new insider transaction activity (ie: if process is ran on 12/23/2021 AND there is an SEC Filing for Insider Transactions on 12/23/2021, an email notification will be sent).

Running finviz_scraper: Double click the following file to execute the process: “.\executable\finviz_scraper.bat”. You can find information on how to automate runs of this executable batch file within this link (specifically under the “Run batch file on schedule” section): https://www.windowscentral.com/how-create-and-run-batch-file-windows-10

References
Credit for the scraping code goes to Shashank Vemuri for the following tutorial: Scraping FinViz: The Ultimate Stock Screener with Python!.

