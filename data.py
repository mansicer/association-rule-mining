import numpy as np
import pandas as pd
import re
import os
from copy import copy
from sys import stderr


def load_grocery_dataset():
    grocery = pd.read_csv(
        'dataset/GroceryStore/Groceries.csv').values[:, 1].tolist()
    grocery = [s[1:-1] for s in grocery]
    grocery = [s.split(',') for s in grocery]
    return grocery


def get_items(data):
    items = set()
    for row in data:
        for it in row:
            if it not in items:
                items.add(it)
    return list(items)


def load_unix_usage_from_filename(filename):
    res = []
    with open(filename, 'r') as f:
        for line in f:
            if line.strip() == '**SOF**':
                item = []
            elif line.strip() == '**EOF**':
                res.append(list(set(item)))
            else:
                line = line.strip()
                if re.match(r'[a-zA-Z0-9\-\._]+$', line):
                    item.append(line.lower())
    return res


def load_unix_usage_dataset(user=None):
    fold = 'dataset/UNIX_usage/USER{}/'
    if user is None:
        res = []
        for i in range(9):
            fn = os.path.join(fold.format(i), os.listdir(fold.format(i))[0])
            res.extend(load_unix_usage_from_filename(fn))
    else:
        fn = os.path.join(fold.format(user), os.listdir(fold.format(user))[0])
        res = load_unix_usage_from_filename(fn)
    return res


def get_grocery_weka_format():
    grocery = pd.read_csv('dataset/Groceries.csv').values[:, 1].tolist()
    grocery = [s[1:-1] for s in grocery]
    grocery = [s.split(',') for s in grocery]
    items = get_items(grocery)
    dic = {j: i for i, j in enumerate(items)}
    with open('grocery_weka.arff', 'w') as f:
        f.write('@relation grocery\n')
        for it in items:
            f.write('@attribute {}'.format(
                ''.join(it.split())) + r' {F, T}' + '\n')
        f.write('@data\n')
        for row in grocery:
            lst = [dic[it] for it in row]
            lst = sorted(lst)
            lst = ['{} T'.format(it) for it in lst]
            f.write(r'{' + ', '.join(lst) + r'}' + '\n')


def get_unix_usage_weka_format(user=None):
    unix = load_unix_usage_dataset(user)
    items = get_items(unix)
    dic = {j: i for i, j in enumerate(items)}
    fn = 'unix_usage_user{}'
    if user is None:
        fn = fn.format('')
    else:
        fn = fn.format(user)
    with open(fn + '.arff', 'w') as f:
        f.write('@relation {}\n'.format(fn))
        for it in items:
            f.write('@attribute {}'.format(
                ''.join(it.split())) + r' {F, T}' + '\n')
        f.write('@data\n')
        for row in unix:
            lst = [dic[it] for it in row]
            lst = sorted(lst)
            lst = ['{} T'.format(it) for it in lst]
            f.write(r'{' + ', '.join(lst) + r'}' + '\n')


# get_grocery_weka_format()
get_unix_usage_weka_format()
for i in range(9):
    get_unix_usage_weka_format(i)
