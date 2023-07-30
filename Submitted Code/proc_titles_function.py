import os
import re
import pandas as pd
import datetime
from datetime import timedelta
from dateutil.parser import parse

link_dict = {
    "bloomberg" : ('-', ["opinion", "news", "en", "features", "politics"], "y-m-d") ,
    "cnbc" : ('-', ["html"], "y/m/d") ,
    "dailymail" :  ('-', ["html"], "") ,
    "foxnews" :  ("-", ["weather", "area-51", "official-polls", "austin", "apps-products-ios", "tech", "fox-and-friends", "family", "fox-friends", "faith-values", "great-outdoors", "slack-success", "health", "lifestyle", "miami", "midterms-2018", "slack-app", "nyc", "newsletters", "about", "compliance", "auto", "politics", "story", "donotsell", "shows", "food-drink", "real-estate", "travel", "updates", "gowatch", "recordkeeping", "transcript", "cw-the-real-texas-rangers", "instant-access", "person", "whats-changed", "newsletters-coronavirus", "chicago", "opinion", "science", "sports", "uncategorized", "sunday-morning-futures", "world", "fox-news", "story", "us", "entertainment"], "") ,
    "nypost" : ("-", '', "y/m/d") ,
    "thedailybeast" : ('-', "", "") ,
    "theglobeandmail" : ("-", "", "") ,
    "usatoday" : ('-', "", 'y/m/d') ,
    "cnn" :  ('-', ["html"], 'y/m/d') ,
    "bbc" :  ('_', "", 'y/m/d') ,
    "nytimes" : ('-', ['html'], "y/m/d") ,
    "washingtonpost" : ('-', '', "") ,
    "dailystar" : ('-', '', "") ,
    "huffpost" : ('-', ["entry"], "") ,
}


path_to_news = "/Users/tristanbrigham/Desktop/Self Study/Computer Science/News Scraper/News Sites Folders/"
path_to_article_titles = "/Users/tristanbrigham/Desktop/Citadel Datathon/Articles_titles/"
col_headers = ["link", "date"]

# how many days after the end of a natural disaster to consider an article hit
days_to_add = 60
days_to_sub = 50
random_year = 2025


# define a function to open the csv and then return the dataframe
def get_article_links(name):

    links_df = pd.read_csv(path_to_news + name + "/news_articles.csv", header=None, index_col=False)
    links_df.columns = col_headers

    # print(links_df.head(5))

    return links_df


# this is meant to parse the link and try to find a date in the case that the article doesn't have one
def get_date(link, args):

    try:

        date_format = args[3]

        if date_format == "":

            return ""
        
        # now we can assume that there is a date format
        # search the link for a date (only considering 2000 and beyond)
        date_idx = link.index("20")

        # check if this is a random 20 or not
        if link[date_idx + 4 != args[3][1]]:

            return ""

        # assume that this is not a random 20
        date = link[date_idx : date_idx + 10]

        return date

    except:

        # print(f"Couldn't find date: {link}")
        return ""
    

# this function takes the title and splits it based off of the arguments provided
def split_title(link, args):

    out = link.split(args[0])

    out = " ".join(out).replace("https://www.cnbc.com/", "").replace(".html", "").replace("https://www.bloomberg.com/", "").replace("https://www.theglobeandmail.com/", "").replace("https://www.thedailybeast.com/", "").replace("https://nypost.com/", "").replace("https://www.foxnews.com/", "").replace("https://www.bbc.com/", "").replace("https://www.dailymail.co.uk/", "").replace("edition.", "").replace("https://cnn.com/", "").replace("https://www.usatoday.com/", "").replace("https://www.huffingtonpost.com/", "").replace("https://www.washingtonpost.com/", "").replace("https://www.nytimes.com/", "").replace("https://www.dailystar.co.uk/", "")

    out = out.split("/")

    return " ".join(out)


def count_words_in_string(word_array, target_string):
    common_words = [word for word in word_array if word in target_string]
    return len(common_words)


