"""
Prepare the Shakespeare dataset for character-level language modeling.
So instead of encoding with GPT-2 BPE tokens, we just map characters to ints.
Will save train.bin, val.bin containing the ids, and meta.pkl containing the
encoder and decoder and some other related info.
"""
import os
import pickle
import requests
import numpy as np
import random
import argparse

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max_digit_num', type=int, default=3)
    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = get_args()
    cur_path = os.path.dirname(__file__)
    data_path = os.path.join(cur_path, 'data')

    content = ''
    for left_digit_num in range(1, args.max_digit_num + 1):
        for right_digit_num in range(1, args.max_digit_num + 1):
            file_name = f'mul_{left_digit_num}_{right_digit_num}.txt'
            file_path = os.path.join(data_path, file_name)
            with open(file_path, 'r') as f:
                content += f.read().strip() + '\n'
    data = content

    # get all the unique characters that occur in this text
    chars = sorted(list(set(data)))
    vocab_size = len(chars)
    print("all the unique characters:", ''.join(chars))
    print(f"vocab size: {vocab_size:,}")

    # create a mapping from characters to integers
    stoi = { ch:i for i,ch in enumerate(chars) }
    itos = { i:ch for i,ch in enumerate(chars) }
    def encode(s):
        return [stoi[c] for c in s] # encoder: take a string, output a list of integers
    def decode(l):
        return ''.join([itos[i] for i in l]) # decoder: take a list of integers, output a string

    # create the train and test splits
    data_list = data.split('\n')
    random.seed(42)
    random.shuffle(data_list)
    n = len(data_list)
    train_data_list = data_list[:int(n*0.9)]
    val_data_list = data_list[int(n*0.9):]
    train_data = '\n'.join(train_data_list)
    val_data = '\n'.join(val_data_list)

    # encode both to integers
    train_ids = encode(train_data)
    val_ids = encode(val_data)
    print(f"train has {len(train_ids):,} tokens")
    print(f"val has {len(val_ids):,} tokens")

    # export to bin files
    train_ids = np.array(train_ids, dtype=np.uint16)
    val_ids = np.array(val_ids, dtype=np.uint16)
    train_ids.tofile(os.path.join(os.path.dirname(__file__), 'train.bin'))
    val_ids.tofile(os.path.join(os.path.dirname(__file__), 'val.bin'))

    # save the meta information as well, to help us encode/decode later
    meta = {
        'vocab_size': vocab_size,
        'itos': itos,
        'stoi': stoi,
    }
    with open(os.path.join(os.path.dirname(__file__), 'meta.pkl'), 'wb') as f:
        pickle.dump(meta, f)

