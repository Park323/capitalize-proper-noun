# Copyright 2024  Jeongkyun Park
#           2024  Sogang University, Korea
# Apache 2.0

import re
import sys
import tqdm
import json
from itertools import zip_longest
from typing import Dict, Union, List


def main(dic:Dict[int, Dict[str, int]], least_cnt:int=1, max_key_len:int=20, max_key_num:int=5, limit_score:Union[int, List[int]]=[5000, 2000, 1000]):
    new_dic = {}
    lower2capital = {}
    
    for length, limit in zip_longest(dic, limit_score, fillvalue=limit_score[-1]):
        subdic = dic[length]
        length = int(length)
        # Limit the number of words
        if length > max_key_num:
            continue
        new_dic[length] = {}
        for key, count in subdic.items():
            # Limit key length
            if len(key) > max_key_len or count < least_cnt:
                continue
            # Limit the number of appearance
            if count < limit:
                continue
            # Choose candidate with the maximum counts
            if cap:=lower2capital.get(key.lower(), None):
                if new_dic[length][cap] > count:
                    print(f"Keep {cap} instead of {key}")
                    continue
            # Register the key
            lower2capital[key.lower()] = key
            new_dic[length][key] = count
    
    return new_dic
    

if __name__ == "__main__":
    assert len(sys.argv) == 3, "Arguments should be passed. \nExample: `python gather_dictionary.py {DICTIONARY_PATH} {NEW_DICTIONARY_PATH}`"
    with open(sys.argv[1]) as f:
        dic = json.load(f)
    
    new_dic = main(dic)
    
    with open(sys.argv[2], "w") as f:
        json.dump(new_dic, f)