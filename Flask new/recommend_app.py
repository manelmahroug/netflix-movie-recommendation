from flask import Flask
from flask import flash, jsonify, redirect, render_template, request, url_for
import pandas as pd
import numpy as np
import png

import movie_recommendation as mr
import load_means as lm

app = Flask(__name__)
app.secret_key = 'some_secret'

# data_loaded=False
print("Loading data...")
means_matrix_1k = lm.png_to_matrix("sparse_means_1k.png")
ids_1k = list(pd.read_csv("movie_ids_1k.csv")["movie_id"])
print("Loaded!")
# data_loaded=True

@app.route('/')
def hello_world():
    #return url_for("static", filename="template.html")
    return render_template("index.html")

@app.route('/users')
def old_users():
    #return url_for("static", filename="template.html")
    return render_template("old_users.html")

@app.route("/user/<uid>")
def get_user_movies(uid):
    ### I think this is close to what we want?
    # user_df = ??
    # output_df=mr.PC_Prediction(user_df)
    # return str(list(output_df.iloc[:,0]))
    return str([1,20,34,23])

@app.route("/predict/<string>")
def get_movies(string):
    input_list = string_to_input_list(string)
    output_df=lm.get_predictions_sparse(input_list,means_matrix_1k,ids_1k).head(10)
    return str(list(output_df["movie_id"]))

def string_to_input_list(string):
    li = [[int(x) for x in string.split(",")[:5][i].split(":")] for i in range(5)]
    return li

def string_to_df(string,columns=["movie_id","rating"],insert_user=True):
    li = [[int(x) for x in string.split(",")[:5][i].split(":")] for i in range(5)]
    df = pd.DataFrame(li, columns=columns)
    if insert_user:
        df.insert(1, "user_id", 0)
    return df
    
if __name__ == "__main__":
    print("OK, this works as expected")
    app.run(debug=1)