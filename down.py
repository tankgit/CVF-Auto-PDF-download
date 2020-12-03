# -*- coding: utf-8 -*-
import os
import requests
import math

list_root = "paper_list"

# set empty to download all, or set to download specific lists
filter_year = [] # ["2018","2019","2020"]
filter_conf = [] # ["CVPR","ICCV"]
ignore_name = ['.DS_Store']
limit_number = 0 # limited downlading for each list file, 0 means no limit.

def file_filter(target, filter):
    return (target in ignore_name) or (filter and target not in filter)

def human(size):
    unit = 'B'
    if size > 1024:
        size /= 1024
        unit = 'KB'
        if size > 1024:
            size /= 1024
            unit = 'MB'
    return size, unit

def down_file(i, n, lst, save_path, pdf_url):
    pdf_name = os.path.basename(pdf_url)
    print("\033[31;01mDownload:\033[0;31m {}\033[0m".format(pdf_name))
    with open(os.path.join(save_path, pdf_name), "wb") as f:
        print("  connecting server...", end='\r')
        response = requests.get(pdf_url, stream=True)
        total_length = int(response.headers.get('Content-Length'))
        if total_length is None: # no content length header
            f.write(response.content)
        else:
            pg = 0
            total_block = 20
            block_size = 4096
            unit = total_block / (total_length / block_size)
            for data in response.iter_content(chunk_size=block_size):
                f.write(data)
                pg += 1
                block = math.ceil(unit * pg)
                print("- \033[34;01m{}/{}\033[0m of {} |".format(i, n, lst), end='')
                for _ in range(block): print("█", end='')
                for _ in range(total_block - block + 1): print(" ", end='')
                curr_size, curr_unit = human(pg * 4096)
                total_size, total_unit = human(total_length)
                print('| \033[32;01m{:.1f}%\033[0m - {:.1f} {} / {:.1f} {}   \t\t'.format(pg * 4096 / total_length * 100, curr_size, curr_unit, total_size, total_unit), end='\r')
            print()


for year in os.listdir(list_root):
    if file_filter(year, filter_year): continue
    path1 = os.path.join(list_root, year)
    for conf in os.listdir(path1):
        if file_filter(conf, filter_conf): continue
        path2 = os.path.join(path1, conf)
        i = 0
        files = os.listdir(path2)
        n_pdf = 0
        for f in files:
            if f[-3:] == 'pdf': n_pdf += 1
        for lst in files:
            if lst[-4:] == "list":
                lst_path = os.path.join(path2, lst)
                with open(lst_path, 'r') as l:
                    lines = l.readlines()
                    j = 0
                    for pdf in lines:
                        i += 1
                        j += 1
                        if i < n_pdf: continue
                        if limit_number != 0 and j > limit_number: break
                        else: down_file(i, limit_number if limit_number != 0 and len(lines) > limit_number else len(lines), lst, path2, pdf.strip())


