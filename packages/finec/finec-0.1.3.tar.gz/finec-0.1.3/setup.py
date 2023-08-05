# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['finec']

package_data = \
{'': ['*']}

install_requires = \
['apimoex>=1.2.0,<2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'folium>=0.2.1,<0.3.0',
 'pandas==1.3.5',
 'pymongo>=4.1.1,<5.0.0',
 'requests>=2.23.0,<3.0.0',
 'tqdm>=4.64.0,<5.0.0']

setup_kwargs = {
    'name': 'finec',
    'version': '0.1.3',
    'description': 'Computational finance from Finec MGIMO',
    'long_description': '[![Tests](https://github.com/epogrebnyak/finec/actions/workflows/.pytest.yml/badge.svg)](https://github.com/epogrebnyak/finec/actions/workflows/.pytest.yml)\n\n# finec\n\nFinancial data and financial computation utilities for Finec MGIMO students.\n\n## Installation\n\n```console\npip install git+https://github.com/epogrebnyak/finec.git\n```\n\n## Moscow Exchange (MOEX)\n\nGet Moscow Exchange (MOEX) data for stocks, bonds, currencies and indices as pandas dataframe. \n\n`(*)` denotes lower level functions, skip at first reading.\n\n### Stocks\n\n```python\nfrom finec.moex import Stock, Index\nfrom finec.dividend import get_dividend\n\n# What stocks are in IMOEX index? \nIndex("IMOEX").composition()\n\n# Aeroflot stock information\nStock("AFLT").whoami()\n\n# Ozon stock price history\nStock("OZON").get_history(columns=["TRADEDATE", "CLOSE"])\n\n# Yandex stock price\nStock("YNDX").get_history(start="2022-01-01")\n\n# Get dividend history from https://github.com/WLM1ke/poptimizer\nget_dividend(ticker="GMKN")\n```\n\n### Bonds\n\n```python \nfrom finec.moex import Bond\n\n# Sistema 2027 bond price and yields from TQCB trading bord\nBond(ticker="RU000A0JXN21", board="TQCB").get_history()\n\n# (*) What data columns are provided provide for trading history?\nBond(ticker="RU000A101NJ6", board="TQIR").provided_columns()\n```\n\n### Currencies\n\n```python\nfrom finec.moex import Currency, usd_rur, eur_rur, cny_rur \n\n# USDRUR exchange rate\nCurrency("USD000UTSTOM").get_history(start="2020-01-01")\n\n# Tickers for euro and yuan exchange rates\neur_rur().ticker\ncny_rur().ticker\n```\n\n### Lookup functions\n\n```python \nfrom finec.moex import describe, find, traded_boards\n\n# General information about ticker\ndescribe("YNDX")  \n\n# What boards does a security trade at?\ntraded_boards("MTSS")\n\n# Are there traded securities with *query_str* in description?\nfind(query_str="Челябинский", is_traded=True)\n```\n\n### Markets and boards\n\n```python \nfrom finec.moex import Market, Board\n\nm = Market(engine="stock", market="shares")\nm.traded_boards()\n\nb = Board(engine="stock", market="shares", board="TQBR")\n```\n\n### More about MOEX data\n\nReferences:\n\n- MOEX API reference <https://iss.moex.com/iss/reference/?lang=en>\n- Developper manual (2016) <https://fs.moex.com/files/6523>\n\nNotes: \n\n- MOEX API is very generious to provide a lot of data for free and without any registration or tokens. \n- API provided on "as is" basis, some parts are undocumented.\n\n\n## Aknowledgements\n\n- We rely on `apimoex.ISSClient` and expertise developped within [apimoex project](https://github.com/WLM1ke/apimoex) by [@WLMike1](https://github.com/WLM1ke).\n- Dividend history relayed from <https://github.com/WLM1ke/poptimizer>\n',
    'author': 'Evgeniy Pogrebnyak',
    'author_email': 'e.pogrebnyak@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.13,<4.0.0',
}


setup(**setup_kwargs)
