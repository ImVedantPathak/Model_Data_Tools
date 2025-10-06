import requests
from bs4 import BeautifulSoup
from measure_bit_rate import measure_bit_Rate
from AdminComs import STORM_SDK as STORM


def gutenberg_data(books:int,gap:int):
    for book in range(gap,gap+books):
        url = f"https://www.gutenberg.org/cache/epub/{book}/pg{book}.html"
        try:
            response = requests.get(url)
            response.raise_for_status()
            html = response.text
            
            soup = BeautifulSoup(html, "html.parser")
            # print(soup.prettify())
            
            with open(f"GutenbergBooks/gutenberg_book_{book}.html",'w',encoding='utf-8') as f:
                f.write(soup.prettify())
            
            # return html    
            # @measure_bit_Rate # only for pipeline
            # STORM.send_to_pipeline_instance(soup)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page: {e}")

if __name__ == "__main__":
    books = 100 #careful, gutenberg might not even have that many books, or some books may not exist
    gutenberg_data(books,gap=100)