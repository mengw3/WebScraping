# -*- coding: utf-8 -*-
# -*- coding: GBK -*-
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import excel
import xlsxwriter
import codecs


# page = requests.get('http://www.sse.com.cn/disclosure/listedinfo/announcement/index_csrc.shtml')
# soup = BeautifulSoup(page.content, "html.parser")
# links = soup.find_all('a')
# print(links)
# a = 0
# b = 0
# for link in links:
#     if (b % 2) > 0:
#         file_url = link['href']
#         print(file_url)
#         r = requests.get(file_url, stream=True)
#         with open("shangjiaosuo-stock-info"+str(a)+".pdf", "wb") as pdf:
#             for chunk in r.iter_content(chunk_size=1024):
#                 if chunk:
#                     pdf.write(chunk)
#         a += 1
#     b += 1

# url = "http://www.sse.com.cn/disclosure/listedinfo/announcement/index_csrc.shtml"
# options = webdriver.ChromeOptions()
# driver = webdriver.Chrome(chrome_options=options,
#                           executable_path=r'/Users/mengwang/PycharmProjects/HTML-scraping/chromedriver')
# driver.get(url)
# names = driver.find_elements_by_xpath("//*[@class='modal_pdf_list']//a")
# lists = []
# for i in names:
#     a = i.text
#     lists.append(a)
#     file_url = i.get_attribute("href")
#     print(file_url)
#     r = requests.get(file_url, stream=True)
#     with open("shangjiaosuo-stock-info" + str(a) + ".pdf", "wb") as pdf:
#         for chunk in r.iter_content(chunk_size=1024):
#             if chunk:
#                 pdf.write(chunk)
# driver.close()
#############################################history###############################################################

url = 'http://www.sse.com.cn/disclosure/listedinfo/announcement/index_csrc.shtml'
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(chrome_options=options,
                          executable_path=r'/Users/mengwang/PycharmProjects/HTML-scraping/chromedriver')
driver.get(url)
names = driver.find_elements_by_xpath("//*[@class='modal_pdf_list']//dd")
my_pdfs = []
for i in names:
    a = i.find_element_by_tag_name("a")
    entity = i.get_attribute("data-seecode")
    note_type = "最新公告"
    date = i.get_attribute("data-time")
    subject = a.get_attribute("title")
    source = u"证券监督委员会"
    attachment = a.get_attribute("href")
    my_pdfs.append(excel.pdf(entity, note_type, date, subject, source, attachment))
    # r = requests.get(attachment, stream=True)
    # with open("上交所StockInfo-" + str(subject) + ".pdf", "wb") as pdf:
    #     for chunk in r.iter_content(chunk_size=1024):
    #         if chunk:
    #             pdf.write(chunk)
driver.close()

workbook = xlsxwriter.Workbook(u'证券监督委员会_上交所.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
# -*- coding: utf-8 -*-
for item in my_pdfs:
    worksheet.write(row, col, item.entity)
    worksheet.write(row, col+1, item.note_type)
    worksheet.write(row, col+2, item.date)
    worksheet.write(row, col+3, item.subject)
    worksheet.write(row, col+4, item.source)
    worksheet.write(row, col+5, item.attachment)
    row += 1
workbook.close()

#######################################################################################################################
page = requests.get('http://www.csrc.gov.cn/pub/newsite/xxpl/shjspl/')
soup = BeautifulSoup(page.content, "html.parser")
# links = soup.find_all('a')
contents = soup.find('div', class_="er_right").findAll('a')
count_content = 0
row = 0
col = 0
my_pdfs = []
for content in contents:
    # print(content)
    if (count_content % 2) > 0:
        component_url = content['href']
        print(component_url)
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(chrome_options=options,
                                  executable_path=r'/Users/mengwang/PycharmProjects/HTML-scraping/chromedriver')
        driver.get(component_url)
        names = driver.find_elements_by_xpath("//*[@id='afficheShow']//li")
        my_pdfs = []
        for i in names:
            a = i.find_element_by_tag_name("a")
            attachment = a.get_attribute("href")
            print(attachment)
            # print(a)
            a = i.text
            # print(a)
            temp = a.split('\n', 2)
            # lists.append(a)
            entity = temp[0]
            print(entity)
            subject = temp[1]
            print(subject)
            date = temp[2]
            print(date)
            if count_content == 1:
                note_type = "深市主板最新公告"
            if count_content == 3:
                note_type = "深市中小板最新公告"
            if count_content == 5:
                note_type = "深市创业板最新公告"
            source = u"证券监督委员会"
            my_pdfs.append(excel.pdf(entity, note_type, date, subject, source, attachment))
            # r = requests.get(attachment, stream=True)
            # with open("深交所StockInfo-" + str(subject) + ".pdf", "wb") as pdf:
            #     for chunk in r.iter_content(chunk_size=1024):
            #         if chunk:
            #             pdf.write(chunk)

        driver.close()
        # workbook = xlsxwriter.Workbook(u'证券监督委员会_深交所'+str(count_content)+u'.xlsx')
        # worksheet = workbook.add_worksheet()
        # # -*- coding: utf-8 -*-
        # for item in my_pdfs:
        #     print(row)
        #     worksheet.write(row, col, item.entity)
        #     worksheet.write(row, col + 1, item.note_type)
        #     worksheet.write(row, col + 2, item.date)
        #     worksheet.write(row, col + 3, item.subject)
        #     worksheet.write(row, col + 4, item.source)
        #     worksheet.write(row, col + 5, item.attachment)
        #     row += 1
        # workbook.close()
    count_content += 1

workbook = xlsxwriter.Workbook(u'证券监督委员会_深交所.xlsx')
worksheet = workbook.add_worksheet()
row = 0
col = 0
# -*- coding: utf-8 -*-
for item in my_pdfs:
    worksheet.write(row, col, item.entity)
    worksheet.write(row, col+1, item.note_type)
    worksheet.write(row, col+2, item.date)
    worksheet.write(row, col+3, item.subject)
    worksheet.write(row, col+4, item.source)
    worksheet.write(row, col+5, item.attachment)
    row += 1
workbook.close()