from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

class finviz_scanner:

  def __init__(self, url):
    self.url = url
    
  def url_response(self):
    

    req = Request(self.url, headers={'user-agent': 'my-app'})
    response = urlopen(req)
    html = BeautifulSoup(response, 'html.parser')

    return html
  
  def url_screener_pages(self):

    url_root = 'https://finviz.com/'

    html_ls = []
    html = self.url_response()
    html_ls.append(html)
    
    td = html.find('td', {"class":"body-table screener_pagination"})
    a = td.findAll('a', {'class': {"tab-link"}})
    n = a[1].b.text
    href = a[1]['href']
    final_url = url_root+href

    while n =='next':

      req = Request(url=final_url, headers={'user-agent': 'my-app'})
      response = urlopen(req)
      html_new = BeautifulSoup(response, 'html.parser')

      td = html_new.find('td', {"class":"body-table screener_pagination"})
      a = td.findAll('a', {'class': {"tab-link"}})
      for x in a:
        n = x.b.text
        if n == 'next':
          href = x['href']

      final_url = url_root+href
      
      html_ls.append(html_new)
    
    return html_ls
  
  def get_tables(self):
    
    frames = []
    html_ls = self.url_screener_pages()
    for html in html_ls:
      parsed_results = []
      table = html.find('table', {'class':'table-light'})
      table_rows = table.findAll('tr')
      for row in table_rows[1:]:
        pre_parsed_results = []
        a = row.findAll('a')
        for x in a[1:]:
            pre_parsed_results.append(x.text)
        parsed_results.append(pre_parsed_results)


      ls = ['symbol', 'company', 'sector', 'industry', 'country', 'market_cap', 'P/E', 'price', 'change%', 'volume']
      df = pd.DataFrame(parsed_results, columns=ls)
      df['change%'] = df['change%'].apply(lambda x : float(x.strip('%')))
      df['price'] = df['price'].apply(lambda x : float(x))
      df['volume'] = df['volume'].apply(lambda x: int(x.replace(',', '')))
      frames.append(df) 

    df = pd.concat(frames)
    df = df[['symbol', 'price', 'change%', 'volume']]
    df = df.sort_values(by='change%', ascending=False, ignore_index=True)

    return df