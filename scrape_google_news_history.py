"""
Title:  Get Google News History
Desc:   Get historical news stories from Google
Author: Yassin Eltahir
Date:   2017-08-21
"""

import datetime
import google_news_scraper as gnews
import time
import itertools
import pandas as pd
import random

# Build dates to search across
def date_seq(start, end):
    
    """
    Builds a sequence of dates
    
    :param start(str): Start date of format 'YYYY-mm-dd'
    :param end(str): End date of format 'YYYY-mm-dd'
    
    :return: List of dates 
    """
    
    # Calculate Time difference
    start_date = datetime.datetime.strptime(start, '%Y-%m-%d')
    end_date = datetime.datetime.strptime(end, '%Y-%m-%d')
    date_diff = end_date - start_date
    
    # Build out list of dates
    date_list = [end_date - datetime.timedelta(days=x) for x in range(0, date_diff.days + 1)]
    date_list = [datetime.datetime.strftime(x,'%Y-%m-%d') for x in date_list]     
    
    return date_list



# Build Variables For Loop
date_range = date_seq('2017-01-01','2017-08-21')
search_terms = ['cryptocurrency','bitcoin','ethereum']
driver_location = r'C:\Users\Yass\Downloads\chromedriver.exe'


# For each search term combination, scrape 100 results
for date, term in itertools.product(date_range, search_terms):
    
    # Get Results
    search_url = gnews.google_news_url(term, date, date, num_results= 100, language='en', sort = 'n')
    search_results = gnews.get_search_results(search_url, driver_location)
    
    # Convert to a dataframe, append the date and save to disk
    results_df = pd.DataFrame(search_results)
    results_df['date'] = date
    results_df['search_term'] = term
    results_df.to_csv(r'C:\Users\Yass\Documents\CryptoData\google_news_history.csv',sep='|', mode = 'a', header=False, encoding='utf-8', index=False)    
    
    # Sleep for a random amount of time. Hopefully this minimises the chances of getting blocked
    sleep_secs = random.randint(30, 240)
    print "{}: Scraped for {} on {}".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'), term, date)
    print "Sleeping for {} seconds".format(sleep_secs)
    time.sleep(sleep_secs)
    
