from bs4 import BeautifulSoup
import requests
import pandas as pd

site_url = 'https://books.toscrape.com'

titles = []
ratings = []
prices = []
imgs = []

def get_books(soup_text):
	book_items = soup.find_all('article', 'product_pod')
	for book in book_items:
		titles.append(book.h3.text)
		for attr_name, class_names in book.find('p', 'star-rating').attrs.items():
			ratings.append(class_names[1])
		prices.append(book.find('p', 'price_color').text)
		img_url = book.find('div', 'image_container').img.attrs['src']

		imgs.append(site_url + img_url.replace('..', ''))

page_count = 10

for i in range(1, page_count + 1):
	url = f'https://books.toscrape.com/catalogue/page-{i}.html'
	r = requests.get(url)
	soup = BeautifulSoup(r.text, 'html.parser')
	get_books(soup)

data = {'Title': titles, 'Price': prices, 'Image': imgs, 'Rating': ratings}

df = pd.DataFrame(data=data)
df.index += 1

df.to_excel('books.xlsx')
