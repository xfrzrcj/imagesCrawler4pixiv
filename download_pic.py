# -*- coding:utf-8 -*-
import urllib.request
import re
import os
from urllib.error import HTTPError
from time import *


# 图片保存根目录
pics_path = r'./pics'
# 输入id文件
id_file = r'./ids.txt'
# 日志文件
logger = r'./piclog.txt'
log = open(logger, 'w')


# ------------定义3个函数，用来创建每个girl的目录、保存图片、写入文本描述及对话----------------
def mkdir_for_girl(f_path):
    """
    创建以标题命令的目录
    :param f_path: 文件根路径
    :return: 返回创建的目录路径
    """
    if not os.path.exists(f_path):
        os.mkdir(f_path)
    return f_path


def save_pictures(path, url_list, opener):
    """
    保存图片到本地指定文件夹
    :param path: 保存图片的文件夹，由mkdir_for_girl返回
    :param url_list: 待保存图片的url列表
    :param opener: urllib传递的输入句柄
    :return: none
    """
    for (index, url) in enumerate(url_list):
        print(u'%s 正在保存第%d张图片' % (ctime(), index))
        log.write(u'%s 正在保存第%d张图片' % (ctime(), index))
        log.write("\n")
        log.flush()
        words = url.split("/")
        pic_name = words[len(words)-1].replace("_master1200", "")
        file_name = os.path.join(path, pic_name)
        # 如果存在该图片则不保存
        if os.path.exists(file_name):
            print(u'%s 该图片已经存在' % ctime())
            log.write(u'%s 该图片已经存在' % ctime())
            log.write("\n")
            log.flush()
            continue
        req = urllib.request.Request(url)
        data = opener.open(req, timeout=30).read()
        f = open(file_name, 'wb')
        f.write(data)
        f.close()


def write_text(path, info):
    """
    在path目录中创建txt文件，将info信息（girl的文本描述和对话）写入txt文件中
    :param path: 保存txt文件的目录，由mkdir_for_girl返回
    :param info: 要写入txt的文本内容
    :return: none
    """
    # 创建/打开info.txt文件，并写入内容
    filename = os.path.join(path, 'info.txt')

    with open(filename, 'a+') as fp:
        fp.write(info.encode('utf-8'))
        fp.write('\n'.encode('utf-8'))
        fp.write('\n'.encode('utf-8'))


class PixivUrl:
    host = "www.pixiv.net"
    path = "member_illust.php"
    mode = "manga"
    illust_id = ""

    def __init__(self, host=None, path=None, mode=None, illust_id=None):
        if host is not None:
            self.host = host
        if path is not None:
            self.path = path
        if mode is not None:
            self.mode = mode
        if illust_id is not None:
            self.illust_id = illust_id

    def get_url(self):
        return "http://"+self.host+"/"+self.path+"?mode="+self.mode+"&illust_id="+self.illust_id


def download(url_id):
    url_host = "www.pixiv.net"
    url_path = "member_illust.php"
    url_mode = "manga"
    pix = PixivUrl(illust_id=url_id)
    opener = urllib.request.build_opener()  # 通过handler来构建opener
    user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ' \
                     r'(KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    opener.addheaders.append(("User-Agent", user_agent))
    req = urllib.request.Request(pix.get_url())
    try:
        response = opener.open(req, timeout=30)
        xml = response.read()
        xml = str(xml, "utf8")
        url_list = re.findall("https://i.pximg.net/img-master/img.*?.jpg", xml)
    except HTTPError as e:
        if 400 == e.code:
            pix.mode = "medium"
            req = urllib.request.Request(pix.get_url())
            response = opener.open(req, timeout=30)
            xml = response.read()
            xml = str(xml, "utf8")
            url_list = re.findall("https://i.pximg.net/c/600x600/img-master/img.*?_master1200.jpg", xml)
            words = url_list[0].split("/")
            del words[4]
            del words[3]
            new_url = "/".join(words)
            url_list = [new_url]
    opener.addheaders.append(("Accept", "image/webp,image/apng,image/*,*/*;q=0.8"))
    opener.addheaders.append(("Accept-Encoding", "gzip, deflate, br"))
    opener.addheaders.append(("Referer", pix.get_url()))
    opener.addheaders.append(("Accept-Language", "zh-CN,zh;q=0.8"))
    opener.addheaders.append(("Host", "i.pximg.net"))
    opener.addheaders.append(("Connection", "keep-alive"))
    save_pictures(mkdir_for_girl(pics_path), url_list, opener)


def download_by_read_ids():
    file = open(id_file)
    line = file.readline().replace("\n", "")
    print('开始下载')
    log.write('开始下载')
    log.write('\n')
    log.flush()
    while line is not '':
        try:
            print('开始任务：'+line)
            log.write('文件保存位置:' + pics_path+'/'+line)
            log.write('\n')
            log.flush()
            download(line)
        except Exception as e:
            print("异常："+str(e))
            log.write(str(e))
            log.write('\n')
        line = file.readline().replace("\n", "")
    log.write('结束下载')
    print('结束下载')
    log.flush()
    log.close()
    file.close()


download_by_read_ids()
