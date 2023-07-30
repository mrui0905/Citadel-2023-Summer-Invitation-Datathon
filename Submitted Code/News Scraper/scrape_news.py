from download_links import *
from get_pages import *
from helper_functions import *


#########################################################################
################## WELCOME TO THE NEWS SCRAPER PROGRAM ##################
#########################################################################

#########################################################################
# Author: Tristan Brigham
# Contact: tristan.brigham@yale.edu
# LinkedIn: https://www.linkedin.com/in/tristanb22/
#########################################################################

#########################################################################
# OVERVIEW

# The purpose of this program is to access a series of news websites' robots.txt files
# From there, we are able to download the links to most of the website's articles
# Then, we process each article so that we only end up with the resulting article text
# This can be used for things such as sentiment analysis on the news articles 

# A WORD OF CAUTION: Scraping websites and hindering their performance can be against terms
# of service, and in cases where you deny other users access to the website, against
# the Computer Fraud and Abuse Act. Be careful and respectful when scraping anything,
# as although it is openly accessible information, it costs websites to host and 
# produce this information. Do not create an undue burden or additional cost for them
# by overloading their servers or stealing their data for resale. They will ban/rate-limit you,
# and could pursue legal action in serious cases. Be respectful, and compensate people for their work when you can.

# TLDR; don't scrape unless you know what you are doing. Even then, don't be a bad guy :)
#########################################################################



#########################################################################
# HOW DOES IT WORK

# This program works by getting the sitemaps of website domains which allow us to access them,
# and then indexing all of the links that are associated with those sitemaps in excel files.
# Domains are incentivized to make sure that their sitemaps have links to every portion
# of their website that they want search engines to index which includes everything
# in the case of news websites as that is how they fundamentally drive revenue.

# The program ignores any websites that are image or video repositories as they are not
# valuable to us as of now -- only print websites are helpful given we don't
# have the bandwidth to process video

#########################################################################


## TO DO:
# implement multi threading so that each thread can focus on a news website and not overwhelm it
# the csv file that I am reading from should include the folder name and the ending to the website
# make it so that we do not have to store the start of ever article link if they are all the same

### SETTINGS
debugging = False
S_GETTING_LINKS = False
path_to_company_csv = "/Users/tristanbrigham/Desktop/Self Study/Computer Science/News Scraper/news_sites.csv"
# path_to_company_csv = "/Users/tristanbrigham/Desktop/Self Study/Computer Science/News Scraper/test_link.csv"
link_starts_file = "article_preambles.csv"
sitemap_string = "Sitemap: "
list_of_banned_words = ["video", "quote"]   # if you see any of these words in the url, don't grab that url
amount_of_false_article_processes = 0



# THE MAIN FUNCTIONALITY OF THE PYTHON PROGRAM
if __name__ == "__main__":

    # check if we should only be getting website links
    if S_GETTING_LINKS:
        threads_get_links()
        # download_robots()

    else:

        fetch_pages("nbcnews", amount_of_pages=-1)