# Copyright 2024  Jeongkyun Park
#           2024  Sogang University, Korea
# Apache 2.0

import re
import sys
import tqdm
import json
from typing import List, Union


def main(paths:Union[str, List[str]], save_path:str=None, max_key_num:int=5):
    proper_dic = {1:{}}
    lower2capital = {}
    
    if isinstance(paths, str):
        paths = [paths]
    
    full_text = ""
    for path in paths:
        with open(path) as f:
            full_text += f.read() + "\n"
        
    sentences = re.split("[.\n]", full_text)
    
    for sentence in tqdm.tqdm(sentences):
        words = sentence.strip().split()[1:]
        proper_seqs = []
        for wid, word in enumerate(words):
            for wlen in range(2, max_key_num+1):
                if wid+2 > wlen:
                    word_seq = " ".join(words[wid-wlen+1:wid+1])
                    if cap:=lower2capital.get(word_seq, None):
                        proper_dic[wlen][cap] -= 1

            if word[0].isupper():
                # Clean a word
                word = re.sub("[^\w\d']", "", word)
                # Add a word to the dictionary
                proper_dic[1][word] = proper_dic[1].get(word, 0) + 1
                lower2capital[word.lower()] = word
                # Continuous capital words
                proper_seqs.append(word)
            elif cap:=lower2capital.get(word, None):
                proper_dic[1][cap] -= 1
            else:
                # Finish the captial words
                if (diclen:=len(proper_seqs)) > 1 and max_key_num >= diclen:
                    if not proper_dic.get(diclen, None):
                        proper_dic[diclen] = {}
                    word_seq = " ".join(proper_seqs)
                    proper_dic[diclen][word_seq] = proper_dic[diclen].get(word_seq, 0) + 1
                    lower2capital[word_seq.lower()] = word_seq
                proper_seqs = []
        # Last words
        if (diclen:=len(proper_seqs)) > 1 and max_key_num >= diclen:
            if not proper_dic.get(diclen, None):
                proper_dic[diclen] = {}
            word_seq = " ".join(proper_seqs)
            proper_dic[diclen][word_seq] = proper_dic[diclen].get(word_seq, 0) + 1
            lower2capital[word_seq.lower()] = word_seq
    
    save_path = save_path if save_path else "./proper.json"
    with open(save_path, "w") as f:
        json.dump(proper_dic, f)


if __name__ == "__main__":
    assert len(sys.argv) > 1, "Arguments should be passed. \nExample: `python gather_dictionary.py ${SAVEPATH} ${TEXTPATH}`"
    save_path, *paths = sys.argv[1:]
    
    main(paths, save_path)
    