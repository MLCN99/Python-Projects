#Import required libraries
import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(soup,quotes):
    quoteClass = htmlContent.find_all('div',class_="quote")

    # loop to extract elements and store into quotes arr
    for quote in quoteClass:
        # extract the text of the quote
        text = quote.find('span', class_='text').text   
        text = text.replace("'","").replace("“","").replace("”","")
        # extract the author of the quote
        author = quote.find('small', class_='author').text
        # extract the tag <a> HTML elements related to the quote
        tag_elements = quote.find('div', class_='tags').find_all('a', class_='tag')

        # store the list of tag strings in a list
        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        quotes.append({
            'text': text,
            'author': author,
            'tags': ', '.join(tags) # merge the tags into a "A, B, ..., Z" string
        })

#Var definition
TargetURL = 'https://quotes.toscrape.com'
quotes = []
csvFilePath = '<localFilePath>'
#Get the HTML content from targetted site
response = requests.get(TargetURL)
htmlContent = BeautifulSoup(response.text, 'html.parser')

# scraping the home page
scrape_page(htmlContent, quotes)

# getting the "Next →" HTML element
next_li_element = htmlContent.find('li', class_='next')

# if there is a next page to scrape
while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    # getting the new page
    page = requests.get(TargetURL + next_page_relative_url)

    # parsing the new page
    soup = BeautifulSoup(page.text, 'html.parser')

    # scraping the new page
    scrape_page(soup, quotes)

    # looking for the "Next →" HTML element in the new page
    next_li_element = soup.find('li', class_='next')

# reading  the "quotes.csv" file and creating it
# if not present
csv_file = open(csvFilePath + '/quotes.csv', 'w', encoding='utf-8', newline='')
# initializing the writer object to insert data
# in the CSV file
writer = csv.writer(csv_file)

# writing the header of the CSV file
writer.writerow(['Text', 'Author', 'Tags'])

# writing each row of the CSV
for quote in quotes:
    writer.writerow(quote.values())

# terminating the operation and releasing the resources
csv_file.close()


