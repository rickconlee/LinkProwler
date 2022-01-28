import json 
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama
#from requests_html import HTMLSession
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import argparse

# grab command line argument for the target site we will crawl for links.
parser = argparse.ArgumentParser(description='Scraping Target')
parser.add_argument('--url', dest='target_url', type=str, help='Target URL to scrape for URLs')
parser.add_argument('--selenium', dest='selenium_url', type=str, help='URL of Selenium Instance in http(s)://URL:PORT format')
args = parser.parse_args()

# Read some inputs from a config file...
with open('scrapeconfig.json') as config_file:
    scrape_config = json.load(config_file)

# init the colorama module
colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# initialize the set of links (unique links)
internal_urls = set()
external_urls = set()

# number of urls visited so far will be stored here
total_urls_visited = 0

def grab_page_selenium(target):
    """
    Uses Selenium to grab a page to process for links. 
    """
    # Specify the options that we want for Selenium
    options = Options()
    options.add_argument("--headless")
    options.add_argument('--disable-dev-shm-usage') 
    options.add_argument("--window-size=1024,768")
    options.add_argument("--disable-notifications")
    options.add_argument("--incognito")
    driver = webdriver.Remote(options=options, command_executor=args.selenium_url, keep_alive=True)
    driver.get(target)
    # Store page source in variable so we can hand it off. 
    html = driver.page_source
    driver.quit()
    
    return html

def is_valid(url):
    """
    Checks whether `url` is a valid URL.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def get_all_website_links(url):
    """
    Returns all URLs that is found on `url` in which it belongs to the same website
    """
    # all URLs of `url`
    urls = set()
    # domain name of the URL without the protocol
    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(grab_page_selenium(target=url), "html.parser")

    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            # href empty tag
            continue
        # join the URL if it's relative (not absolute link)
        href = urljoin(url, href)
        parsed_href = urlparse(href)
        # remove URL GET parameters, URL fragments, etc.
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            # not a valid URL
            continue
        if href in internal_urls:
            # already in the set
            continue
        if domain_name not in href:
            # external link
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls

def crawl(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in `external_urls` and `internal_urls` global set variables.
    params:
    max_urls (int): number of max urls to crawl, default is 30.
    """
    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        time.sleep(3)
        crawl(link, max_urls=max_urls)

if __name__ == "__main__":

    time_int = int(time.time())
    crawl(args.target_url)
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
    # Convert the sets to something that we can do with JSON
    internal_url_list = list(internal_urls)
    external_url_list = list(external_urls)
    # Serialize into JSON so we can store it for later 
    json_data1 = {
        "Internal URLs":internal_url_list,
        "External URLs":external_url_list
    }
    # Write everything to a JSON file so we can process the results outside this module
    with open(f'crawls/{time_int}-urlscrawled.json', 'w', encoding='utf-8') as f:
        json.dump(json_data1, f, ensure_ascii=True, indent=4)
