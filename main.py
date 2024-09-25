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

    def get_token(self, url='https://www.goofish.com/search?q=macbook'):
        
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

        for attempt in range(5):

            try:
                match = re.match(r'([a-f0-9]+)_\d+', _m_h5_tk)

                token = match.group(1)
                print(f"第{attempt+1}次匹配到的token: {token}")
                break

            except TypeError as e:
                print(f"第{attempt+1}次未找到匹配期望token: {e}")
                token = ''
            time.sleep(1)
            page.refresh()
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

    def get_data(self, page:int) -> json:

        data = {"pageNumber":page,"keyword":"macbook M1","fromFilter":False,"rowsPerPage":30,"sortValue":"","sortField":"","customDistance":"","gps":"","propValueStr":{},"customGps":""}
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

    def get_userInfo(self, itemId:str) -> json:
        
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

        try:
            data = response.json()
        except ValueError as e:
            print('JSON 解析失败，返回结果：', response.text)
            return ''

        # 使用 dict.get() 方法来避免 KeyError
        seller_data = data.get('data', {}).get('sellerDO', {})

        itemCount = seller_data.get('itemCount', '未知')
        city = seller_data.get('city', '未知')
        nick = seller_data.get('nick', '未知')

        if itemCount != '未知' or city != '未知' or nick != '未知':
            print('卖出件数：', itemCount, "卖家昵称:", nick, '城市：', city)
            return {'卖出件数': itemCount, '卖家昵称': nick, '城市': city}
        else:
            print('抓取失败，数据不完整')
            return response.text

    def get_itemDetails(self, itemId:str) -> json:

        url = f'https://www.goofish.com/item?id={itemId}'

        cookies = {
        '_m_h5_tk': '88e05480d6cc21133a9854b3f6c023f0_1725343615524',
        '_m_h5_tk_enc': 'c07401e74bc18be181c71eccdb1eee19',}

        # token,cookies = self.get_token(url) # 这里可以优化，重复请求token容易被风控

        timestamp = int(time.time()*1000)



        itemId = {"itemId":itemId}
        itemId = json.dumps(itemId).replace(' ', '')
        data = {
        'data': itemId,
}
        
        sign = self.encrypt(self.token, timestamp, itemId) # 21f87a4d7daf3607d9f217af9d729d95
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
            cookies=self.cookies,
            headers=self.headers,
            data=data,
        )

        try:
            data = response.json()
            print('数据已返回')
            return data
        except ValueError as e:
            print('JSON 解析失败，返回结果：', response.text)
            return ''

    def get_itemDetails_browser(self,itemId:str) -> dict:
        
        page = WebPage()
        url=f'https://www.goofish.com/item?id={itemId}'
        page.get(url)
        itemList = page.eles("xpath://div[@class='value--iaKzLDas']")
        item_description = ''
        for item in itemList:
            item_description += item.text + " "

        item_description = item_description.replace('\n', ' ')
        
        item_detail = {'itemId':itemId,'item_description':item_description}

        print(item_detail)
        return item_detail
    
    def parse_Details(self, itemId:str,data:json):
        
        # 路径 ["data"]["itemDO"]["itemLabelExtList"][2]["properties"]
        # 使用 dict.get() 方法来避免 KeyError
        itemDo = data.get('data', {}).get('itemDO', {})
        itemList = itemDo.get('itemLabelExtList', '未知')
        soldPrice = itemDo.get('soldPrice',{})

        if itemList != '未知':
            # print('商品报价：',soldPrice)
            # print('型号信息：',itemList)
  
            # 将列表转换为 DataFrame
            df = pd.DataFrame(itemList)
            df['报价'] = soldPrice
            df['商品ID'] = itemId
            return df

        else:
            print('保存失败',data) # 返回空的情况：itemId=624651727381
    def get_itemId(self, data:json) -> list:
        
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

    def save_to_excel(self, ItemIds:list):
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

    def scrape_userInfo(self, page_number=1):
        data = self.get_data(page_number)
        itemIds = self.get_itemId(data)
        for item in itemIds:
            userInfo = self.get_userInfo(item)
            filename = f'userinfo{item}.json'
            self.save_data(userInfo, filename)

    def scrape_itemDetails(self, page_number=1):
        data = self.get_data(page_number)
        itemIds = self.get_itemId(data)
        
        # 用于存储所有 DataFrame 的列表
        df_list = []

        for item in itemIds:
            data = self.get_itemDetails(item)
            df = self.parse_Details(item, data)
            df_list.append(df)
            print(f'{item}已保存')
        # 拼接所有 DataFrame
        if df_list:
            concatenated_df = pd.concat(df_list, ignore_index=True)
            print(concatenated_df)
            concatenated_df.to_csv('./data/output.csv',encoding='utf-8')
        else:
            print("没有数据可拼接。")



@app.get("/fetch_data/")
def fetch_data(page_number: int):
    xianyu = Xianyu()
    try:
        return xianyu.get_data(page_number)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/fetch_userInfo/')
def fetch_userInfo(ItemId:str):
    xianyu = Xianyu()
    try:
        return xianyu.get_userInfo(ItemId)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/itemDetail_browser/')
def itemDetail_browser(ItemId:str):
    xianyu = Xianyu()
    try:
        return xianyu.get_itemDetails_browser(ItemId)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    # import uvicorn
    # uvicorn.run(app, host="0.0.0.0", port=8000)   
    xianyu = Xianyu()
    xianyu.scrape_itemDetails(2)