#!/usr/bin/env python3
from requests import get
from sys import argv


def print_to_csv(out_file,massive):
    open(out_file,'a').writelines('id;name;full_name;html_url;description;fork;created_at;updated_at;pushed_at;homepage;'
                                  'stargazers_count;has_wiki;has_pages;archived;license;score\n')
    for i in massive:
        open(out_file,'a').writelines(i+'\n')

def string_to_csv_string(my_dict):
    csv_string=''
    keys=['id', 'name', 'full_name', 'html_url', 'description', 'fork', 'created_at', 'updated_at',
          'pushed_at', 'homepage', 'stargazers_count','has_wiki', 'has_pages',  'archived',   'license', 'score']
    for i in keys:
        csv_string+=(str(my_dict[i])+';')
    return csv_string

def dicts_to_dictsString(dicts):
    strings=set()
    for dict in dicts:
        string=string_to_csv_string(dict)
        strings.add(string)
    return strings


def search_to_git(keyword):
    item_all=set()

    req=get('https://api.github.com/search/repositories?q={}&per_page=100'.format(keyword))
    item_all=item_all|dicts_to_dictsString(req.json()['items'])
    page_all=req.json()['total_count']/100
    if page_all>=10:
        page_all=10
    for i in range(2,int(page_all)+1):
        req = get('https://api.github.com/search/repositories?q={}&per_page=100&page={}'.format(keyword,i))
        item_all=item_all|dicts_to_dictsString(req.json()['items'])

    return item_all




if __name__ == '__main__':

    try:
        strings=list(search_to_git(argv[1]))
        print_to_csv(argv[2],strings)
    except IndexError:
        print('''exemple:
        ./git_search_info file_to_out keywords for search
                        ''')


