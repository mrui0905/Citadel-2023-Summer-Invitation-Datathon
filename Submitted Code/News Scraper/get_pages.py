from helper_functions import *
import pandas as pd
import random


    
# we are going to check that this is the right filetype for the news website
# we know that article_link is not NULL
# this is the function that is going to return whether we should process a certain link or not
def process_individual(article_link, last_mod, file_type, domain):

    if "huffpost" in domain:
        return "entry" in article_link.text

    elif "cnbc" in domain:
        return file_type in article_link.text

    elif "dailymail" in domain:
        return file_type in article_link.text

    elif "cnn" in domain:
        return file_type in article_link.text

    elif "abcnews" in domain:
        return file_type in article_link.text

    else:
        exit()






# this function will go through and fetch some of the webpages that are in the
# csv file in the domain that we specify
# if we do not give it a number, then it fetches all of them
# use the variable urls to get the list that we want to be using
def fetch_pages(domain, amount_of_pages=0):

    articles_file = open("../News Sites Folders/{}/news_articles.csv".format(domain))

    # check that opening the file worked
    if articles_file is None:
        
        return
    
    urls = articles_file.readlines()

    # go through and pick a certain amount below
    if amount_of_pages <= 0:

        print(f"FETCHING all pages from {domain}")
        # we did not give it a valid amount of pages, so we get all of them
        # IMPLEMENT LATER

        articles_file = pd.read_csv("../News Sites Folders/{}/news_articles.csv".format(domain))
        global amount_of_false_article_processes

        for idx, row in articles_file.iterrows():
        
            link = row["link"]
        
            if "wbna" not in link:
        
                continue

            if amount_of_false_article_processes > 10:

                break
        
            time.sleep(random.random() * 3 + 1)

            response = get_html(link)

            if response is not None:

                title = process_nbcnews_page(response.content, domain, link)
                row["title"] = title

            else:

                amount_of_false_article_processes += 1

                articles_file.to_csv("../News Sites Folders/{}/news_articles.csv".format(domain), index = False)

            pass


        

            
    else:
    
        print(f"FETCHING {amount_of_pages} pages from {domain}")
        # first we read the csv that has all of the links to the articles that we are interested in

        temp_urls = []

        if amount_of_pages < len(urls):
            
            for i in range(amount_of_pages):

                temp_urls.append(urls[random.randint(0, len(urls))])

            urls = temp_urls


        else:

            # if the amount of pages that we are looking for is equal to or more than the 
            # length of the file that has all of our links then we want to just return everything

            amount_of_pages = len(urls)

            pass
    
    # now the amount_of_pages and the urls variables are updated so we are going to go ahead
    # and fetch each of the urls

    global amount_of_false_article_processes

    for set in urls:

        time.sleep(2)

        # this will return NULL if it is invalid and the page code otherwise
        url = set.split(',')[0]

        response = get_html(url)

        if response is not None:

            process_cnbc_page(response.content, domain, url)

        else:

            amount_of_false_article_processes += 1

            # print(response.content)

    print("WE FAILED ON {} ARTICLES".format(amount_of_false_article_processes))
