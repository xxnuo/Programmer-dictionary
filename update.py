#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sys import flags
import requests
import os
import my
from bs4 import BeautifulSoup
import re

# 全局设置
IFUPDATE = True # False: All-Language.md文件存在则不更新, True: 即使.md文件存在也更新
CONTINUEINDEX = 0 #自定义序号来继续未完成的获取，为0则不需要继续任务

# 代理设置
# proxy = '127.0.0.1:7890'
# proxies = {'http': 'http://' + proxy, 'https': 'https://' + proxy}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}

# 创建数据存储目录
path_data = os.path.abspath('./data')
path_data_all = os.path.join(path_data, 'github')
try:
    os.mkdir(path_data)
    os.mkdir(path_data_all)
    my.log('1.创建数据存储目录成功')

except FileExistsError:
    my.log('1.数据存储目录已存在')
    pass


# 获取包含所有项目仓库链接的md文件

url_md_all = [
    'https://github.com/GrowingGit/GitHub-English-Top-Charts/raw/main/content/charts/overall/software/All-Language.md',
    'https://github.com/GrowingGit/GitHub-English-Top-Charts/raw/main/content/charts/overall/knowledge/All-Language.md',
]
path_md_all = os.path.join(path_data, 'All-Language.md')

if IFUPDATE or not os.path.exists(path_md_all):
    #删除旧path_md_all文件
    if os.path.exists(path_md_all):
        os.remove(path_md_all)
    for _url in url_md_all:
        try:
            r = requests.get(_url, headers=headers, timeout=10)
            #my.log('url_md_all:' + str(r.status_code))
            if r.status_code == 200:
                # 写入md文件
                with open(path_md_all, 'a', encoding='utf-8') as f:
                    f.write(r.text)
                    my.log('2.写入All-Language.md文件成功')

        except requests.exceptions.ConnectionError as e:
            my.log('2.获取包含所有项目仓库链接的md文件出错：' + e.args)
            exit()

    my.log('3.已获取到所有All-Language.md，开始解析')

    url_md_dict =my.get_links(path_md_all)
    for i,key in enumerate(url_md_dict):
        #自定义start来继续未完成的任务
        if i < CONTINUEINDEX:
            continue
        _title,_url = key,url_md_dict[key]
        # 获取每个项目仓库的README.md文件的url
        # 取title内/前的内容为目录名
        _title_dir = _title.split('/')[0].rstrip()
        # 取title内/后的内容为文件名
        _title_file = _title.split('/')[1].rstrip()
        _file_path = os.path.join(path_data_all , _title_dir)

        # 因为部分仓库的master分支没有更新，使用的是其他分支作为主分支
        # 所以需要访问仓库网址获取默认显示的README.*文件的url
        r = requests.get(_url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'lxml')
        _readme_urls = soup.find_all('a',title = re.compile('README.*', flags=re.IGNORECASE))
        
        for x in _readme_urls:
            _url_md_single = x.get('href')
            #print(_url_md_single)
            my.log('3.'+ str(i) + '.找到：' + _url_md_single)
            
            if 'commit' in _url_md_single:
                my.log('3.'+ str(i) + '识别为commit，跳过')
                continue
            if 'vercel.app' in _url_md_single:
                my.log('3.'+ str(i) + '识别为vercel.app，跳过')
                continue

            # 替换掉url中的blob为raw
            _file_path_detail = os.path.join(_file_path, _url_md_single.split('/')[-1].rstrip())
            my.log('3.'+ str(i) + '获取并写入：' + _file_path_detail)
            _url_md_single = 'https://github.com' + _url_md_single.replace('blob', 'raw')
            #my.log('处理：'+ _url_md_single)
            _r = requests.get(_url_md_single, headers=headers, timeout=10)
            #print(_r.status_code)
            if _r.status_code == 200:
                # 写入md文件
                os.makedirs(os.path.dirname(_file_path_detail), exist_ok=True)

                with open(_file_path_detail, 'w', encoding='utf-8') as f:
                    f.write(_r.text)
            else:
                my.log('3.'+ str(i) + '获取' + _url_md_single + '文件出错：' + str(_r.status_code))

        my.log('3.'+ str(i) + '获取'+ _title +'的文件处理完成')

# README.md文件获取完成
my.log('4.更新完成')
