from flask import Flask
from flask import flash, jsonify, redirect, render_template, request, url_for

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
    
if __name__ == "__main__":
    print("OK, this works as expected")
    app.run(debug=1)