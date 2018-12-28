# -*- coding:utf-8 -*-
__date__ = '17/3/10 上午12:47'

import requests
import re,json,os
from user_agent import generate_user_agent
from mxonline.settings import MEDIA_ROOT
import esm,codecs




def get_onepage_keyword(keyword,page):          #获取某个关键字某一页商品title
    keyword_all=[]
    headers={'User-Agent':generate_user_agent()}
    r=requests.get('https://s.taobao.com/search?q='+keyword+'&s='+str(page*44),headers=headers)
    r=re.findall("raw_title\":\"(.*?)\"\,",r.text)
    if len(r)>0:

        for n in  r:
            keyword_all.append(n)
        return keyword_all





def get_all_title(keyword,pages=30):
    # title_all=[keyword,'fdsfdsfds']
    keyword_all_all=[]
    title_all=[]
    for page in range(pages):
        a=get_onepage_keyword(keyword,page)
        if a is not None:
            keyword_all_all.append(a)
    for n1 in keyword_all_all:
        for n2 in n1:
            title_all.append(n2.strip().lower())
    title_all = list(set(title_all))


    if len(title_all)>0:
            return "\n".join(title_all)
    else:
        return None



def filter_branch(title_all,good_type):




    file_path_branch = MEDIA_ROOT + '/taoke_data/branch/' + good_type + '.txt'
    if os.path.exists(file_path_branch) == True and len(title_all) > 0:

        with codecs.open(file_path_branch, 'r', 'utf8') as csvfile:
            index = esm.Index()
            branch_filter = []
            for line_one in csvfile:
                index.enter(line_one.strip())
            index.fix()


            a = index.query(title_all)
            for aaaaa in a:
                branch_filter.append(aaaaa[1])

            branch_filter_distinct = {k: branch_filter.count(k) for k in set(branch_filter)}
            str_branch=""
            branch_filter_distinct=sorted(branch_filter_distinct.items(), key=lambda d:d[1], reverse = True)

            str_branch_distinct=""

            for one_key in branch_filter_distinct:
                if len(one_key[0].strip())>1:
                    str_branch = str_branch + one_key[0] + ':' + str(one_key[1]) + '\n'
                    str_branch_distinct=str_branch_distinct+one_key[0]+'|'

            return str_branch,str_branch_distinct


