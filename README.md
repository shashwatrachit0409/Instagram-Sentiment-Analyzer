Project Instagram Sentiment Analyzer is python based project made using the flask as a framework.
It scrape data using the automation tool selenium and beautifulsoup
It analyzes sentiment of the all the public profile post using the hashtags and captions used in the post using the library named TextBlob
It's limitation is that it can scrape upto 10 post per account and can scrape only few profile at a time
Scraping many times at a particular point of time can make the website banned by instgram due to instagram security policy

File Structure

instagram-analyzer (main folder)
|_app.py
|_scraper.py
|_sentiment_utils.py
|_templates (folder name)
  |_index.html
  |_filter.html
  |_results.html
