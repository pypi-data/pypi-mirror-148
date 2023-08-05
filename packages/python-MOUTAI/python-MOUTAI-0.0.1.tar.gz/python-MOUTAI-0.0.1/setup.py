#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: 程序员晚枫
# Mail: 1957875073@qq.com
# Created Time:  2022-4-19 10:17:34
# Description: https://mp.weixin.qq.com/s/zzD4pxNMFd0ZuWqXlVFdAg
#############################################

from setuptools import setup, find_packages            #这个包没有的可以pip一下

setup(
    name = "python-MOUTAI",      #这里是pip项目发布的名称
    version = "0.0.1",  #版本号，数值大的会优先被pip
    keywords = ("pip", "python-MOUTAI"),
    description = "python for wps",
    long_description = "项目使用说明：https://mp.weixin.qq.com/s/n9AN6Z-60Rws_qJ-6XITXg",
    license = "MIT",
    url = "https://gitee.com/CoderWanFeng/python-office",     #项目相关文件地址，一般是github。考虑国内用户上网问题，本项目主要使用gitee
    author = "程序员晚枫",
    author_email = "1957875073@qq.com",
    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = [
        'pandas',
        'xlrd',
        'xlwt',
        'xlutils',
        'xlwings',
        'openpyxl',
        'lxml>=2.3.2',
        'python-docx',
        'python-pptx',
        'PyPDF2',
        'scrapy',
        'django',
        'flask',
        'matplotlib',
        'easyocr',
    ],#这个项目需要的第三方库
    python_requires='>=3.6',
)

# 'Django >= 1.11, != 1.11.1, <= 2',

