import pandas as pd
import numpy as np
from utils import *
from sklearn.metrics.pairwise import cosine_similarity

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


pd.set_option('future.no_silent_downcasting', True)

# n_user = int(input('用户数量：'))
# n_column = int(input('电影数量：'))
# column_film = [f"film{i + 1}" for i in range(n_column)]
# index_user = [f"user{i + 1}" for i in range(n_user)]
# matrix_user_film = pd.DataFrame(columns=column_film, index=index_user)
# while True:
#     inf_ = input('依次输入用户id、电影id、评分（q退出）：')
#     if inf_ == 'q':
#         break
#     inf = list(map(int, inf_.split(' ')))
#     matrix_user_film.iloc[inf[0]-1, inf[1]-1] = inf[2]
# matrix_user_film = matrix_user_film.fillna(0)
# matrix_user_film = matrix_user_film.infer_objects(copy=False)

matrix_user_film = pd.read_csv('UF_data.csv', names=[f'film{i + 1}' for i in range(len_row('UF_data.csv'))])
matrix_user_film.index = [f'user{i + 1}' for i in range(len_col('UF_data.csv'))]  # 读取文件

print(matrix_user_film)

print('='*50)
data_cos = pd.DataFrame(cosine_similarity(matrix_user_film))
data_cos.index = [f'user{i + 1}' for i in range(len_col('UF_data.csv'))]
data_cos.columns = [f'user{i + 1}' for i in range(len_col('UF_data.csv'))]
print(data_cos)


def pre_rating(UF_matrix, cos_matrix, threshold=0.2):  # 阈值设置
    pr_matrix = UF_matrix.copy()

    for user in UF_matrix.index:
        # user_film_rating = {}
        for film in UF_matrix.columns:
            if UF_matrix.loc[user, film] == 0:
                numerator = 0
                denominator = 0
                # film_rating = []

                for other_user in UF_matrix.index:
                    if other_user != user and UF_matrix.loc[other_user, film] != 0 and cos_matrix.loc[user, other_user] > threshold:
                        simi = cos_matrix.loc[user, other_user]
                        rating = UF_matrix.loc[other_user, film]
                        numerator += simi * rating
                        denominator += simi
                        # other_user_rating = [other_user, simi, rating]
                        # film_rating.append(other_user_rating)
                # user_film_rating[user] = film_rating

                if denominator != 0:
                    pr_matrix.loc[user, film] = numerator/denominator

    return pr_matrix  # return pr_matrix, user_film_rating  原因（不推荐使用）


print('='*50)
pr = pre_rating(matrix_user_film, data_cos)
print(pr)


def recommend_films(UF_matrix, PR_matrix):
    recommend = {}
    for user in PR_matrix.index:
        films = {}
        for film in UF_matrix.columns:
            if UF_matrix.loc[user, film] == 0:
                films[film] = PR_matrix.loc[user, film]
        films = sorted(films.items(), reverse=True, key=lambda x: x[1])
        recommend[user] = films
    return recommend


result = recommend_films(matrix_user_film, pr)
print('='*50)
print(result)

w_dict2txt(result)  # 写入文件
