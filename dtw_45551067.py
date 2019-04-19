from tqdm import tqdm
from math import inf

def get_dtw(s,t):
    res = [[0] * (len(t)+1) for x in range(len(s)+1)]

    for i, row in enumerate(res):
        if i == 0:
            for j, col in enumerate(res[0]):
                if j > 0:
                    res[i][j] = inf
        if i > 0:
            res[i][0] = inf

    for i, val_s in enumerate(s):
        for j,val_t in enumerate(t):
            cost = (val_s - val_t) ** 2
            res[i+1][j+1] = cost + min(res[i-1][j], res[i][j-1], res[i-1][j-1])

    return res[len(s)][len(t)]


def parsing(file):
    database = []

    for row in file.readlines():
        fila = row.split()
        index = int(fila[0])
        data = [float(i) for i in fila[1:]]
        database.append((index, data))
    return database

train = parsing(open("train.txt", "r"))
test = parsing(open("test.txt", "r"))


def get_index_dtw(s, t):
    res = []
    for i, val_train in tqdm(train):
        for j, val_test in test:
            res.append([i, j, get_dtw(val_train, val_test)])
    return res

if __name__ == '__main__':
    results = get_index_dtw(train, test)

    with open('output', 'w') as f:
        for i,j,val in results:
            f.write(f'{i},{j},{val:0.15e}\n')

    minima = []
    for n in range(1, 13):
        same = [(j, dtw) for i, j, dtw in results if i == n]

        minima.append([n, *min(same, key=lambda x: x[1])])


    for i, j, val in minima:
        print(f'[{i},{j}]: {val:1.15e}')
