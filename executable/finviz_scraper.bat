@ECHO OFF
ECHO Process Initiated...
FOR %%A IN ("%~dp0.") DO SET folder=%%~dpA
python "%folder%finviz_scraper_engine.py"
ECHO Process Complete!
pause