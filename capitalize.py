# Copyright 2024  Jeongkyun Park
#           2024  Sogang University, Korea
# Apache 2.0

import re
import sys
import tqdm
import json
import tqdm
from shutil import copy
from itertools import zip_longest
from typing import List, Dict, Union



def extract_target(sentence):
    uid, *words = sentence.split()
    return " ".join(words), uid

def envelop_target(sentence, uid):
    return " ".join([uid, sentence])

def capitalize_sentence(sentence, dic, max_word_num:int=5):
    # Initialize the sentence by lowercases
    sentence = sentence.lower()
    words = sentence.split()
    # Key lengths follow non-decreasing order.
    for word_num in tqdm.tqdm(range(1, max_word_num+1), position=1, leave=False):
        for sid in range(0, len(words)-word_num+1):
            key = (" ".join(words[sid:sid+word_num])).lower()
            if cap:=dic.get(key, None):
                words[sid:sid+word_num] = cap.split()
    words[0] = words[0].capitalize()
    sentence = " ".join(words)
    return sentence
    

def main(sentences:List[str], dic:Dict[int, Dict[str, int]], limit_score:Union[int, List[int]]=[5000, 2000, 1000]):
    # Map
    low2up = {}
    max_word_num = None
    for plen, subdic in dic.items():
        for key, value in subdic.items():
            low2up[key.lower()] = key
            max_word_num = int(plen)
    
    # Captialize loop
    for sid, sentence in enumerate(tqdm.tqdm(sentences, position=0)):
        # Set the range of the modification
        target, *others = extract_target(sentence)
        # Do capitalize
        target = capitalize_sentence(target, low2up, max_word_num=max_word_num)
        # Restore the original form
        sentence = envelop_target(target, *others)
        # Register
        sentences[sid] = sentence

    return sentences


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Arguments should be passed. \nExample: `python gather_dictionary.py {TARGET_TEXT_PATH} {DICTIONARY_PATH}`"
    target_path, dic_path = sys.argv[1:]
    
    copy(target_path, target_path+".backup")
    
    with open(target_path) as f:
        sentences = f.readlines()
    
    with open(dic_path) as f:
        dic = json.load(f)
    
    sentences = main(sentences, dic)
    
    with open(target_path, "w") as wf:
        for sentence in sentences:
            wf.write(sentence+"\n")
