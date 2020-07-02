# COVID-19 Updates Scraper (International)
This web scraper uses [Scrapy](https://scrapy.org/) with Python to scrape all updates posted in select government websites regarding COVID-19

This scraper uses scrapy,[CLD-2](https://pypi.org/project/cld2-cffi/), [dateparser](https://pypi.org/project/dateparser/), and [html2text](https://pypi.org/project/html2text/) as dependencies. I am also using Python3 to create a [virtual environment](https://docs.python.org/3/library/venv.html#venv-def) to create an isoalted environment to run the scraper on.

## Steps before running scraper:
- Create a virtualenv and run it. (This is slightly different for [Windows](https://programwithus.com/learn-to-code/Pip-and-virtualenv-on-Windows/) vs [Linux/Mac](https://www.pythonforbeginners.com/basics/how-to-use-python-virtualenv))
- Run `pip install scrapy`,`pip install cld2-cffi`, `pip install dateparser`, and `pip install html2text` from the virtualenv to install all the dependencies
## Running the Scraper on Windows
While inside the virtualenv `cd` into the directory that contains `powershell_script.ps1` and run `.\powershell_script.ps1` while passing allowed arguments, from powershell terminal to run the script. For example, running `.\powershell_script.ps1 cdc` will fetch covid-19 related posts from the CDC website. The list of allowed options can be found in the bottom of this document.
## Running the Scraper on Mac/Linux
While inside the virtualenv `cd` into the directory that contains `unix_script.sh` and run `bash unix_script.sh` while passing allowed arguments, from shell terminal to run the script. For example, running `bash unix_script.sh cdc` will fetch covid-19 related posts from the CDC website. The list of allowed options can be found in the bottom of this document.

## Accessing the data
The scraped posts are saved in `posts` directory in the format `{title,source,published,url,scraped,classes,country,municipality,language,text}` for each post. The links to each update are saved in `links` directory.

## List of allowed shell arguments: 
#### v0-dataset:
- [CDC](https://www.cdc.gov/coronavirus/2019-ncov/whats-new-all.html)
- [Brazil](https://www.saude.gov.br/noticias?filter-search=coronavirus&limit=0&filter-start_date=&filter-end_date=&filter_order=&filter_order_Dir=&limitstart=&task=)
- [Spain](https://www.mscbs.gob.es/profesionales/cargarNotas.do?time=1577833200000)
- [UK](https://www.gov.uk/search/all?content_purpose_supergroup%5B%5D=news_and_communications&level_one_taxon=5b7b9532-a775-4bd2-a3aa-6ce380184b6c&order=updated-newest&page=1)
- [Italy](http://www.salute.gov.it/portale/nuovocoronavirus/archivioNotizieNuovoCoronavirus.jsp?lingua=italiano&menu=notizie&p=dalministero&area=nuovocoronavirus&notizie.page=0)
- [Germany](https://www.bundesregierung.de/breg-de/suche/992800!search?f=1495774%3A1726012&page=0)
- [Peru](https://www.gob.pe/busquedas?contenido[]=noticias&desde=01-01-2020&institucion[]=minsa&reason=sheet&sheet=1&term=coronavirus)
- [New_Zealand](https://www.health.govt.nz/search/results/coronavirus?f%5B0%5D=im_field_news_type%3A31) (Links to this were added manually) [Regex link](https://regex101.com/r/MxoFhB/1)
- [Korea](http://ncov.mohw.go.kr/tcmBoardList.do?pageIndex=1&brdId=&brdGubun=&board_id=&search_item=1&search_content=)
#### v1-dataset (v0+others):
- __All__ (Run all scrapers)

**Note:** Since all the passed arguments are converted into lowercase, casing doesn't matter when you are passing it in the shell. For example: `.\powershell_script.ps1 cDc` would work the same way as `.\powershell_script.ps1 CDC`

## Important Notes:
- Since the addition to `posts` are appended on instead of overwritten, all the contents of or the whole directory - `posts` must be deleted before each run (except the first run since `posts` directory does not exist yet during the first run). If this step is not taken `posts` **WILL HAVE** incorrect data
- **DO NOT** delete the files in `links` directory even though it is safe to delete the contents of the files themselves
- Since the log settings has been set to `INFO` only information will be displayed during runs. If an error is encounterd and the link trying to be scraped has `downloads` or `.pdf` on it somewhere, the error message can be ignored. There might also be a `404` response sometimes and `dateparser errors` which should be ignored on a case-by-case basis
- While in virtualenv run `deactivate` to stop and exit the virtual envrionment
- Source code for scraper can be found in `spiders` directory
