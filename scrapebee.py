
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from scrapingbee import ScrapingBeeClient
import dataTable
import pandas as pd
import os


def scrape_site(urls):
    load_dotenv()
    # Params for google search api
    API_KEY = os.getenv('SCRAPEBEE_API_KEY')

    client = ScrapingBeeClient(api_key='IEFN589WKC94DBOL6OVBLN0NDC5AFYTSW62QEI34K3NH7MHDMSYNX8TUGO9ZY5EYHB8ITW156Y5AG3Z2')
    for url in urls:
        response = client.get(url,
            params = { 
            '   json_response': 'True',
        })
        print('Website HTML: ', response.content)

def get_results(results):
    all_results = ''
    urls =  ''
    for result in results:
        for key in result:
            print(key,":", result[key]) 

    return all_results, urls


def send_request(name):
    response = requests.get(
        url='https://app.scrapingbee.com/api/v1/store/google',
        params={
            'api_key': 'IEFN589WKC94DBOL6OVBLN0NDC5AFYTSW62QEI34K3NH7MHDMSYNX8TUGO9ZY5EYHB8ITW156Y5AG3Z2',
             
            'search': name,
            'country_code': 'de',
            'language': 'de',
            'nb_results': '10', 
        },
        
    )
    print('Response HTTP Status Code: ', response.status_code)
    return response

def get_linkedin_url(name):
    response = send_request(name)
    if response.status_code == 200:
        #print('Response HTTP Response Body: ', response.content)
        linkedin_url = ""
        firstName, lastName = name.split(maxsplit=1)
        results = response.json()
        #print("Results:", results)
        organic_results = results['organic_results']
        #print("Organic Results:", organic_results)
        for result in organic_results:
            url = result['url']
            if "linkedin" in url.lower() and "de" in url.lower() and "dir" not in url.lower() and "post" not in url.lower() and (firstName.lower() in url.lower() or lastName.lower() in url.lower()):
                linkedin_url = url
    else: linkedin_url = str(response.json())
    return linkedin_url

def scrape_linkedin_google():
    results = []
    names = dataTable.get_data_names()
    for name in names:
        linkedin_url = get_linkedin_url(name)
        if len(linkedin_url) < 1:
            linkedin_url = get_linkedin_url(str(name + " Linkedin"))
        while "error" in linkedin_url:
            print(name + ", " + linkedin_url)
            linkedin_url = get_linkedin_url(name)
        results.append((name,linkedin_url))
        print(name + ", " + linkedin_url)

    # Convert to DataFrame
    df = pd.DataFrame(results, columns=['Name', 'LinkedIn URL'])
    # Write to CSV file
    df.to_csv("Output_bee.csv", index=False)

def main():
    scrape_linkedin_google()




if __name__ == "__main__":
    main()