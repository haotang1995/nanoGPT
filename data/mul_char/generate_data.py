#!/usr/bin/env python
# coding=utf-8

import os, os.path as osp

import argparse
def get_args():
    parser = argparse.ArgumentParser(description='Generate data for training')
    parser.add_argument('--max_digit_num', type=int, default=2, help='left digit')
    args = parser.parse_args()
    return args

def generate_data(left_digit_num, right_digit_num):
    curdir = osp.dirname(osp.abspath(__file__))
    data_dir = osp.join(curdir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    data_file = osp.join(data_dir, 'mul_{}_{}.txt'.format(left_digit_num, right_digit_num))
    if osp.exists(data_file):
        return

    content = ''
    for left_num in range(0, 10**left_digit_num):
        for right_num in range(0, 10**right_digit_num):
            content += '{} * {} = {}\n'.format(left_num, right_num, left_num*right_num)
    with open(data_file, 'w') as f:
        f.write(content)

def main():
    args = get_args()
    max_digit_num = args.max_digit_num
    for left_digit_num in range(1, max_digit_num+1):
        for right_digit_num in range(1, max_digit_num+1):
            generate_data(left_digit_num, right_digit_num)

if __name__ == '__main__':
    main()
