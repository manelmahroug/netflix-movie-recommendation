import pandas as pd
import numpy as np
import png

# Takes around 45 sec for 1k
def png_to_matrix(filename, output_range=(0,1)):
    
    r=png.Reader(filename=filename)
    png_list = list(r.read()[2])
    
    def interp(x):
        return np.interp(x, [0,255],output_range)
    
    matrix=[]
    for i in range(len(png_list)):
        matrix.append([])
        for j in range(int(len(png_list[0])/3)):
            matrix[i].append([interp(png_list[i][3*j+k]) for k in range(3)])

    return matrix

def get_predictions_sparse(input_list, matrix, id_list):
    numrows = len(matrix)
    numcols = numrows
    predictions = []
    total=len(input_list)
    
    for m_r in input_list:
        movie_id = m_r[0]
        rating = m_r[1]
        if movie_id not in id_list:
            total-=1
            continue
        predict_row = matrix[id_list.index(movie_id)]
        predict_list = [np.interp(rating,[1,3,5],predict_row[i])*4+1 for i in range(numcols)]
        predictions.append(predict_list)
        
    predict_sums=[]
    for i in range(len(predictions[0])):
        predict_sums.append(0)
        for j in range(len(predictions)):
            predict_sums[i] += predictions[j][i]
    
    predictions_df = pd.DataFrame({"movie_id":id_list,"rating":[x/total for x in predict_sums]})
    predictions_df.query(f'movie_id not in {[x[0] for x in input_list]}', inplace=True)
 
    return predictions_df.sort_values("rating",ascending=False)
