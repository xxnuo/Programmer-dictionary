#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re

path_data = os.path.abspath('./data')
# path_md_dir = os.path.join(path_data,'github')
with open(os.path.join('./export.txt'), 'w') as fw:
    with open(os.path.join(path_data,'words.txt'), 'r') as fr:
        for word in fr.readlines():
            fw.write(word.strip() + ' ')

print('导出完成')
