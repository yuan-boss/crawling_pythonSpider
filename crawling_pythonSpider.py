#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import os
import sys
import imp
imp.reload(sys)
from termcolor import colored, cprint

error_print = lambda x: cprint(x, "red")
success_print = lambda x: cprint(x, 'green', attrs=['underline'])
tip_print = lambda x: cprint(x, 'yellow')
banner_print = lambda x: cprint(x, 'magenta', attrs=['concealed'])

def banner():
    banner_print(f'{35*"-"} 面向对象之爬取 pythonSpider 网页数据实战 {34*"-"}')
    banner_print(f'{15 * " "}version:0.1 | made by yuanboss | date:2023/09/19{15 * " "}')
    banner_print(f'{88*"*"}')
    banner_print(f'{40*"-"}yuanboss{40*"-"}')
    banner_print(""" 
                                                   .o8                                   
                                                  "888                                   
    oooo    ooo oooo  oooo   .oooo.   ooo. .oo.    888oooo.   .ooooo.   .oooo.o  .oooo.o 
     `88.  .8'  `888  `888  `P  )88b  `888P"Y88b   d88' `88b d88' `88b d88(  "8 d88(  "8 
      `88..8'    888   888   .oP"888   888   888   888   888 888   888 `"Y88b.  `"Y88b.  
       `888'     888   888  d8(  888   888   888   888   888 888   888 o.  )88b o.  )88b 
        .8'      `V88V"V8P' `Y888""8o o888o o888o  `Y8bod8P' `Y8bod8P' 8""888P' 8""888P' 
    .o..P'                                                                               
    `Y8P'                                                                                                                                                                    
        """)
    banner_print(f'{88*"*"}')
    banner_print(f'{40*"-"}yuanboss{40*"-"}')

# 提示
def tip():
    tip_print(f"""
    简介：该工具使用面向对象的编程思想进行编码，结合爬虫，完成对部署在本地的 pythonSpider 网页的信息爬取
    {100*'='}
    请输入要爬取的python-spider的url:http://127.0.0.1/python-spider/
    {100*'='}\n
    """)

class MyWeb():
    def __init__(self, url):
        ua = UserAgent()
        headers = {"User-Agent": ua.random}
        self.url = url
        self.headers = headers

    def get_soup(self):
        resp = requests.get(self.url, headers=self.headers)
        self.source = resp.text
        # 获取爬虫对象
        self.soup = BeautifulSoup(self.source, "lxml")
        return self.soup

    def get_js(self, soup):
        self.js_urls = []
        script_soup = soup.find_all('script', {'src': True})
        for script in script_soup:
            # 获取js的url路径
            js_url = self.url + script.get('src')
            self.js_urls.append(js_url)
        return self.js_urls

    def get_pic_url(self, soup):
        # 定义图片地址列表
        self.pic_url = []
        imgs = soup.find_all('img')
        # 通过 beautifulsoup 获取 图片地址并存入地址列表
        for index in range(0, len(imgs)):
            # 获取图片的url路径
            pic_url = self.url + imgs[index].get('src')
            self.pic_url.append(pic_url)
        return self.pic_url
    def dir_exist(self,dir_name):
        folder = os.path.exists(dir_name)
        if not folder:
            error_print(f'文件夹:{dir_name[0:-1:]}-----不存在，正在爬取js源码，图片，与网页源代码')
            return False
        else:
            banner_print(f'文件夹:{dir_name[0:-1:]}-----存在，将会追加并覆盖文件夹内容')
            return True

    def get_index(self):
        tip_print('正在爬取源码到index.html中......')
        with open('index.html', 'wb') as f:
            html = requests.get(self.url, headers=self.headers).content
            f.write(html)
        f.close()
        success_print('网页源代码下载完成')

    def download_pic(self, pic_url_list):

        # 获取当前目录
        self.current_dir = os.getcwd()
        self.pic_path = 'pictures/'
        # 拼接新文件夹的路径字符串
        pic_path_folder = os.path.join(self.current_dir, self.pic_path)
        # 创建图片目录
        # 如果存在,则创建
        exist = self.dir_exist(pic_path_folder)
        tip_print('正在下载图片到pictures目录中......')
        if not exist:
            os.makedirs(pic_path_folder)
        else:
            pass
        for pic_url in pic_url_list:
            pic_name = pic_url[pic_url.rindex('/') + 1::]
            with open(self.pic_path + pic_name, 'wb') as f:
                img = requests.get(pic_url, headers=self.headers).content
                f.write(img)
        f.close()
        success_print('图片下载完成')
    def download_js(self, js_url_list):
        self.current_dir = os.getcwd()
        self.js_path = 'js/'
        # 拼接新文件夹的路径字符串
        js_path_folder = os.path.join(self.current_dir, self.js_path)
        # 创建JS目录
        # 如果存在,则创建
        exist = self.dir_exist(js_path_folder)
        tip_print('正在下载js源码到js目录中......')
        if not exist:
            os.makedirs(js_path_folder)
        else:
            pass
        for js_url in js_url_list:
            js_name = js_url[js_url.rindex('/') + 1::]
            with open(self.js_path + js_name, 'wb') as f:
                js = requests.get(js_url, headers=self.headers).content
                f.write(js)
        f.close()
        success_print('JS源码下载完成')


if __name__ == '__main__':
    banner()
    tip()
    url = input('请输入要爬取的python-spider的url:')
    web = MyWeb(url)
    # 获取爬虫对象
    soup = web.get_soup()
    # 获取图片地址
    pic_url_list = web.get_pic_url(soup)
    # 下载html源码到本地
    web.get_index()
    # 下载图片到本地
    web.download_pic(pic_url_list)
    # 下载JS源码到本地
    js_url_list = web.get_js(soup)
    web.download_js(js_url_list)