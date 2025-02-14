# E-commerce Crawler
Building a crawler which can crawl through all the pages of an e-commerce website and find out the product pages present in that website. This crawler is scalable and efficient at handling multiple different types of product pages and websites.

## Prerequisites
- Clone this GitHub project
- Create a python virtual environment and activate it (optional) \
  Steps: https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/
- Install all the required python packages: \
  `pip install -r requirements.txt`

## Steps to run the application
- Update the list of domains in `main.py` you would like the crawler to crawl for product pages
- Open `ecommerce_crawler.py` and update `product_url_patterns` to add/remove regex which would be used for the crawler to determine where a url is product url or not
- Save the changes and run the following command in your terminal to start the application: \
  `python3 main.py`

## Improvements areas
- The crawler is still slow and can take from a few minutes to hours for a large website. We could parallelize the work in order to gain significant performance benefits
- Currently, the start url is the home page for that website. While this can be a good enough starting point for most cases, we could improve and help crawler to find more pages by using sitemap of a website as a starting point
- Current solution doesn't do well with dynamically loading content (like infinite scrolling websites). Handling such edge cases would be critical to ensure crawler can find all product pages effectively