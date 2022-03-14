#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

path_data = os.path.abspath('./data')
path_md_dir = os.path.join(path_data,'github')
path_mds_full = []

for dirpath, dirnames, filenames in os.walk(path_md_dir):
    for filename in filenames:
        path_mds_full.append(os.path.join(dirpath, filename))

#获取了所有的md文件的路径到列表path_mds_full
#print(path_mds_full)
words = {}
lwords = []

reUrl = re.compile(r'[http|https]*://[a-zA-Z0-9.?/&=:]*', re.S)

for path_md in path_mds_full:
    with open(path_md, 'r') as f:
        #获取每一行
        for line in f.readlines():
            #去除每一行的http网址
            line = re.sub(reUrl, '', line)
            #替换每一行的非英文字符为空格
            line = re.sub(r'[^a-zA-Z]', ' ', line)
            #将每一行英文转为小写
            line = line.lower()

            print(line)

            #将每一行的单词分割开
            r = line.split()
            for word in r:
                #排除过长的单词
                if len(word) < 32:
                    #将每一个单词作为key，记录出现的次数作为value
                    if word in words:
                        words[word] += 1
                    else:
                        words[word] = 1
#提取出words中的key到lwords
for key in words:
    lwords.append(key)
#print(lwords)
#按行保存lwords中的单词到文件
with open(os.path.join(path_data,'words.txt'), 'w') as f:
    for word in lwords:
        f.write(word + '\n')
    print('保存成功')