# this function checks whether the title of the news article that it is passed has any of the words that might indicate weather event
# this is done in two ways -- first, we are looking for any words that are in the list that we have passed it below
# second, we are looking for the names of any storms 
def check_weather(link):

    weather_words = ['storm', 'hurricane', 'typhoon', 'tornado', 'cyclone', 'thunderstorm', 'flood', 'drought', 
    'heat', 'cold', 'snowstorm', 'blizzard', 'hailstorm', 'monsoon', 'rainfall', 'snowfall', 'temperature', 
    'earthquake', 'tsunami', 'volcano', 'wildfire', 'landslide', 'avalanche', 'eruption', 'seismic', 'environment', 
    'climate change', 'biodiversity', 'deforestation', 'ozone', 'sunny', 'cloudy',
    'windy', 'rainy', 'snowy', 'overcast', 'humid', 'foggy', 'aurora', 'eclipse', 'meteor', 'comet', 'solar', 
    'flare', 'lightning', 'precipitat', 'drizzle', 'sleet', 'muggy', 'breezy', 'gust', 'heat', 'wind', 'dew', 
    'barometer', 'thermometer', 'anemometer', 'forecast', 'atmospheric', 'pressure', 'uv', 'index', 
    'seismology', 'aftershock', 'fault line', 'evacuation', 'emergency', 'disaster', 'relief', 'catastrophe', 
    'resilience', 'preparedness', 'shelter', 'disaster recovery', 'warm front', 'cold front', 'weather system', 
    'isobar', 'microclimate', 'atmospheric conditions', 'weather patterns', 'climate patterns', 
    'aurora borealis', 'northern lights', 'aurora australis', 'southern lights', 'meteor shower', 
    'solar', 'eclipse', 'lunar', 'eclipse', 'gravity wave', 'cosmic', 'rays', 'coronal mass ejection', 'snowfall', 
    'snowstorm', 'blizzard', 'snowdrift', 'snowflake', 'frost', 'ice', 'snowbank', 'slush', 'snowmelt', 
    'hail', 'winter', 'frosty', 'winter wonderland', 'polar vortex', 'snow', 'snow-capped', 'avalanche', 'whiteout', 
    'rainfall', 'showers', 'downpour', 'drizzle', 'cloudburst', 'deluge', 'rainstorm', 'raindrops', 'precipitation', 
    'thunderstorm', 'monsoon', 'rainy', 'wet', 'rain', 'rain gauge', 'rain cloud', 'drenching rain', 'rain shower', 
    'rainy season', 'rain boots', 'raincoat', 'windy', 'breezy', 'gust', 'gale', 'zephyr', 'bluster', 'whirlwind', 
    'cyclone', 'tornado', 'twister', 'tempest', 'windstorm', 'wind chill', 'windy weather', 'anemometer', 'wind', 
    'wind speed', 'wind', 'farm', 'wind', 'energy', 'system', 'pattern', 'atmospheric', 'condition', 
    'forecast', 'meteorology', 'front', 'weather']

    # now check if the name of any storms exists
    storm_words = [
        'iniki', 'opal', 'sandy', 'imelda', 'isidore', 'michael', 'hugo', 
        'katrina', 'nicholas', 'storm', 'flood', 'irma', 'matthew', 'wildfire', 'elena', 
        'ian', 'harvey', 'allison', 'georgia', 'alberto', 'ike', 'blizzard', 'floods', 'isaac', 'allen', 
        'tropical', 'hanna', 'fire', 'cold', 'dorian', 'storm', 
        'hail', 'ice', 'jeanne', 'blizzard', 'hurricane', 'dolly', 'fiona', 'laura', 'delta', 
        'maria', 'isabel', 'lee', 'midwest/ohio', 'isaias', 'kansas', 'irene', 'wave', 'england', 'storm,', 
        'drought', 'heat', 'ivan', 'charley', 'floyd', 'ida', 'drought', 'andrew', 'flooding', 'gustav', 
        'erin', 'elsa', 'dennis', 'nicole', 'zeta', 'fran', 'heat', 'lili', 'georges', 'tornado', 'midwest', 
        'fred', 'juan', 'wilma', 'derecho,', 'marilyn', 'rita', 'sally', 'bob', 'firestorm', 'eta', 'gloria', 
        'derecho', 'winter', 'wildfires', 'alicia', 'freeze', 'bonnie', 'flash'
        ]

    
    # for word in storm_words:

    #     if word.lower() in link.lower():

            # print(f"STORM: {word}")

    # print(f"storm: {any(word.lower() in link.lower() for word in storm_words)}")
    # print(f"weather: {any(word.lower() in link.lower() for word in weather_words)}")

    pattern = r"[!@#$%^&*()\-_=+[{\]};:'\",<.>/?\\|`~]"

    # Use re.sub() to replace the special characters with spaces
    link = re.sub(pattern, ' ', link)

    return any(word in [x.lower() for x in link.split(" ")] for word in storm_words) or any(word in [x.lower() for x in link.split(" ")] for word in weather_words)

        
    
    
