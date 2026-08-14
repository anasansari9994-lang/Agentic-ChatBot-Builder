from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import requests

def crawl_website(start_url, max_depth=10):
    visited = set()
    to_visit = [start_url]
    domain = urlparse(start_url).netloc
    scraped_data = []

    while to_visit and len(visited) < max_depth:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue
        visited.add(current_url)
        try:
            response = requests.get(current_url, timeout=10)
            if response.status_code != 200 or 'text/html' not in response.headers.get(
                'content-type', ''
            ):
                continue
            visited.add(current_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            for element in soup(['script', 'style', 'navigate', 'header', 'footer', 'aside']):
                element.decompose()
            text = soup.get_text(separator=' ', strip=True)
            title = soup.title.string if soup.title else current_url
            scraped_data.append(
                {
                    'url' : current_url, 'title' : title, 'content' : text
                }
            )

            for link in soup.find_all('a', href=True):
                absolute_url = urljoin(current_url, link['href'])
                parsed_link = urlparse(absolute_url)
                clean_url = (
                    f'{parsed_link.scheme}://{parsed_link.netloc}{parsed_link.path}'
                )
                if (
                    parsed_link.netloc == domain
                    and clean_url not in visited
                    and clean_url not in to_visit
                ):
                    to_visit.append(clean_url)
        except Exception as e:
            print(f'Error crawling {current_url}: {e}')

    return scraped_data