import os
import shutil
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import random

import requests
from bs4 import BeautifulSoup

# 今天日期的字符串
# today_str = datetime.datetime.today().strftime("%Y-%m-%d")
today_str = "2019-07-05"

# 当前工作目录
project_path = os.getcwd()

# 日志目录
log_path = project_path + os.sep + "log" + os.sep

# 附件目录
attachment_path = project_path + os.sep + "attachment" + os.sep
# 当天附件保存在一个以日期命令的文件夹中
attachment_path_today = attachment_path + today_str + os.sep

# 关键字眼
key_array = [u"年度报告"]


# 初始化一些环境
def init():
    # 初始化附件目录
    if not os.path.exists(attachment_path):
        os.mkdir(attachment_path)
    # 每次都清空当日附件文件夹中的文件，重新下载
    if os.path.exists(attachment_path_today):
        shutil.rmtree(attachment_path_today)
    os.mkdir(attachment_path_today)
    # 初始化日志目录
    if not os.path.exists(log_path):
        os.mkdir(log_path)
#
# # 深交所基金公告
# def get_fundinfo_sz():
#     # 设置请求头，模拟浏览器行为
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
#         'Accept-Language': 'zh-CN,zh;q=0.9'
#     }
#     # 公告pdf路径
#     base_url_pdf = "http://www.szse.cn/disclosure/listed/bulletinDetail/index.html?"
#
#     # 返回参数，scrawler_count:总爬取数目;warning_count:异常数目;fund_info:异常信息
#     fund_info = ""
#     scrawler_count = 0
#     warning_count = 0
#     i = 1
#     while (True):
#         random_str = str(random.random())
#         page_size = 30
#         requst_url = "http://www.szse.cn/api/disc/info/find/tannInfo?random=%s&type=2&pageSize=%s&pageNum=%s"%(random_str, page_size, str(i))
#         # 发送请求并获取返回数据
#         response = requests.get(requst_url, headers=headers)
#         #print response.text
#         announceCount = response.json()["announceCount"]
#         # 分页
#         pages = announceCount / 30 + 1
#
#         # 数据
#         data = response.json()["data"]
#         for obj in data:
#             scrawler_count = scrawler_count + 1
#             id = obj["id"]
#             title = obj["title"]
#             print(title)
#             date_str = obj["publishTime"][:11]
#             if(date_str >= today_str):
#                 print(date_str)
#                 # 检查包含的关键字
#                 for key in key_array:
#                     if key in title:
#                         warning_count = warning_count + 1
#                         # 在线阅览路径
#                         pdf_url = base_url_pdf + id
#                         fund_info = fund_info + '%s <a href="%s">%s</a><br>%s<br><br>' % (date_str, pdf_url, title, pdf_url)
#                         # 下载公告附件，（附件路径）
#                         file_path = "http://disc.static.szse.cn/download" + obj["attachPath"]
#                         file_format = obj["attachFormat"]
#                         file_name = title + "." + file_format
#                         print(file_name)
#                         load_file(file_path, file_name)
#                         break
#         # 超过页数就退出
#         i = i + 1
#         if (i > pages):
#             break
#     fund_info = u"深交所总爬取数目：%d, 需要关注数目：%d。 (当总爬取数目为0时，请登陆官网检查！！)<br>%s<br><br>"%(scrawler_count, warning_count, fund_info)
#     return (scrawler_count, warning_count, fund_info)

# 上交所基金公告
def get_fundinfo_sh():
    # 设置请求头，模拟浏览器行为
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    base_url = "http://www.sse.com.cn"
    # fund_url = r"/disclosure/fund/announcement/"
    fund_url = r"/disclosure/listedinfo/regular/"
    # 发送请求并获取返回数据
    response = requests.get(base_url+fund_url, headers=headers)
    print(response)
    response.encoding = "utf-8"
    # 获取html网页源码
    # print response.text

    # 首先新建个BeautifulSoup对象，指定html解析器为python标准库自带的html.parser
    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)

    # 获取源码结构 <div class="sse_list_1"> 内容
    notices = soup.find_all("div", "sse_list_1 list ")
    print(notices)

    # 如果有内容即解析
    # 返回参数，scrawler_count:总爬取数目;warning_count:异常数目;fund_info:异常信息
    fund_info = ""
    scrawler_count = 0
    warning_count = 0
    if len(notices) > 0:
        dl_element = notices[0].dl
        dd_elements = dl_element.find_all("dd")
        for obj in dd_elements:
            scrawler_count = scrawler_count + 1
            date_str = obj.span.string.replace(" ", "")
            title = obj.a.get("title")
            print(title)
            if(date_str >= today_str):
                print(date_str)
                for key in key_array:
                    if key in obj.a.get("title"):
                        warning_count = warning_count + 1
                        # 在线阅览路径
                        pdf_url = base_url + obj.a.get("href")
                        fund_info = fund_info + '%s <a href="%s">%s</a><br>%s<br><br>' % (date_str, pdf_url, title, pdf_url)
                        # 下载公告附件
                        file_name = title + ".PDF"
                        load_file(pdf_url,file_name)
                        break
    fund_info = u"上交所总爬取数目：%d, 需要关注数目：%d。 (当总爬取数目为0时，请登陆官网检查！！)<br>%s" % (scrawler_count, warning_count, fund_info)
    return (scrawler_count, warning_count, fund_info)

# 下载文件
def load_file(url, file_name):
    #url = "http://disc.static.szse.cn/download/disc/disk01/finalpage/2018-10-29/a7ceaf7a-f42e-48b5-99c9-cfe5d6927c3c.PDF"
    file_path = attachment_path_today + file_name
    # 附件如果重名，在前面加个数字
    if os.path.exists(file_path):
        for i in range(2, 100):
            file_path = attachment_path_today + str(i) + file_name
            if not os.path.exists(file_path):
                break
    response = requests.get(url)
    with open(file_path, "wb") as f:
        f.write(response.content)
        print("load file end .....")

# 主函数
if __name__ == "__main__":
    # 初始化
    init()
    # # 调用深交所基金公告函数
    # scrawler_count_sz, warning_count_sz, fund_info_sz = get_fundinfo_sz()
    # 调用上交所基金公告函数
    scrawler_count_sh, warning_count_sh, fund_info_sh = get_fundinfo_sh()
