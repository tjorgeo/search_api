import requests
import pandas as pd
from bs4 import BeautifulSoup
import dataTable
from dotenv import load_dotenv
import os
import validate_mail
from urllib.parse import quote_plus



def get_search_params(name, start):

    load_dotenv()
    # Params for google search api
    API_KEY = os.getenv('API_KEY')
    SEARCH_ID = os.getenv('SEARCH_ID')

    # query to search for
    search_query = name

    # params for further filterin results
    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ID,
        'cr': 'de',
        'lr': 'de',
        'start': start
    }
    return params


def get_search_results(params):

    url = 'https://www.googleapis.com/customsearch/v1'
    # get search params
    try:
        response = requests.get(url, params=params)
        print('Response HTTP Status Code: ', response.json())
        results = response.json()['items']
    except:
        print("No results for query")
        print(params)
        results = ''
    return results


def store_and_print(results, name):
    # Split the string into a list of two elements, handling extra spaces
    firstName, lastName = name.split(maxsplit=1)
    all_results = []
    for item in results:
        
        try:
            #website = requests.get(item['link'])
            if "linkedin" in item['link'].lower() and "de" in item['link'].lower() and "dir" not in item['link'].lower() and "post" not in item['link'].lower() and (firstName.lower() in item['link'].lower() or lastName.lower() in item['link'].lower()):
                all_results.append((name, item['link']))
            #soup = BeautifulSoup(website.content, 'html.parser')
            #title = soup.title.text
            #webtext = soup.contents
                
            #print(webtext)
        except:
            print("Invalid URL or empty request results for Link:")
            #print(item['link'])
            print(item)
            #all_results = all_results + item['link']
    return all_results

def search_for_leads(row):
    start = 1
    while start < 15:
        params = get_search_params(row, start)
        results = get_search_results(params)
        all_results = store_and_print(results, row)
        start = start + 10
    return all_results

def do_linkedin_search():
    all_results = []
    names = dataTable.get_data_names()
    for name in names:
        results = search_for_leads(name)
        all_results.extend(results)
    # Convert to DataFrame
    df = pd.DataFrame(all_results, columns=['Name', 'LinkedIn URL'])
    # Write to CSV file
    df.to_csv("Output_try.csv", index=False)

def main():
    #write_to_file()
    do_linkedin_search()

if __name__ == "__main__":
    main()