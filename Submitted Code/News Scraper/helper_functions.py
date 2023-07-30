import requests
import random
from bs4 import BeautifulSoup


# define a series of custom user agents that we can use
agents = [
    {'User-Agent': 'Mozilla/5.0; (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'},
    {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36'},
    {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1'},
    {'User-Agent': 'Mozilla/5.0 (iPhone9,4; U; CPU iPhone OS 10_0_1 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/14A403 Safari/602.1'},
]

# This function goes to the url that it is given and grabs the HTML from the webpage
# it uses the response package in python
def get_html(url):
    
    response = requests.get(url, headers=agents[random.randint(0, len(agents))], timeout=20)

    try:
        r_code = response.status_code
    except:
        print("FAILURE GETTING STATUS CODE")
        return None

    if r_code == 200:
        return response
    
    # elif r_code = 406:

    else:
        print(f"Error {r_code} for {url}")
        return None




# this creates the folder name that we are going to use based off of the url
# it is used to store the links from individual news websites
def get_folder_name(url):

    # Create the directory name
    folder_name = url.replace("https://", "").replace("www.", "").replace(".com", "").replace("/", "").replace(".my", "").replace(".indiatimes", "").replace(".go", "").replace(".net", "")
    folder_name = folder_name.replace("edition.", "")

    
    try:
        folder_name = folder_name[ : folder_name.index(".co")]
    except:
        pass

    return folder_name



# this is the function for specifically getting the article text from cnbc pages
def process_cnbc_page(response, domain, url):
    
    # cnbc has the entire article text stored in the json that we get back sometimes, so we are
    # going to parse through that data and get the actual article text
    response = response.decode('utf-8')

    print(response)

    # Find the script tag containing the desired JavaScript variable
    start_marker_1 = ',"articleBodyText":"'
    end_marker_1 = '","contentClassification'

    ticker_symbols = "\\\"tickerSymbols\\\":"
    stock_market_1 = '"symbol":"'
    stock_market_end_1 = '","tagName":"'
    stock_market_name_end = '","category":'

    # check if this is one of the valid articles
    if start_marker_1 not in response or end_marker_1 not in response:

        global amount_of_false_article_processes

        output_file = open("./News Sites Folders/{}/bad_article{}.txt".format(domain, amount_of_false_article_processes), "w")

        output_file.write(domain)
        output_file.write(url)
        output_file.write(response)

        return

    else:

        temp_stock_response = response

        # check if there are some stocks that are in the article
        if ticker_symbols in temp_stock_response:
            
            temp_stock_response = temp_stock_response[temp_stock_response.index(ticker_symbols) + len(ticker_symbols) : ]
            
            # check if the stock list is null
            if temp_stock_response[ : len("null")] != "null":

                print(temp_stock_response[ : temp_stock_response.index("]") + 1])

                # # go through each of the stocks that could be included
                # while stock_market_1 in temp_stock_response:

                #     print(f"{stock_market_1} is in response?\t{stock_market_1 in temp_stock_response}")
                #     if stock_market_1 not in temp_stock_response:
                #         print(temp_stock_response)

                #     stock_market_index = temp_stock_response.index(stock_market_1) + len(stock_market_1)
                #     temp_stock_response = temp_stock_response[stock_market_index : ]

                #     print(f"{stock_market_end_1} is in response?\t{stock_market_end_1 in temp_stock_response}")
                #     if stock_market_end_1 not in temp_stock_response:
                #         print(temp_stock_response)

                #     end_stock = temp_stock_response.index(stock_market_end_1)
                #     ticker = temp_stock_response[ : end_stock]

                #     print(f"{stock_market_name_end} is in response?\t{stock_market_name_end in temp_stock_response}")
                #     if stock_market_name_end not in temp_stock_response:
                #         print(temp_stock_response)

                #     end_name = temp_stock_response.index(stock_market_name_end)
                #     stock_name = temp_stock_response[end_stock + len(stock_market_end_1) : end_name]

                #     print(f"{ticker} :: {stock_name}")

        # the starting index of the article text
        start_index = response.index(start_marker_1)
        response = response[start_index + len(start_marker_1) : ]
        
        # the ending index of the article text
        end_index = response.index(end_marker_1)
        response = response[ : end_index]

        # print the article contents
        print()
        print()
        # print(domain)
        print(url)
        return response.replace("\"", "").replace("\\", "").replace(" ,", ",")



def process_nbcnews_page(response, domain, ur):

    try:

        response = BeautifulSoup(response, 'html.parser')

        first_headline = soup.find(class_='article-hero-headline__htag lh-none-print black-print')

        # Extract and return the text content from the first headline
        if first_headline:
            return first_headline.get_text().strip()
        else:
            return ""

    except:

        return ""
    