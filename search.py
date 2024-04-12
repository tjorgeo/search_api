import requests
import pandas
from bs4 import BeautifulSoup
import dataTable


def get_search_params(name):
    
    

    # Params for google search api
    API_KEY = open('API_KEY').read()
    SEARCH_ID = open('SEARCH_ID').read()

    # query to search for
    search_query = name

    # params for further filterin results
    params = {
        'q': search_query,
        'key': API_KEY,
        'cx': SEARCH_ID,
        'cr': 'countryDE',
        'lr': 'lang_de',
        'hl': 'lang_de'

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
            webtext = website.text
            all_results = all_results + item['link'] + " -- Titel: " + title + "\n"
            #print(webtext)
        except:
            print("Invalid URL or empty request results")
    return all_results

def search_for_leads(row):
    params = get_search_params(row)
    results = get_search_results(params)
    all_results = store_and_print(results)
    return all_results

def write_to_file():
    search_data_df = dataTable.get_dataframe("bä_ms_06_Leads_2024-02-29_2024-03-30.csv")

    for index,row in search_data_df.iterrows():
        print(index)
        name = row.firstName + " " + row.lastName
        all_results = name + "\n" + search_for_leads(name)
        with open("Output_{idx}.txt".format(idx = index), "w") as text_file:
            text_file.write(all_results)



def main():
    write_to_file()

if __name__ == "__main__":
    main()