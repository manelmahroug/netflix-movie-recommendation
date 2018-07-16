from pathlib import Path
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Unzip the data files into a directory
# Point the following string to the directory

dir_to_scan = "netflix-data"  

p = Path(dir_to_scan)

# Create lists of the folders and files

folders = []
files = []

for entry in os.scandir(p):
    if entry.is_dir():
        folders.append(entry)
    elif entry.is_file():
        files.append(entry)

print("Folders - {}".format(folders))
print("Files - {}".format(files))


# The code below creates the combined file with 4 columns
# Columns: Movie ID, User ID, Rating, Date

if not os.path.isfile('data.csv'):

     data = open('data.csv',mode='w')


row = list()


for file in files:


    print("Reading ratings from {}..... ".format(file))


    

     

with open(file, encoding= "ISO-8859-1") as f:


        for i,line in enumerate(f):
            del row[:]
            line = line.strip()
            if ':' in line:
                movie_id = line.replace(':',' ')
            else:
                row = [x for x in line.split(',')]
                row.insert(0,movie_id)
                data.write(','.join(row))  #error in this line
                data.write('\n')
    print("Done.\n")
data.close() 

# Place newly created combined data file in pandas dataframe

data_all = pd.read_csv('data.csv', header = None, names = ['movie_id', 'user_id', 'rating', 'date'])
data_all['date'] = pd.to_datetime(data_all['date'])

# Drop duplicates if any (in this case none)

data_all.drop_duplicates()

# Place movie titles file into pandas dataframe

movie_titles = pd.read_csv('movie_titles.csv', header = None, names = ['movie_id', 'year', 'title'], usecols=[0,1,2],encoding = "ISO-8859-1")

# Get the average of the movie ratings by movie_id
ratings_by_title = data_all.groupby(['movie_id']).mean()['rating']
ratings_dict = ratings_by_title.to_dict()

def add_ratings(row):
    return ratings_dict[row['movie_id']]

movie_titles['avg_rating'] = movie_titles.apply (lambda row: add_ratings (row),axis=1)


# Place top 15 (by ratings) movies into dataframe

top_15 = movie_titles.sort_values(by=['avg_rating'],  ascending=False).head(15)
