import pandas as pd
import numpy as np
import time

df=pd.read_csv("test_data_2.csv")

max_id = max(df["movie_id"])
min_id = min(df["movie_id"])

movies = {}
for i in range(min_id,max_id+1):
    movies[i] = df[df["movie_id"]==i].drop(["movie_id"],axis=1).set_index("user_id")

def rough_means_v1(df, id1, id2, movie_dict=None, col_norm=50, low_clip=0):
    if movie_dict is None:
        df1 = df[df["movie_id"]==id1].drop(["movie_id"],axis=1)
        df2 = df[df["movie_id"]==id2].drop(["movie_id"],axis=1)
    else:
        df1 = movie_dict[id1]
        df2 = movie_dict[id2]
    
    df_join = df1.join(df2, how="inner", lsuffix="_x", rsuffix="_y")
    
    total = len(df_join)
    if total == 0 or total < low_clip:
        return [0,0,0]
    
    rx = df_join["rating_x"]
    ry = df_join["rating_y"]
    
    low = df_join[rx<3]
    med = df_join[rx==3]
    high = df_join[rx>3]
    
    result = []
    
    for x in [(low,2),(med,1),(high,2)]:
        if len(x[0])==0:
            result.append(0)
        else:
            result.append(np.interp(x[0]["rating_y"].mean(),[1,5],[0,1])*np.interp(len(x[0]),[0,col_norm*x[1]],[0,1]))

    return result

def rough_means_matrix(df, min_id, max_id, movie_dict=None, col_norm=50, low_clip=0, progress=False, prog_interval=100):
    matrix = []
    counter=0
    t0=time.time()
    for i in range(min_id, max_id+1):
        matrix.append([])
        for j in range(min_id, max_id+1):
            matrix[i-min_id].append(rough_means_v1(df, i, j, movie_dict, col_norm, low_clip))
            
            if progress:
                if counter%prog_interval==0:
                    t1=time.time()
                    print(f"{counter} records complete... ({round(t1-t0,3)} s elapsed)")
                counter+=1
    return matrix

means_matrix = rough_means_matrix(df, min_id, max_id, movies, low_clip=150, progress=True, prog_interval=1000)