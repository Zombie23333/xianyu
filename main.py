import requests
import time
import json
from DrissionPage import WebPage
import re
import hashlib
import pandas as pd
import threading
from fastapi import FastAPI, HTTPException

app = FastAPI()

class Xianyu:
    def __init__(self):

        self.token,self.cookies = self.get_token()
        data = {"pageNumber":3,"keyword":"macbook","fromFilter":False,"rowsPerPage":30,"sortValue":"","sortField":"","customDistance":"","gps":"","propValueStr":{},"customGps":""}
        self.data = json.dumps(data).replace(' ', '')
        self.headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'cna=iSkaH/aP+SsCAXJUuECf2VoA; t=2369cb6e0db6cb3137e6de0ef28be349; mtop_partitioned_detect=1; _m_h5_tk=819112b0b38cb4631214ef507843276f_1724078232549; _m_h5_tk_enc=94d311b0a9eee80579f5e0cf3e2bbf0c; cookie2=1621a01914c8b335d0fb631ae3d9ca52; xlly_s=1; tfstk=fUBqTiTnj-eq8GfMzU9w4GTX7s9vLpUQ_OT6jGjMcEYmhxgGawbJl11Xlc5PSadXoEZvQCbGoNRTDFTM7NsGGuwQdiIvBdvaRJwCnsxh21lMSAqiEHhdfiuUdiIxqmugA_2I_eKOutYGSIvoqH8kmAvGSLckxUDDjxxiru-9rFvMohcoZntImFxmIbJXsBkyXIqe1_GnhlZH_ejDoisfEJOoMiLPuaXW0gJFmfHiIT-2gOgvOTWDG1jp9tsTQYpfY_vkAieqUpjDYZT5-JDyEgsl5BC8WvORzORGnIng-eAwu_XDacDG2d829174ujLcGaRpqQmap3_BriBcal3lmwT2n3A7KkSks_6v9tao3pfdcK1GWWGJ3GfDUgSEW34A9OCqSfRD238Q4uDXiZd-dZYUKfh9G4KyRoqm6fdVgAGVpolt6INv4eZ0q; isg=BLa22h2hzMJM4rj2a4eB6CwVB-y41_oRpaxdVSCdYhmgY1X9iGXCISpVez8PS_Ip',
    'origin': 'https://www.goofish.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.goofish.com/',
    'sec-ch-ua': '"Not)A;Brand";v="99", "Microsoft Edge";v="127", "Chromium";v="127"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
}

    def get_token(self):
        
        # 默认d模式创建对象
        page = WebPage()
        url='https://www.goofish.com/search?q=macbook'
        page.get(url)
        # 获取cookie
        cookies = page.cookies(as_dict=True)
        # 获取token
        _m_h5_tk = cookies.get('_m_h5_tk',0)
        if not _m_h5_tk:
            page.refresh()

        try:
            re.match(r'([a-f0-9]+)_\d+', _m_h5_tk)
        except TypeError as e:
            print(f"未找到匹配期望token: {e}")
            page.refresh()
        match = re.match(r'([a-f0-9]+)_\d+', _m_h5_tk)

        if match:
            token = match.group(1)
            print(f"匹配到的token: {token}")
        else:
            token = ''
            print("未找到匹配的token")
        
        return token,cookies

    def encrypt(self, token, timestamp, data):
        # 固定的字符串 h 和 token
        h = "12574478"

        
        # 构造待加密的字符串
        to_encrypt = f"{token}&{timestamp}&{h}&{data}"
        
        # 计算 MD5 哈希
        md5_hasher = hashlib.md5()
        md5_hasher.update(to_encrypt.encode('utf-8'))
        
        # 获取哈希值（十六进制表示）
        sign = md5_hasher.hexdigest()
        
        return sign

    def get_data(self,page:int) -> json:

        data = {"pageNumber":page,"keyword":"macbook","fromFilter":False,"rowsPerPage":30,"sortValue":"","sortField":"","customDistance":"","gps":"","propValueStr":{},"customGps":""}
        self.data = json.dumps(data).replace(' ', '')
        timestamp = int(time.time()*1000)

        sign = self.encrypt(self.token, timestamp, self.data)
        print(f"第{page}页sign: {sign}")

        
        params = {
            'jsv': '2.7.2',
            'appKey': '12574478',
            't': timestamp,
            'sign': sign,
            'v': '1.0',
            'type': 'originaljson',
            'accountSite': 'xianyu',
            'dataType': 'json',
            'timeout': '20000',
            'api': 'mtop.taobao.idlemtopsearch.pc.search',
            'sessionOption': 'AutoLoginOnly',
            'spm': 'a21ybx.search.0.0',
            'logid': '4c053da67N5RDX',
        }

        data = {
            'data': self.data,
        }

        res = requests.post(
            'https://h5api.m.goofish.com/h5/mtop.taobao.idlemtopsearch.pc.search/1.0/',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
            data=data,
        )

        
        data = res.json().get('data', {})
        if data:
            print(f'第{page}页数据抓取成功')
        else:
            print(f'第{page}页数据抓取失败：',res.text)

        return data    

    def save_data(self, data:json, file_name:str):
        with open(f'./data/{file_name}', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def get_userInfo(self,itemId:str):
        
        url = f'https://www.goofish.com/item?id={itemId}'

        cookies = {
    '_m_h5_tk': '88e05480d6cc21133a9854b3f6c023f0_1725343615524',
    '_m_h5_tk_enc': 'c07401e74bc18be181c71eccdb1eee19',
}

        token,cookies = self.get_token(url)

        timestamp = int(time.time()*1000)
        timestamp_test = 1725322011710


        itemId = {"itemId":itemId}
        itemId = json.dumps(itemId).replace(' ', '')
        data = {
        'data': itemId,
}
        
        sign = self.encrypt(token, timestamp, itemId) # 21f87a4d7daf3607d9f217af9d729d95
        print(f"sign: {sign}")


        params = {
            'jsv': '2.7.2',
            'appKey': '12574478',
            't': timestamp,
            'sign': sign,
            'v': '1.0',
            'type': 'originaljson',
            'accountSite': 'xianyu',
            'dataType': 'json',
            'timeout': '20000',
            'AntiCreep': 'true',
            'AntiFlool': 'true',
            'api': 'mtop.taobao.idle.pc.detail',
            'sessionOption': 'AutoLoginOnly',
            'spm_cnt': 'a21ybx.item.0.0',
            'spm_pre': 'a21ybx.search.searchFeedList.1.587c3da696Pi8q',
            'log_id': '587c3da696Pi8q',
        }

        response = requests.post(
            'https://h5api.m.goofish.com/h5/mtop.taobao.idle.pc.detail/1.0/',
            params=params,
            cookies=cookies,
            headers=self.headers,
            data=data,
        )

        if response.json():
            data = response.json()
            itemCount = data['data']['sellerDO']['itemCount']
            city = data["data"]["sellerDO"]["city"]
            nick = data["data"]["sellerDO"]["nick"]
            print('卖出件数：',itemCount,"卖家昵称:",nick,'城市：',city)
            seller_data = {'卖出件数':itemCount,'卖家昵称':nick,'城市':city}
            
        return seller_data

    def get_itemId(self,data:json):
        
        itemIds = []
        if data:
            


            # 获取列表长度
            length = len(data["resultList"])
            
            
            # 遍历列表
            for item in data["resultList"]:

                itemId = item["data"]["commonDO"]["redirectUrl"]
                match = re.search(r'fleamarket://item\?id=(\d+)', itemId)
                if match:
                    itemId = match.group(1)
                    print(f"匹配到的itemId: {itemId}")
                else:
                    itemId = ''
                    print("未找到匹配itemId")
                itemIds.append(itemId)
            
            print(itemIds)
        else:
            print('ItemId为空')
        return itemIds

    def save_to_excel(self,ItemIds:list):
        # 创建一个空的 DataFrame，用于存储所有请求的数据
        df = pd.DataFrame(columns=['卖出件数', '卖家昵称', '城市'])
        for itemId in ItemIds:
            seller_data = self.get_userInfo(itemId)
            # 创建一个 DataFrame 用于当前请求的数据
            temp_df = pd.DataFrame([seller_data])

            # 使用 pd.concat() 将新数据追加到 df
            df = pd.concat([df, temp_df], ignore_index=True)
        # 将 DataFrame 保存到 Excel 文件中
        df.to_excel('./data/seller_data.xlsx', index=False)

    def main(self, page_number):
        data = self.get_data(page_number)
        filename = f'test_{page_number}.json'
        self.save_data(data, filename)

@app.get("/fetch_data/")
def fetch_data(page_number: int):
    xianyu = Xianyu()
    try:
        return xianyu.get_data(page_number)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)