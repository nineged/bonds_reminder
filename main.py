from asyncio.windows_events import NULL
import json
import requests
import csv
import re
from lxml import etree
import time

def get_dat():
    # 请求头
    header={
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
                    'AppleWebKit/537.36 (KHTML, like Gecko) '
                    'Chrome/83.0.4103.97 Safari/537.36',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Referer': 'http://www.baidu.com/',
    'Accept':'text/html,application/xhtml+xml,application/xml;'
                        'q=0.9,image/webp,image/apng,*/*;'
                    'q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',  }
    # 集思录可转债上新url
    newUrl ="https://www.jisilu.cn/data/cbnew/pre_list/?___jsl=LST___t=1645434599859"
    response = requests.get(newUrl)
    data = response.content.decode("utf-8")
    dat = json.loads(data)

    lst_data = []
    for one in dat['rows']:
        lst_dat = []
        # 转债id
        dat_cell = one["cell"]
        id = dat_cell['bond_id']
        # 转债名称
        name = dat_cell['bond_nm']
        # 方案进展
        progress = dat_cell['progress_nm']
        # 中签率
        lucky = dat_cell['lucky_draw_rt']
        # 单账户中签
        if lucky == None:
            single = None
        else:
            single = float(lucky) * 10.0
        lst_dat.append(id)
        lst_dat.append(name)
        lst_dat.append(progress)
        lst_dat.append(lucky)
        lst_dat.append(single)
        lst_data.append(lst_dat)
    return lst_data

def wirte_csv(data):
    # 创建文件对象
    f = open('可转债.csv', 'w', encoding='utf-8', newline='')
    # 基于文件对象构建 csv写入对象
    csv_writer = csv.writer(f)
    # 构建列表头
    csv_writer.writerow(["代 码", "转债名称", "方案进展", "中签率"])
    # 写入csv文件内容
    for dat in data:
        csv_writer.writerow(dat)
    # 关闭文件
    f.close()

def retimelist(data):   #获取新债申购时间信息
    timelist = []
    for dat in data:
        if dat[2].find("申购") >= 0:
            spattern = re.compile(r'\d+-\d+-\d+申购')
            stime = spattern.findall(dat[2])
            timelist.append(stime)
    return timelist

def server_push(timelist): #server酱推送
    pushurl = "https://sctapi.ftqq.com/****************.send" # **************** 填写server酱的SendKey
    today = time.strftime("%Y-%m-%d",time.localtime())
    datas = {
        'title':"新债申购提醒",                                #推送消息内容(详见server酱)
        'desp':"""                                                      
        # 今日有新债申购

        ```python
        print("hello the world")
        ```



        """}
    for one in timelist:
        if one[0][:-2] == today:
            requests.post(pushurl,data=datas)
            
if __name__ == '__main__':
    data = get_dat()
    time_list = retimelist(data)
    server_push(time_list)
    wirte_csv(data)
