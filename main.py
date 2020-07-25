from baseline import baseline
from apriori import apriori
from data import load_grocery_dataset, load_unix_usage_dataset
from rules import generate_rules
import time
import os
import psutil

if __name__ is '__main__':
    print('==========DATASET: grocery==========')
    print('=============Baseline===============')
    print('====================================')
    tic = time.time()
    grocery = load_grocery_dataset()
    result = baseline(grocery, min_sup=0.01)
    generate_rules(result, min_conf=0.5)
    print('Baseline time cost {:.6f}'.format(time.time() - tic))
    print('Memory cost {}'.format(psutil.Process(os.getpid()).memory_info().rss))
    print('====================================')
    print()

    print('==========DATASET: grocery==========')
    print('==============Apriori===============')
    print('====================================')
    tic = time.time()
    grocery = load_grocery_dataset()
    result = apriori(grocery, min_sup=0.01)
    generate_rules(result, min_conf=0.5)
    print('Apriori time cost {:.6f}'.format(time.time() - tic))
    print('Memory cost {}'.format(psutil.Process(os.getpid()).memory_info().rss))
    print('====================================')
    print('\n')

    for i in range(9):
        print('=========DATASET: UNIX-USER{}========='.format(i))
        print('=============Baseline===============')
        print('====================================')
        tic = time.time()
        unix = load_unix_usage_dataset(i)
        result = baseline(unix, min_sup=0.02)
        generate_rules(result, min_conf=0.8)
        print('Baseline time cost {:.6f}'.format(time.time() - tic))
        print('====================================')
        print()

        print('=========DATASET: UNIX-USER{}========='.format(i))
        print('==============Apriori===============')
        print('====================================')
        tic = time.time()
        unix = load_unix_usage_dataset(i)
        result = apriori(unix, min_sup=0.02)
        generate_rules(result, min_conf=0.8)
        print('Apriori time cost {:.6f}'.format(time.time() - tic))
        print('====================================')
        print('\n')

    print('=======DATASET: UNIX-USER-all======='.format(i))
    print('=============Baseline===============')
    print('====================================')
    tic = time.time()
    unix = load_unix_usage_dataset()
    result = baseline(unix, min_sup=0.02)
    generate_rules(result, min_conf=0.8)
    print('Baseline time cost {:.6f}'.format(time.time() - tic))
    print('====================================')
    print()

    print('=======DATASET: UNIX-USER-all======='.format(i))
    print('==============Apriori===============')
    print('====================================')
    tic = time.time()
    unix = load_unix_usage_dataset()
    result = apriori(unix, min_sup=0.02)
    generate_rules(result, min_conf=0.8)
    print('Apriori time cost {:.6f}'.format(time.time() - tic))
    print('\n')