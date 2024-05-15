#!/usr/bin/env python3
""" expiring web cache module """

import requests
import redis
import time

# Initialize Redis connection
r = redis.Redis()


def get_page(url: str) -> str:
    count_key = f"count:{url}"
    page_key = f"page:{url}"

    # Increment the access count for the URL
    r.incr(count_key)

    # Check if the page content is already cached
    cached_page = r.get(page_key)
    if cached_page:
        return cached_page.decode()

    # Fetch the HTML content from the URL
    response = requests.get(url)
    page_content = response.text

    # Cache the page content with an expiration time of 10 seconds
    r.setex(page_key, 10, page_content)

    return page_content


# Test the get_page function
url = "http://slowwly.robertomurray.co.uk/delay/5000/url/http://www.google.com"
html_content = get_page(url)
print(html_content)