def get_type_disaster(link):

    pattern = r"[!@#$%^&*()\-_=+[{\]};:'\",<.>/?\\|`~]"

    # Use re.sub() to replace the special characters with spaces
    link = re.sub(pattern, ' ', link)

    types_disasters = ["Drought", "Cold", "Storm", "Fire", "Flood", "Cyclone"]

    drought_dict = ['drought', 'arid', 'dry', 'thirst', 'parched', 'waterless', 'scorching', 'heatwave', 'dehydrated', 'desiccated', 'dusty', 'cracked', 'barren', 'hot', 'thirsty', 'withered', 'deficit', 'scorched', 'rainless', 'shrinking', 'severe', 'lack', 'aridity', 'desert', 'water shortage', 'scarcity', 'heat', 'crop failure', 'dryness', 'famine', 'wildfire', 'shortage', 'water crisis', 'water stress', 'water rationing', 'waterless', 'dry spell', 'dustbowl', 'crop loss', 'thirsty crops', 'parch', 'crop damage', 'drying', 'water conservation', 'rainfall deficiency', 'desertification', 'heat stress', 'reservoir levels', 'water depletion', 'hydrological drought']
    cold_storm_dict = ['snowstorm', 'blizzard', 'frosty', 'chills', 'icy', 'snowy', 'brr', 'snowflakes', 'freeze', 'flurries', 'sleet', 'slush', 'frost', 'icicles', 'polar', 'arctic', 'whiteout', 'cold', 'wintry', 'snowfall', 'winter', 'snowbound', 'snowpack', 'hail', 'drifts', 'freeze', 'winterize', 'snowmageddon', 'snowbanks', 'chill', 'frostbite', 'snowslide', 'hibernation', 'frigid', 'snowcap', 'snowmobile', 'snowshoes', 'snowplow', 'snowman', 'avalanche', 'powder', 'slippery', 'shiver', 'iciness', 'snowscape', 'snowbelt', 'snowball', 'winterize', 'snowy', 'cold snap']
    other_storm_dict = ["Storm", "Thunder", "Rain", "Flash", "Hail", "Wind", "Flood", "Clouds", "Lightning", "Snow", "Sleet", "Tornado", "Gales", "Downpour", "Squall", "Deluge", "Blustery", "Cyclone", "Tempest", "Drizzle", "Monsoon", "Cloudburst", "Whirlwind", "Typhoon", "Hurricane", "Drench", "Shower", "Torrent", "Wet", "Thunderclap", "Rainfall", "Snowfall", "Stormy", "Gusts", "Thunderhead", "Lightning strike", "Rumble", "Frost", "Mist", "Polar", "Gale-force", "Fog", "Twister", "Blizzard", "Snowflake", "Sleet", "Wetness", "Lightning bolt", "Flooded", "Cyclonic",  ]
    fire_dict = ['fire', 'blaze', 'inferno', 'flame', 'wildfire', 'burn', 'hot', 'smoke', 'heat', 'combustion', 'charred', 'ash', 'ember', 'scorch', 'smolder', 'ignite', 'flare', 'sear', 'scorched', 'incinerate', 'pyre', 'kindle', 'singe', 'conflagration', 'heatwave', 'flaming', 'fiery', 'spark', 'sizzle', 'blaze up', 'firestorm', 'burning', 'flameout', 'bonfire', 'incendiarism', 'flashfire', 'infernal', 'engulf', 'arson', 'firefighting', 'firefighter', 'blazing', 'ignition', 'fireball', 'fireproof', 'smoky', 'cinders', 'firetruck', 'combustible', 'flamingo']
    flood_dict = ['flood', 'deluge', 'inundation', 'water', 'overflow', 'surge', 'submerge', 'swell', 'torrent', 'overflowing', 'rains', 'flash flood', 'waterlogged', 'dam', 'flooding', 'soaked', 'river', 'flooded', 'rising', 'evacuation', 'disaster', 'reservoir', 'emergency', 'levee', 'submerged', 'torrential', 'waterway', 'floodplain', 'floody', 'rainfall', 'floodwater', 'leaking', 'damaged', 'damaging', 'barrier', 'riverbank', 'inflow', 'deluged', 'floodgate', 'overflowed', 'flooded-out', 'rainstorm', 'water surge', 'overtop', 'soggy', 'flood-prone', 'heavy rain', 'flooded area', 'waterlogged', 'rainfall records']
    cyclone_typhoon_dict = ['cyclone', 'typhoon', 'storm', 'wind', 'tropical', 'hurricane', 'gales', 'weather', 'dangerous', 'destruction', 'devastating', 'powerful', 'cyclonic', 'eye', 'landfall', 'intense', 'category', 'rain', 'evacuation', 'threat', 'warning', 'disaster', 'windy', 'severe', 'tornadoes', 'coastal', 'windswept', 'shelter', 'emergency', 'damaging', 'impact', 'prepare', 'safety', 'damage', 'landfall', 'surge', 'relief', 'resilience', 'evacuate', 'precautions', 'preparedness', 'cyclonic storm', 'typhoon warning', 'evacuation plan', 'weather alert', 'severe weather', 'cyclone aftermath', 'emergency response', 'tropical storm', "cyclone's path"]

    temp_title = link
    score_array = []

    for l in [drought_dict, cold_storm_dict, other_storm_dict, fire_dict, flood_dict, cyclone_typhoon_dict]:

        score_array.append(count_words_in_string(l, temp_title))


    max_value = max(score_array)

    if max_value == 0:

        type_disaster = "unknown"

    else:
        
        type_disaster = types_disasters[score_array.index(max_value)]

    return type_disaster



