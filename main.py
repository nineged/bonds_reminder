from asyncio.windows_events import NULL
import json
import requests
import re
import time

def get_dat():
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

    newUrl ="https://www.jisilu.cn/data/cbnew/pre_list/?___jsl=LST___t=1645434599859"
    response = requests.get(newUrl,headers=header)
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

def getNameTime(data):
    list = {}
    for dat in data:
        if dat[2].find("申购") >= 0:
            spattern = re.compile(r'\d+-\d+-\d+申购')
            stime = spattern.findall(dat[2])
            list[dat[1]] = stime      
    return list

def server_push(list):
    todayNamelist = []
    namestring = ""
    pushurl = "https://sctapi.ftqq.com/************.send"   #填server酱SendKey
    today = time.strftime("%Y-%m-%d",time.localtime())
    for name in list.keys():
        if list[name][0][:-2] == today:
            todayNamelist.append(name)
            namestring += name + "\n"

    count = len(todayNamelist)
    print(count)
    datas = {
            'title':"今日共有 "+ str(count) +" 支新债",
            'desp':namestring}        
    requests.post(pushurl,data=datas)
            
if __name__ == '__main__':
    data = get_dat()
    list = getNameTime(data)
    server_push(list)

