from flask import Flask
from flask import flash, jsonify, redirect, render_template, request, url_for
import pandas as pd
import numpy as np

import movie_recommendation as mr

app = Flask(__name__)
app.secret_key = 'some_secret'

@app.route('/')
def hello_world():
    #return url_for("static", filename="template.html")
    return render_template("index.html")

'''@app.route("/predict/")
def ratingsHandler():
    movie1 = request.form["movie_1"]
    rating1 = int(request.form["rating_1"])
    movies = movies.getRecommendations([(movie1, rating1)])
    return jsonify(movies)'''

@app.route("/predict/<string>")
def get_movies(string):
    user_df = string_to_df(string)
    
    print(mr.PC_Prediction(user_df))

    return str(list(user_df.iloc[:,0])) #dummy return for now
    #
    # Do whatever ML stuff with the df here
    # 
    
    # return top_5_movies_or_whatever
    #    (Maybe a jsonify'd list?)

def string_to_df(string,columns=["movie_id","rating"],insert_user=True):
    li = [[int(x) for x in string.split(",")[:5][i].split(":")] for i in range(5)]
    df = pd.DataFrame(li, columns=columns)
    if insert_user:
        df.insert(1, "user_id", 0)
    return df
    
if __name__ == "__main__":
    print("OK, this works as expected")
    app.run(debug=1)