def split_date(date):

    date = str(date)

    year = date[:4]
    month = date[4:6]
    day = date[6:]

    return str(year) + "/" + str(month) + "/" + str(day)




# checking if this date is in the right quarter (year agnostic)
def check_quarter(date, idx):

    return quarter_starts[idx] <= date.replace(year=random_year) <= quarter_starts[idx + 1]



# Wrapper function that unpacks arguments and calls the original function
def my_function_wrapper(args):
    (key, information, weather_event_df) = args
    return process_titles(key, information, weather_event_df)


def process_titles(key, information, weather_event_df):

    print(f"STARTING: {key}")

    # key, information = next(iter(link_dict.items()))

    # go through each of the pairings... get the name of the news org and the respective news data first
    temp_df = get_article_links(key)

    # check if the right text is in the article title
    if information[2] != "":
        
        # drop any of the rows that don't contain right text
        temp_df = temp_df[temp_df['link'].str.contains('|'.join(information[2]))]

    # now that we have the associated dataframe, go link by link and process it into individual words 
    # that we can compare against our bad word dictionary
    # make sure that we keep the date there too

    # remember, we still need to process nbcnews'

    # temp_df["date"] = temp_df["date"].apply(lambda row: get_date(row["link"], information) if row["date"].isnull().all() else row)

    for _, row in temp_df.iterrows():

        # check if there is a date attached
        if pd.isna(row["date"]):

            row["date"] = get_date(row["link"], information)
        
        # now we either have a date or we don't
        # if we don't, we can't consider this article link and should drop it

    temp_df = temp_df.dropna(subset=["date"])
    temp_df = temp_df.loc[~(temp_df["date"] == "")]

    ## WEATHER STUFF
    # check if the article mentions any weather events
    temp_df["mentions_weather"] = temp_df["link"].apply(check_weather)
    temp_df["weather_type"] = None
    temp_df["weather_type"] = temp_df[temp_df["mentions_weather"]]["link"].apply(get_type_disaster)

        
    # create a new df column that has the article names
    temp_df["title"] = temp_df["link"].apply(lambda age: split_title(age, information))

    temp_w = weather_event_df["name"].copy()
    temp_w["mentions"] = 0


    # go line by line in the df now and increase the reference count for news-worthy weather events
    for _, men_row in temp_df[temp_df["mentions_weather"] == True].iterrows():

        # parse the date of the article
        article_date = parse(men_row["date"]).replace(tzinfo=None)

        # now add one to the reference count for weather events
        # for _, w_row in weather_event_df.iterrows():
            
        temp_w.loc[(weather_event_df["start"] < article_date) & (weather_event_df["end"] + timedelta(days=days_to_add) > article_date), "mentions"] += 1
            # weather_event_df[parse(weather_event_df["start"]) < article_date & parse(weather_event_df["end"]) + timedelta(days=days_to_add) > article_date, "mentions"] += 1
        

    # save this to a new csv in my local citadel correlation folder
    temp_df.to_csv(path_to_article_titles + key + "_titles.csv", index=False)


    print(f"DONE: {key}")

    return temp_w
