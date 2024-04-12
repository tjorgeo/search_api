import pandas as pd


def get_dataframe(file):
    try:
        data = pd.read_csv(file, encoding = "UTF-16 LE", sep='\t', engine='python')
        df = pd.DataFrame(data)
        relevant_df = pd.DataFrame(df[["firstName", "lastName", "email", "postcode", "city", "company"]])
        return relevant_df
    except:
        print("Error!")




