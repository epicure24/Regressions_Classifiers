import bs4 as bs
import urllib.request
import re

scraped_data = urllib.request.urlopen('https://en.wikipedia.org/wiki/Latent_Dirichlet_allocation')
article = scraped_data.read()

parsed_article = bs.BeautifulSoup(article,'lxml')

paragraphs = parsed_article.find_all('p')

article_text = ""

for p in paragraphs:
    article_text += p.text

print(article_text)
