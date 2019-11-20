# -*- coding: utf-8 -*-
# -*- coding: GBK -*-
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import xlsxwriter
import codecs
import random
import json
import datetime
import re
import sys


class WebScraper:
    sec_code = ""
    entity = ""
    note_type = ""
    date = ""
    subject = ""
    source = ""
    attachment = ""

    def __init__(self, sec_code, entity, note_type, date, subject, source, attachment):
        self.sec_code = sec_code
        self.entity = entity
        self.note_type = note_type
        self.date = date
        self.subject = subject
        self.source = source
        self.attachment = attachment

    def __str__(self):
        return "" + self.entity + self.note_type + self.date + self.subject + self.source + self.attachment


def request_data_from_url(url1, data1, headers1):
    rep = requests.post(url=url1, data=json.dumps(data1), headers=headers1)
    return rep.content


def note_type_filter(name):
    if u"半年度报告摘要" in name:
        return u"半年报摘要"
    if u"半年度报告" in name:
        return u"半年报"
    if u"年度报告摘要" in name:
        return u"年报摘要"
    if u"年度报告" in name:
        return u"年报"
    if u"第一季度报告" in name:
        return u"第一季度季报"
    if u"第三季度报告" in name:
        return u"第三季度季报"
    return u"其他"


def get_excel_for_shenjiaosuo(pages, download):  # total num is pages*30
    total_page = int(pages/10) + 1  # Pages of data got
    current_page = 1
    headers = {'Content-Type': 'application/json'}
    stack_data = []
    download_url = "http://disc.static.szse.cn/download"
    for page in range(current_page, total_page):
        my_random = random.uniform(0, 1)
        url = "http://www.szse.cn/api/disc/announcement/annList?random=" + str(my_random)
        data = {"channelCode": ["fixed_disc"], "pageSize": 10, "pageNum": page, "stock": []}
        json_str = request_data_from_url(url, data, headers)
        response = json.loads(json_str)["data"]
        for obj in response:
            title = obj["title"]
            sec_code = "".join(obj["secCode"])
            sec_name = "".join(obj["secName"])
            publish_time = obj["publishTime"]
            source = u"深圳证券交易所"
            attachment = download_url + obj["attachPath"]
            note_type = note_type_filter(title)
            stack_data.append(WebScraper(sec_code, sec_name, note_type, publish_time, title, source, attachment))
            title = re.sub('[*]', '', title)

            # delete * in filename
            if download:
                r = requests.get(attachment, stream=True)
                with open(title + ".pdf", "wb") as pdf:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:
                            pdf.write(chunk)
                print(title + "downloaded")
    # Write Excel
    workbook = xlsxwriter.Workbook(u'证券监督委员会_深交所.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    for item in stack_data:
        worksheet.write(row, col, item.sec_code)
        worksheet.write(row, col + 1, item.entity)
        worksheet.write(row, col + 2, item.note_type)
        worksheet.write(row, col + 3, item.date)
        worksheet.write(row, col + 4, item.subject)
        worksheet.write(row, col + 5, item.source)
        worksheet.write(row, col + 6, item.attachment)
        row += 1
    workbook.close()


def str_to_bool(string):
    return True if string.lower() == 'true' else False


def main(argv):
    if len(argv) != 3:
        print("""give wrong number of parameters for SZ""")
        return
    if len(argv) == 3:
        get_excel_for_shenjiaosuo(int(argv[2]), str_to_bool(argv[1]))
        return


if __name__ == "__main__":
    # Users should type in a sentence with following format: "True/False number" (e.g. "False 1000").
    # True/False means if users need download pdf documents.
    # Number means the number of documents users want to download.
    print("Start")
    main(sys.argv)
    print("Finished")

