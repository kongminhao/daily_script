#!/usr/bin/env python
# coding:utf-8
try:
    import cookielib
except:
    import http.cookiejar as cookielib

import requests

from bs4 import BeautifulSoup
from prettytable import PrettyTable
import json

class Baidu(object):
    """贴吧签到"""
    def __init__(self):
        self.sign_url = (
            "http://tieba.baidu.com/sign/add")
        self.sess = requests.Session()
        self.sess.timeout = 30
        with open('cookies', 'r') as cookies:
            self.sess.headers = {
                "Cookie": cookies.read(),
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"),
            }


    def sign_single_ba(self, kw):
        """单个吧签到"""
        url = self.sign_url
        tbs = self.sess.get("http://tieba.baidu.com/dc/common/tbs").text
        tbs = json.loads(tbs)["tbs"]
        postdata = {"ie":"utf-8", "tbs":tbs, "kw":kw}

        try:
            html = self.sess.post(url, data=postdata,timeout=30).text
        except:
            print("timeout, sign again.")
            html = self.sess.post(url, data=postdata,timeout=30).text
        html_json = json.loads(html)
        if html_json["no"] == 0 or html_json["no"] == 1101:
            return "签到成功"
        else:
            return "签到异常"


    def get_info(self):
        """获取个人关注贴吧，以及各贴吧经验，等级并返回"""
        myFavor = 'http://tieba.baidu.com/mo/m?tn=bdFBW&tab=favorite'
        html = self.sess.get(myFavor).text
        # print(html)
        # print(str(self.sess.cookies))
        soup = BeautifulSoup(html, 'html.parser')
        allLabel = soup.find_all('td')
        kws = [item.text.split('.')[-1] for
               item in allLabel[::3]]
        levels = [item.text for item in allLabel[1::3]]
        exercises = [item.text for item in allLabel[2::3]]
        return [kws, levels, exercises]

    def sign_all_ba(self):
        """每个页的每个贴吧签到"""
        table = PrettyTable([u'贴吧', u'签到状态'])
        table.padding_width = 2

        kws = self.get_info()[0]
        for index, kw in enumerate(kws):
            import time
            time.sleep(10)
            try:
                status = self.sign_single_ba(kw)
            except IndexError:
                status = u'签到异常.'
            print(u'{0}\t\t{1}'.format(kw, status))
            table.add_row([kw, status])
        kws, levels, exercises = self.get_info()
        table.add_column(u'经验', exercises)
        table.add_column(u'等级', levels)
        print(table)
        print(u'共{0}个吧'.format(len(levels)))


def start():
    tieba = Baidu()
    tieba.sign_all_ba()

if __name__ == '__main__':
    start()
