import numpy as np
import pandas as pd
from copy import copy
from sys import stderr


def get_key(item):
    return tuple(sorted(item))


def get_conf(itsets, it1, it2):
    it1 = tuple(sorted(it1))
    it2 = tuple(sorted(it2))
    return itsets[it1] / itsets[it2]


def get_subset(items):
    # generate all combination of N items
    N = len(items)
    # enumerate the 2**N possible combinations
    for i in range(1, 2**N - 1):
        combo = []
        for j in range(N):
            # test jth bit of integer i
            if(i >> j) % 2 == 1:
                combo.append(items[j])
        yield tuple(combo)


def check_not_failed(failed_rules, A, B):
    if get_key(A) not in failed_rules:
        return True
    for s in failed_rules[A]:
        if s <= set(B):
            return False
    return False

def generate_rules(itsets, min_conf=0.5, print_num=10, min_items=2):
    rules = []
    print('Generate rules with min confidence {:.3f}'.format(min_conf))
    failed_rules = {}
    for name, count in itsets.items():
        if len(name) < min_items:
            continue
        for A in get_subset(name):
            B = tuple(set(name) - set(A))
            if check_not_failed(failed_rules, A, B):
                conf = get_conf(itsets, name, A)
                if conf >= min_conf:
                    rules.append((A, B, count, conf))
                else:
                    failed_rules.get(A, []).append(B)
    
    print('{} rules generated. Print top {} rules:'.format(len(rules), print_num))
    rules = sorted(rules, key=lambda v: (-v[3], -v[2]))
    for i, rule in enumerate(rules):
        print('{:<3d}: [{:<40}] -> [{:<20}] occurs {} times, conf {:.2f}'.format(i+1, ', '.join(rule[0]), ', '.join(rule[1]), rule[2], rule[3]), file=stderr)
        if i + 1 == print_num:
            break
    return rules
