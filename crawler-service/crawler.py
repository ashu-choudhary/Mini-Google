# crawler-service/crawler.py
import requests
from bs4 import BeautifulSoup
import redis
import time
import os

# --- Configuration ---
# Connect to the Redis instance running in Docker.
# The hostname 'redis' is used because Docker Compose creates a network
# where services can be reached by their service name.
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = 6379
URL_QUEUE_KEY = "url_queue" # The list in Redis holding URLs to crawl
VISITED_URLS_KEY = "visited_urls" # The set in Redis holding already crawled URLs

# --- Connect to Redis ---
try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)
    redis_client.ping()
    print("Successfully connected to Redis.")
except redis.exceptions.ConnectionError as e:
    print(f"Could not connect to Redis: {e}")
    exit(1)


def add_seed_urls(urls):
    """Adds the initial set of URLs to the queue if the queue is empty."""
    if redis_client.llen(URL_QUEUE_KEY) == 0:
        print(f"Queue is empty. Seeding with initial URLs: {urls}")
        redis_client.lpush(URL_QUEUE_KEY, *urls)

def crawl(url):
    """
    Fetches a single URL, extracts its text and links,
    and sends the data to other services (in a real system).
    """
    # Use a set for visited URLs for fast lookups
    if redis_client.sismember(VISITED_URLS_KEY, url):
        print(f"Already visited: {url}")
        return

    print(f"Crawling: {url}")
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return

    # Mark as visited
    redis_client.sadd(VISITED_URLS_KEY, url)

    soup = BeautifulSoup(response.content, 'html.parser')

    # --- Extract Text ---
    # A simple approach: get all text from the body
    text_content = soup.body.get_text(separator=' ', strip=True)
    # In a real system, you would send this to the indexer service.
    # For now, we'll just print a snippet.
    print(f"  -> Extracted Text (first 100 chars): {text_content[:100]}...")

    # --- TODO: Send to Indexer ---
    # This is where you would publish the content to another queue
    # for the indexer-service to process.
    # For example: redis_client.publish('text_to_index', {'url': url, 'text': text_content})


    # --- Extract Links and Add to Queue ---
    new_links_found = 0
    for link in soup.find_all('a', href=True):
        href = link['href']
        # Basic link cleaning and validation
        if href.startswith('http'):
            # Add new, unvisited links to the queue
            if not redis_client.sismember(VISITED_URLS_KEY, href):
                redis_client.lpush(URL_QUEUE_KEY, href)
                new_links_found += 1
    print(f"  -> Found and queued {new_links_found} new links.")


def main():
    """Main loop for the crawler."""
    # Add some starting points for the crawl
    add_seed_urls([
        "https://www.google.com",
        "https://www.wikipedia.org",
        "https://www.python.org"
    ])

    while True:
        # Block until a URL is available in the queue
        # rpop is atomic, so multiple crawlers won't get the same URL
        url_to_crawl = redis_client.rpop(URL_QUEUE_KEY)

        if url_to_crawl:
            crawl(url_to_crawl)
        else:
            print("URL queue is empty. Waiting for new URLs...")
            time.sleep(10) # Wait before checking again

        # Be a polite crawler
        time.sleep(1)

if __name__ == "__main__":
    main()
