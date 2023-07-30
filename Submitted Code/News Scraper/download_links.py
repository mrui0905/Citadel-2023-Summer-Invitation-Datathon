from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time
import requests
import csv
import os
import random
import threading
import json

# importing the settings from my other python file (the main one)
from scrape_news import debugging, path_to_company_csv, link_starts_file, sitemap_string, list_of_banned_words, amount_of_false_article_processes

# importing helper functions
from helper_functions import get_html, get_folder_name



# this runs threads to get the links from a bunch of different news sites that we are interested in
# this is the master function that we are going to be running to get all of the information
def threads_get_links():

    thread_list = []

    # run the program so that we have a thread working on each of the websites that we are interested in
    with open(path_to_company_csv, 'r') as company_csv:
            
        # Create a CSV reader object
        reader = csv.reader(company_csv)
        
        # skip the first line
        next(reader)

        # Read each row of the CSV file
        for link in reader:

            # create a thread to focus on each of the websites
            my_thread = threading.Thread(target=get_sitemaps_base, args=[link])
            my_thread.start()
            thread_list.append(my_thread)

    # now wait for all of them to finish
    for thread in thread_list:
        thread.join()





# this function is an iterative function to traverse through sitemaps and get the data
# @folder_name is the name of the folder that we are operating in
# @sitemap_link is the link to the sitemap that we should consider
# @csv_writer is the writer of the csv file that we want to append to
def iterate_sitemaps(folder_name, sitemap_link, file_type, csv_writer):

    # so that we do not overwhelm the website
    time.sleep(random.random() * 1)

    # printing the link that we are looking at
    # print(sitemap_link)

    # get the data from the sitemap link
    # response = requests.get(sitemap_link)
    response = requests.get(sitemap_link, timeout=20)

    try:
        code = response.status_code
    except:
        print("FAILURE GETTING STATUS CODE")
        return

    if response.status_code != 200:
        print(f"Error {response.status_code} for {sitemap_link}")
        return

    # ok the data should be good after our checks
    # we are going to search again for more sitemap instances
    # print(response.text)

    # search for all sitemap instances
    soup = BeautifulSoup(response.content, features="xml")


    # Find all instances of the sitemap class so that we can continue to iterate on those
    sitemaps = soup.find_all('sitemap')

    for link in sitemaps:

        inside_text = link.find_all("loc")

        # Iterate over each child element
        for child in inside_text:

            process = True

            # if this is trying to access a sitemap that we are uninterested in, then skip
            for naughty_word in list_of_banned_words:
                if naughty_word in child.text.strip().lower():
                    process = False
            
            try:
                # Access the contents of the child element and iterate
                if process:
                    if child is None or child.text is None:
                        print("NONE: {}".format(child.text))
                        continue

                    # process the link to the xml file
                    print(f"PROCESSING:\t{child.text.strip()}")
                    iterate_sitemaps(folder_name, child.text.strip(), file_type, csv_writer)

                else:
                    print(f"NOT PROCESSING:\t{child.text.strip()}")

                pass

            except Exception as e:
                print(f"ERROR PROCESSING {child.text} :: {str(e).strip()}")

    
    # now find all of the insances of urls so that we can also explore those
    urls = soup.find_all('url')

    for link in urls:

        last_mod = ""
        date = ""

        # try to get the article link
        try:
            article_link = link.find_all("loc")[0]
        except:
            print(f"Couldn't find the link for {link.text.strip()}")
            continue

        # if this is a nonetype then we skip
        if article_link is None or article_link.text is None:
            continue

        # now see if we can get the date
        try:
            last_mod = link.find_all("lastmod")[0]
        except:
            
            try:
                last_mod = link.find_all("news:publication_date")[0]
                
            except:
                last_mod = ""

        # try to get the publicatin datae of the article (Bloomberg)
        # try:
        #     date = link.find_all("news:title")[0]
        
        # except:
        #     date = ""

        # Iterate over each child element
        # Access the contents of the child element and iterate
        try:

            if isinstance(article_link, str):
                a_l = article_link.strip()
            
            else:
                a_l = article_link.text.strip()

            
            # if we are struggling with the date
            if last_mod == "":
                # csv_writer.writerow([a_l, ""], date)
                csv_writer.writerow([a_l, ""])
            else:
                # csv_writer.writerow([a_l, last_mod.text], date)
                csv_writer.writerow([a_l, last_mod.text])


        except Exception as e:
            print(f"ERROR ON {article_link.text.strip()} :: {str(e)} :: {type(article_link)}")





# this function goes through and gets the robots.txt page
def download_robots():
    # Open the CSV file
    with open(path_to_company_csv, 'r') as file:
        
        # Create a CSV reader object
        reader = csv.reader(file)

        # skip the first line
        next(reader)
        
        # Read each row of the CSV file
        for link in reader:
            
            # get the robots file and print
            response = get_html("{}robots.txt".format(link[0]))
            # response = get_html(link[0])

            if response is not None:

                folder_name = get_folder_name(link[0])

                with open("../News Sites Folders/{}/robots.txt".format(folder_name), 'w') as file:
                    file.write(response.text)
                    # print(response.text)
                
                # try:
                #     # os.makedirs("./News Sites Folders/{}".format(folder_name))
                #     # Open the file in write mode and pipe the string to it
                # except:
                #     pass

                pass


# now go through each of the files
# we are going to grab all of the links that might be of interest to us
def get_sitemaps_base(link):

    # get the name of the folder that we are operating in
    folder_name = get_folder_name(link[0])

    # open the csv file so that we can write to it
    print(f"ANALYZING:\t{folder_name}")

    csv_file = open("../News Sites Folders/{}/news_articles.csv".format(folder_name), "w")
    csv_writer = csv.writer(csv_file)


    with open("../News Sites Folders/{}/robots.txt".format(folder_name)) as f:

        for line in f.readlines():

            # check if this is a link to a sitemap in the robots.txt file
            if sitemap_string.lower() in line.lower():
                
                try:
                    iterate_sitemaps(folder_name, line[line.index(sitemap_string) + len(sitemap_string) : ].strip(), link[1].strip(), csv_writer)

                except Exception as e:
                    print(f"ERROR ITERATING :: {line} {str(e)}")
                    print(f"* : {line[line.index(sitemap_string) + len(sitemap_string) : ].strip()}")
                    print(f"* : {link[1].strip()}")

        # print(folder_name)
    
    # finally go through and drop the duplicates
    csv_file.close()

    # Check if the file is empty or not
    with open("../News Sites Folders/{}/robots.txt".format(folder_name), 'r') as file:
        first_line = file.readline()
        if not first_line:
            print("Error: The file is empty.")
        else:
            # Read the CSV file
            print("DROP DUPS:\t../News Sites Folders/{}/news_articles.csv".format(folder_name))
            df = pd.read_csv("../News Sites Folders/{}/news_articles.csv".format(folder_name))

            # Remove duplicates
            deduplicated_df = df.drop_duplicates()

            # Write the deduplicated data back to the CSV file
            deduplicated_df.to_csv('../News Sites Folders/{}/news_articles.csv'.format(folder_name), index=False)

  

           


def personalized_check_link(link):

    if "usatoday" in link:

        return "story" in link



  