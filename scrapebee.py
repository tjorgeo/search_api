
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import requests
from scrapingbee import ScrapingBeeClient
import dataTable
import pandas as pd
import os



# Scraping various websites
def scrape_site(urls):
    load_dotenv()
    API_KEY = os.getenv('SCRAPEBEE_API_KEY')
    # Params for google search api
    client = ScrapingBeeClient(api_key=API_KEY)
    for url in urls:
        response = client.get(url,
            params = { 
            '   json_response': 'True',
        })
        print('Website HTML: ', response.content)

# scraping google search
def send_request(name):
    load_dotenv()
    API_KEY = os.getenv('SCRAPEBEE_API_KEY')
    response = requests.get(
        url='https://app.scrapingbee.com/api/v1/store/google',
        params={
            'api_key': API_KEY,
             
            'search': name,
            'country_code': 'de',
            'language': 'de',
            'nb_results': '10', 
        },
    )
    print('Response HTTP Status Code: ', response.status_code)
    return response

# method to filter the linkedin url outof the google search results
def get_linkedin_url(name):
    response = send_request(name)
    if response.status_code == 200:
        #print('Response HTTP Response Body: ', response.content)
        linkedin_url = ""
        name_parts = name.split(maxsplit=1)
        # Assign firstName and lastName
        if len(name_parts) == 1:
            firstName = lastName = name_parts[0]
        else:
            firstName, lastName = name_parts
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

# method to get the linkedin URLs and put them in a DataFrame and export a CSV file
def scrape_linkedin_google():
    j = 1
    results = []
    df = dataTable.get_dataframe("data/pipedrive_01_07_24.csv")
    df = df.iloc[800:1000]
    #names = dataTable.get_data_names()

    # iterating through names and finding Linkedin URL
    for name in df["name"]:
            # Ensure name is a string
        if isinstance(name, float):
            name = str(name)
        elif name is None:
            name = ""
        print(j)
        i = 0
        linkedin_url = get_linkedin_url(name)
        if len(linkedin_url) < 1:
            linkedin_url = get_linkedin_url(str(name + " Linkedin"))
        while "error" in linkedin_url and i < 5:
            print(str(i) + ") " + name + ", " + linkedin_url)
            linkedin_url = get_linkedin_url(name)
            i = i + 1
        results.append((name,linkedin_url))
        print(name + ", " + linkedin_url)
        df.loc[df['name'] == name, 'Person - LinkedIn'] = linkedin_url
        j = j + 1

    # Convert to DataFrame
    #df = pd.DataFrame(results, columns=['Name', 'LinkedIn URL'])
    # Write to CSV file
    df.to_csv("output/Output_bee_800_1000.csv", index=False)

# Main method for this application
def main():
    scrape_linkedin_google()

if __name__ == "__main__":
    main()