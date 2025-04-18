import csv


def len_row(file):
    with open(file) as f:
        return len(list(csv.reader(f))[0])


def len_col(file):
    with open(file) as f:
        return len(list(csv.reader(f)))


def w_dict2txt(dic, name='users_recommend_films.txt'):
    with open(name, 'w') as f:
        for item in dic.items():
            if item[1]:
                text = f'用户{item[0]}受推荐的电影有{[film[0] for film in item[1]]},最推荐的电影为{item[1][0][0]},推荐分为{item[1][0][1]}\n'
            else:
                text = f'用户{item[0]}没有受推荐的电影\n'
            f.write(text)
