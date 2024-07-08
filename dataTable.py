import pandas as pd


def get_dataframe(file):
    #try:
    #data = pd.read_csv(file, encoding = "UTF-16 LE", sep='\t', engine='python')
    data = pd.read_csv(file)
    df = pd.DataFrame(data)
    df['name'] = df["Person - Vorname"] + " " + df["Person - Nachname"]
    #relevant_df = pd.DataFrame(df[["firstName", "lastName", "email", "postcode", "city", "company"]])
    return df
    
def get_data_names():
    names = ["Hannes Tausend",
             "Peter Muryshkin",
             "Sina Nägel",
             "Benjamin Borgerding",
             "Harald Kratel",
             "Linda Mozham",
             "Christian Schmalzl",
            "Jürgen Mayer",
            "Markus Reiser",
            "Thomas Grethe",
            "Johanna Bormann",
            "Stephan Settmacher",
            "Ingo Scharfe",
            "Lars Bleeker",
            "Oliver Seltmann",
            "Christian Jund",
            "Malte Andresen",
            "Philip Chhatwani",
            "Dörte Brilling",
            "Markus Gotta",
            "Kerstin Neubert",
            "Jan Tackmann",
            "Nele Husmann",
            "Stephan Waltl",
            "Gesa Kettler",
            "Bärbel Hammer",
            "Stephan Bange",
            "Ralph Voggenreiter",
            "Olaf Kracht",
            "Thilo Kramny",
            "Jan Persiel",
            "Christoph Möller",
            "Kai Schächtele",
            "Sandra Gläsner"]
    return names

    #except:
     #   print("Error!")




