import pandas as pd
# import seaborn as sns
import numpy as np
import csv
from surprise import Reader, Dataset, SVD, evaluate,accuracy,dump
from surprise.model_selection import train_test_split


def clean_ratings(all_ratings_DF):
    f = ['count','mean']

    ratings_summary_DF = all_ratings_DF.groupby('movie_id')['rating'].agg(f)
    ratings_summary_DF.index = ratings_summary_DF.index.map(int)
    movie_benchmark = round(ratings_summary_DF['count'].quantile(0.8),0)
    drop_movie_list = ratings_summary_DF[ratings_summary_DF['count'] < movie_benchmark].index

    print('Movie minimum times of review: {}'.format(movie_benchmark))
    
    user_summary_DF = all_ratings_DF.groupby('user_id')['rating'].agg(f)
    user_summary_DF.index = user_summary_DF.index.map(int)
    cust_benchmark = round(user_summary_DF['count'].quantile(0.8),0)
    drop_cust_list = user_summary_DF[user_summary_DF['count'] < cust_benchmark].index

    print('Customer minimum times of review: {}'.format(cust_benchmark))
    

    all_ratings_clean_DF = all_ratings_DF
    print('Original Shape: {}'.format(all_ratings_clean_DF.shape))
    all_ratings_clean_DF = all_ratings_DF[~all_ratings_DF['movie_id'].isin(drop_movie_list)]
    all_ratings_clean_DF = all_ratings_DF[~all_ratings_DF['user_id'].isin(drop_cust_list)]
    print('After Trim Shape: {}'.format(all_ratings_clean_DF.shape))
    
    return(all_ratings_clean_DF)


def load_ratings():
    all_ratings_DF =  pd.read_csv('all_ratings.csv') 
    all_ratings_clean_DF = clean_ratings(all_ratings_DF)
    return(all_ratings_clean_DF)


def load_movies():

    all_movies_DF = pd.DataFrame(columns=['movie_id','year','movie_name'])

    csv_file = open('movie_titles.csv',encoding = "ISO-8859-1")
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        if(len(row) == 3):
            all_movies_DF.loc[row[0]] = [int(row[0]),row[1],row[2]]
        else:
            temp_movie_title = ''
            for j in (2,len(row)-1):
                if (j==len(row)-1):
                    temp_movie_title = temp_movie_title + row[j]
                else:
                    temp_movie_title = temp_movie_title + row[j] + ','
            all_movies_DF.loc[row[0]] = [int(row[0]),row[1],temp_movie_title]

    csv_file.close()
    
    all_movieids_DF = all_movies_DF.movie_id
    all_movieids_DF.to_csv('movie_ids.csv', index=True, header=True)
    
    all_movies_DF = all_movies_DF.set_index('movie_id')

    return(all_movies_DF)

def PC_Evaluate(all_ratings_DF):
    reader = Reader()
    readerS = Reader(rating_scale=(1, 5))
    svd = SVD()
    #train_movie_data = Dataset.load_from_df(all_ratings_DF[['user_id', 'movie_id', 'rating']], reader)
    train_movie_data = Dataset.load_from_df(all_ratings_DF[['user_id', 'movie_id', 'rating']][:100000], reader)
    train_movie_data.split(n_folds=3)
    svd = SVD()
    evaluate(svd, train_movie_data, measures=['RMSE', 'MAE'])

def PC_TrainTest(all_ratings_DF):
    reader = Reader()
    readerS = Reader(rating_scale=(1, 5))
    svd = SVD()
    #all_ratings_data = Dataset.load_from_df(all_ratings_DF[['user_id', 'movie_id', 'rating']][:100000], reader)
    all_ratings_data = Dataset.load_from_df(all_ratings_DF[['user_id', 'movie_id', 'rating']][:100000], reader)
    all_ratings_train_data, all_ratings_test_data = train_test_split(all_ratings_data, test_size=.25)

          
    svd.fit(all_ratings_train_data)
    predictions = svd.test(all_ratings_test_data)
    RMSE = accuracy.rmse(predictions)
    MAE = accuracy.mae(predictions)
    predictions_DF = pd.DataFrame(predictions)
    predictions_DF = predictions_DF.rename(columns={"uid": "user_id"
                               , "iid": "movie_id"
                               , "r_ui": "rating"
                               , "est": "prediction"
                              })
    predictions_DF.to_csv('movie_predictions_SVD.csv', index=True, header=True)
    return(predictions_DF)


def PC_TrainFull(all_ratings_DF):
    reader = Reader()
    readerS = Reader(rating_scale=(1, 5))
    svd = SVD()
    
    data = Dataset.load_from_df(all_ratings_DF[['user_id', 'movie_id', 'rating']], reader)
    trainset = data.build_full_trainset()
    svd.train(trainset)
    dump.dump('ratings_CF_SVD_main', algo=svd)

def PC_Prediction(user):
    reader = Reader()
    
    userID = 9999999
    user['user_id'] = userID
    #all_movieids_list = pd.read_csv('movie_ids.csv')['movie_id'] 
    all_movieids_list = [i for i in range (1,17771)]
    movies_list = user.movie_id
    
    
    
    new_list = list(set(all_movieids_list)-set(movies_list))
    
    print(len(all_movieids_list),len(movies_list),len(new_list))
    
    add_movie = pd.DataFrame({   'movie_id': new_list,
                                 'user_id': [userID for _ in range(len(new_list))],
                                 'rating': [0 for _ in range(len(new_list))]
                             })
    user_all_movie_DF = pd.concat([user,add_movie])
    print("Preparing to load model...")
    _, svd = dump.load('svd_model_M')
    print("Loaded model")
    user_dat = Dataset.load_from_df(user_all_movie_DF[['user_id', 'movie_id', 'rating']], reader)
    user_dateset = user_dat.build_full_trainset().build_testset()
    predictions = svd.test(user_dateset)
    pred_rating = [p.est for p in predictions]
    user_all_movie_DF['Predictions'] = pred_rating
    print(len(user_all_movie_DF))
    user_all_movie_DF = user_all_movie_DF[~user_all_movie_DF['movie_id'].isin(movies_list)]
    print(len(user_all_movie_DF))
    user_recommentation_DF = user_all_movie_DF.sort_values('rating',ascending = False).head(10)
    return(user_recommentation_DF)



