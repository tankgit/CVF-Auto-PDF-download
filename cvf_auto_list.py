# -*- coding: utf-8 -*-
import os
import requests


year_start = 2013
year_end = 2020
conf_list = ['CVPR', 'WACV', 'ICCV', 'ECCV']
site_root = 'https://openaccess.thecvf.com/'


list_root = "paper_list"

if not os.path.exists(list_root):
    os.mkdir(list_root)

def gen_conf():
    conf_year = []
    for conf in conf_list:
        for y in range(year_start, year_end + 1):
            conf_year.append(conf + str(y))
    return conf_year


def find_sub(conf_url):
    content = requests.get(conf_url + '.py').text
    lines = content.split('\n')
    if lines[2].find('404 Not Found') > -1: return []

    res = []
    for line in lines:
        if line.find('>Day ') > -1:
            res.append(site_root + line.split('"')[1])
    if not res: res.append(conf_url)
    return res

def fetch_list(i, url, n):
    content = requests.get(url).text
    pdf_list = []
    lines = content.split('\n')
    for line in lines:
        if line.find('>pdf</a>]') > -1:
            pdf = line.split('"')[1]
            pdf_list.append(site_root + pdf + '\n')
    return pdf_list

def save_list(cy, num, pdf_list):
    conf, year = cy[:4], cy[4:]
    save_path = os.path.join(list_root, year, conf)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    with open(os.path.join(save_path, "{}-{}.list".format(cy, num)), 'w') as f:
        f.writelines(pdf_list)


if __name__ == '__main__':
    conf_year = gen_conf()
    for i, cy in enumerate(conf_year):
        print("\033[32;1m[ {}/{} - {} ]\033[0m".format(i + 1, len(conf_year), cy), end='')
        pages = find_sub(site_root + cy)
        if not pages: 
            print("\033[31m  Not Found\033[0m\n")
            continue
        print("\033[33m  Found {} page(s)\033[0m".format(len(pages)))
        for i, page in enumerate(pages):
            pdf_list = fetch_list(i, page, len(pages))
            print("- Get \033[34;1m{}\033[0m PDF(s) from {}".format(len(pdf_list), page))
            save_list(cy, i + 1, pdf_list)
        print()
