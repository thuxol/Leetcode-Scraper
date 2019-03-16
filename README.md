## Leetcode-Scraper
This script attempts to connect to leetcode.com and download the source code for all accepted submission of a user.
As leetcode has a lot of dynamically generated, selenium is used to facilitate scraping. 


#### Requirements
- Python 3.6
- Selenium
- Chromedriver
- BeautifulSoup
#### Execution
First, update the login info inside the script:
```python
# TODO: replace this by your account info
NAME = ''
PASSWORD = ''
```
Then simply run it via:
```sh
$ python scrape.py
```
This should save source code fo  __all__ your accepted submissions (including multiples for each question) in a subfolder `/leetcode_solutions`, organised by question title and number.

#### Remarks
There are a number of similar projects out there, in particular https://github.com/jrluu/Leetcode-Scraper and https://github.com/b1ns4oi/Leetcode-crawler were helpful. However, presumably because of changes to the leetcode site, neither of those appear to work anymore.