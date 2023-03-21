import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin

def create_directory(url):
    """Create necessary directories for website"""
    o = urlparse(url)
    domain_name = o.netloc
    path_name = o.path.strip('/')
    if not path_name:
        path_name = 'index.html'
    else:
        path_name = path_name.replace('/', '_')
    directory_name = domain_name + '_' + path_name

    parent_directory = 'Sites'
    if not os.path.exists(parent_directory):
        os.makedirs(parent_directory)

    full_directory = os.path.join(parent_directory, directory_name)
    if not os.path.exists(full_directory):
        os.makedirs(full_directory)

    return full_directory

def download_assets(url, directory_name):
    """Download CSS, JS, and image files used on website"""
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    # Download HTML file
    with open(os.path.join(directory_name, 'index.html'), 'wb') as f:
        f.write(r.content)

    for link in soup.find_all('link'):
        href = link.get('href')
        if href and href.endswith('.css'):
            filename = href.split('/')[-1]
            css_url = urljoin(url, href)
            r = requests.get(css_url)
            with open(os.path.join(directory_name, filename), 'wb') as f:
                f.write(r.content)

    for script in soup.find_all('script'):
        src = script.get('src')
        if src and src.endswith('.js'):
            filename = src.split('/')[-1]
            js_url = urljoin(url, src)
            r = requests.get(js_url)
            with open(os.path.join(directory_name, filename), 'wb') as f:
                f.write(r.content)

    for img in soup.find_all('img'):
        src = img.get('src')
        if src:
            filename = src.split('/')[-1]
            img_url = urljoin(url, src)
            r = requests.get(img_url)
            with open(os.path.join(directory_name, filename), 'wb') as f:
                f.write(r.content)

if __name__ == '__main__':
    url = input('Enter URL to scrape: ')
    directory_name = create_directory(url)
    download_assets(url, directory_name)
    print('Download complete.')
