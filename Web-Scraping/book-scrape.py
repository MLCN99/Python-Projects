#Import required libraries
import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(htmlContent,books):
    productClass = htmlContent.find_all('article',class_="product_pod")

    # loop to extract elements and store into quotes arr
    for book in productClass:
        # Extract the product_price class
        product = book.find('div', class_='product_price')
        # Extract the stock availability and remove whitespace
        stockAvailability = product.find('p', class_='instock availability').text.strip()
        # Extract the price value 
        price = product.find('p',class_='price_color').text

        # Extract the title from the h3 element
        title = book.find('h3').find('a').get('title')
        # Extract the book URL
        url = TargetURL + book.find('h3').find('a', href=True)['href']
        # Extract rating from the class as class name and picking specific index
        rating = book.find('p',class_=lambda x: x and 'star-rating' in x).get('class')[1]

        
        books.append({
            'Book_Title': title,
            'Book_Price': price,
            'Book_Rating': rating,
            'Book_Stock_Availability': stockAvailability,
            'Book_URL': f'=HYPERLINK("{url}", "{url}")'
        })

#Var definition
TargetURL = 'https://books.toscrape.com/'
books = []
csvFilePath = '<localFilePath>'
#Get the HTML content from targetted site
response = requests.get(TargetURL)
htmlContent = BeautifulSoup(response.text, 'html.parser')

# scraping the home page
scrape_page(htmlContent, books)

# getting the "Next →" HTML element
next_li_element = htmlContent.find('li', class_='next')

# if there is a next page to scrape
while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']
    
    if "catalogue/" in next_page_relative_url:
        # getting the new page
        page = requests.get(TargetURL + next_page_relative_url)
    else:
        page =requests.get(TargetURL + "catalogue/" + next_page_relative_url)

    # parsing the new page
    soup = BeautifulSoup(page.text, 'html.parser')

    # scraping the new page
    scrape_page(soup, books)

    # looking for the "Next →" HTML element in the new page
    next_li_element = soup.find('li', class_='next')

# reading  the "books.csv" file and creating it
# if not present
csv_file = open(csvFilePath + '/books.csv', 'w', encoding='utf-8', newline='')
# initializing the writer object to insert data
# in the CSV file
writer = csv.writer(csv_file)

# writing the header of the CSV file
writer.writerow(['Book_Title', 'Book_Price', 'Book_Rating','Book_Stock_Availability',"Book_URL"])

# writing each row of the CSV       
for book in books:
    writer.writerow([book['Book_Title'], book['Book_Price'], book['Book_Rating'], book['Book_Stock_Availability'], book['Book_URL']])

# terminating the operation and releasing the resources
csv_file.close()



