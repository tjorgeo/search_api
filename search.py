import requests
import pandas
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
        'cr': 'countryDE',
        'lr': 'lang_de',
        'start': start
    }
    return params


def get_search_results(params):

    url = 'https://www.googleapis.com/customsearch/v1'
    # get search params
    try:
        response = requests.get(url, params=params)
        results = response.json()['items']
    except:
        print("No results for query")
        results = ''
    return results


def store_and_print(results):
    #print('     ')
    #print('following links are to consider:')
    #print('     ')
    all_results = ''
    for item in results:
        try:
            #print(item['link'])
            
            website = requests.get(item['link'])
            soup = BeautifulSoup(website.content, 'html.parser')
            title = soup.title.text
            webtext = soup.contents
            all_results = all_results + item['link'] + " -- Titel: " + title + "\n"
            #print(webtext)
        except:
            print("Invalid URL or empty request results for Link:")
            print(item['link'])
            #all_results = all_results + item['link']
    return all_results

def search_for_leads(row):
    start = 1
    while start < 15:
        params = get_search_params(row, start)
        results = get_search_results(params)
        all_results = store_and_print(results)
        start = start + 10
    return all_results

def write_to_file():
    search_data_df = dataTable.get_dataframe("bä_ms_06_Leads_2024-02-29_2024-03-30.csv")

    search_data_df.info()

    validate_df = validate_mail.mail_validation(search_data_df)

    validate_df.info()

    all_results = ''

    for index,row in validate_df.iterrows():
        print(index)
        name = row.firstName + " " + row.lastName
        all_results = all_results + name + "\n" + search_for_leads(name) + "\n"
    with open("Output.txt", "w") as text_file:
        text_file.write(all_results)

def main():
    write_to_file()

if __name__ == "__main__":
    main()