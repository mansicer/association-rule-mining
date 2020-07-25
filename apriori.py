import numpy as np
import pandas as pd
from copy import copy
from sys import stderr
from data import get_items


def get_L1(data, items, min_sup=0.4):
    res = {}
    n = len(data)
    # L1 item
    for it in items:
        idx = [i for i in range(len(data)) if it in data[i]]
        count = len(idx)
        if count / n < min_sup:
            continue
        else:
            itset = {}
            name = (it,)
            itset['idx'] = idx
            itset['count'] = count
            res[name] = itset
    return res


def get_Lk(data, items, l, min_sup=0.4):
    res = {}
    n = len(data)
    # Lk item
    for pname, prev in l.items():
        for it in items:
            if it in pname:
                continue

            name = list(pname)
            name.append(it)
            name = tuple(sorted(name))
            if name in res:
                continue

            idx = [idx for idx in prev['idx'] if it in data[idx]]
            count = len(idx)
            if count == 0:
                continue
            if count / n < min_sup:
                continue

            itset = {}
            itset['idx'] = idx
            itset['count'] = count
            res[name] = itset

        del prev['idx']
    return res


def apriori(data, min_sup=None):
    items = get_items(data)
    res = {}

    if min_sup is None:
        min_sup = 1 / len(items)
    print('Apriori with min support {:.3f}'.format(min_sup))

    k = 1
    print('Analyze L{} item set'.format(k), end='... ', file=stderr)
    cursets = get_L1(data, items, min_sup)
    l1_num = len(cursets)
    print('finished with {} item sets'.format(len(cursets)), file=stderr)
    while len(cursets) != 0:
        res.update(cursets)
        k += 1
        print('Analyze L{} item set'.format(k), end='... ', file=stderr)
        cursets = get_Lk(data, items, cursets, min_sup)
        print('finished with {} item sets'.format(len(cursets)), file=stderr)
    print('Find {} frequent sets'.format(len(res) - l1_num))
    res = {k: v['count'] for k, v in res.items()}
    return res


def print_itemset(kname, v, n):
    if len(kname) == 1:
        return
    name = r'{' + ', '.join(kname[:-1]) + r'}'
    name += ' => {}'.format(kname[-1])
    if len(name) <= 50:
        print('Set {:<50}: occurs {} times, support {:.3f}'.format(name, v, v/n))
    else:
        print('Set {}: occurs {} times, support {:.3f}'.format(name, v, v/n))


def print_itemsets(res, n):
    rules = sorted(res.items(), key=lambda e: -e[1])
    for k, v in rules:
        print_itemset(k, v, n)
