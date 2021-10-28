from base_tokenizer import BaseTokenizer
import pandas as pd
import numpy as np
import re

#data = pd.read_excel("C:/Users/ASUS/Desktop/New folder/core_nlp/tokenization/data.xlsx")
#y = np.array(data['after'])
#xử lý dữ liệu rf.write(v) ghi file
y=[]
wf = open('wf.txt', 'w', encoding = "utf8")
with open('vietan.data1', 'r', encoding = "utf8") as f:
    for s_line in f:
        s_line = s_line.split("-",1)
        substring = s_line[0]
        viet = substring.lstrip("@")
        v = re.sub(r'[\n\t]*', '', viet)
        y.append(v.lower())
        wf.write(v+'\n')

class LongMatchingTokenizer(BaseTokenizer):

    def tokenize(self, text):
        """
        Tokenize text using long-matching algorithm
        :param text: input text
        :return: tokens
        """
        syllables = LongMatchingTokenizer.syllablize(text)
        syl_len = len(syllables)
        curr_id = 0
        word_list = []
        done = False
        while (curr_id < syl_len) and (not done):
            curr_word = syllables[curr_id]
            if curr_id >= (syl_len - 1):
                word_list.append(curr_word)
                done = True
            else:
                next_word = syllables[curr_id + 1]
                pair_word = ' '.join([curr_word.lower(), next_word.lower()])
                if curr_id >= (syl_len - 2):
                    if pair_word in y:
                        word_list.append('_'.join([curr_word, next_word]))
                        curr_id += 2
                    else:
                        word_list.append(curr_word)
                        curr_id += 1
                elif curr_id >= (syl_len - 3):
                    next_next_word = syllables[curr_id + 2]
                    triple_word = ' '.join([pair_word.lower(), next_next_word.lower()])
                    if triple_word in y:
                        word_list.append('_'.join([curr_word, next_word, next_next_word]))
                        curr_id += 3
                    elif pair_word in y:
                        word_list.append('_'.join([curr_word, next_word]))
                        curr_id += 2
                    else:
                        word_list.append(curr_word)
                        curr_id += 1
                else:
                    next_next_word = syllables[curr_id + 2]
                    triple_word = ' '.join([pair_word, next_next_word.lower()])
                    f_w = syllables[curr_id + 3]
                    
                    fw = ' '.join([curr_word.lower(), next_word.lower(), next_next_word.lower(), f_w.lower()])
                    if fw in y:
                        word_list.append('_'.join([curr_word, next_word, next_next_word, f_w]))
                        curr_id += 4
                    elif triple_word in y:
                        word_list.append('_'.join([curr_word, next_word, next_next_word]))
                        curr_id += 3
                    elif  pair_word in y:
                        word_list.append('_'.join([curr_word, next_word]))
                        curr_id += 2
                    else:
                        word_list.append(curr_word)
                        curr_id += 1
                        
                        
        return word_list


"""Tests"""


def test():
    lm_tokenizer = LongMatchingTokenizer()
    t = open('t.txt', 'r', encoding = "utf8")
    data1 = t.read()   
    tokens = lm_tokenizer.tokenize(data1)
    with open('t1.tok.txt', 'w', encoding = "utf8") as s:
        s.write(' '.join(tokens))
if __name__ == '__main__':
    test()

