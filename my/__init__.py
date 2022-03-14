import time
import re

# 简单记录日志
def log(msg):
    print(time.strftime('%H:%M:%S', time.localtime(time.time())) + ' > ' + msg)

# 向数据目录覆盖写入md文件
def write_md(path_to_md_file, md_content):
    with open(path_to_md_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
        log('写入md文件成功')

# 使用正则表达式从md文件中提取出链接的标题和链接
def get_links(path_to_md_file):
    with open(path_to_md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
        # 提取出所有链接
        links = re.findall(r'\[.*?\]\(.*?\)', md_content)
        # 提取出links中的url
        links_url = [re.findall(r'\(.*?\)', i)[0][1:-1] for i in links]
        # 提取出links中的标题
        links_title = [re.findall(r'\[.*?\]', i)[0][1:-1] for i in links]
        # 将标题和链接组合成字典
        links_dict = {}
        for i in range(len(links)):
            links_dict[links_title[i]] = links_url[i]
        return links_dict
