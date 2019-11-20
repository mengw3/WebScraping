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


def get_excel_for_shangjiaosuo(begin, end, download):
    total_num = 5000
    stock_data = []
    begin_date = str(datetime.date(int(begin[0]), int(begin[1]), int(begin[2])))  # begin date to change
    end_date = str(datetime.date(int(end[0]), int(end[1]), int(end[2])))  # end date to change
    response = requests.get(
        'http://query.sse.com.cn/infodisplay/queryLatestBulletinNew.do?&jsonCallBack=jsonpCallback43752&productId=&reportType2=DQGG&reportType=ALL&beginDate=' + begin_date + '&endDate=' + end_date + '&pageHelp.pageSize='+str(total_num)+'&pageHelp.pageCount=50&pageHelp.pageNo=1&pageHelp.beginPage=1&pageHelp.cacheSize=1&pageHelp.endPage=5&_=1566674248173'
        ,
        headers={'Referer': 'http://www.sse.com.cn/disclosure/listedinfo/regular/'}
    )
    # print(response.text)
    json_str = response.text[19:-1]
    data = json.loads(json_str)
    for report in data['result']:
        attachment = 'http://www.sse.com.cn/' + report['URL']
        title = report['title']
        security_code = report['security_Code']
        date = report['SSEDate']
        note_type = report['bulletin_Type']
        source = u"上海证券交易所"
        stock_data.append(WebScraper(security_code, security_code, note_type, date, title, source, attachment))
        title = re.sub('[*]', '', title)

        if download:
            r = requests.get(attachment, stream=True)
            with open(title + ".pdf", "wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)
            print(title + "downloaded")

    # Write Excel
    workbook = xlsxwriter.Workbook(u'证券监督委员会_上交所.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    for item in stock_data:
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
    if len(argv) != 4:
        print("""give wrong number of parameters for SH""")
        return
    if len(argv) == 4:
        get_excel_for_shangjiaosuo(argv[2].split("."), argv[3].split("."), str_to_bool(argv[1]))
        return


if __name__ == "__main__":
    # Users should type in a sentence with following format: "True/False BeginDate EndDate"
    # (e.g. "True 2019.4.7 2019.5.19").
    # True/False means if users need download pdf documents.
    # BeginDate and EndDate restrict info's date range.
    print("Start")
    main(sys.argv)
    print("Finished")
