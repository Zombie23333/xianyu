import requests
import time
import json
from DrissionPage import WebPage
import re
import hashlib
import pandas as pd
import threading
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# 允许所有来源
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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

    def get_data(self, keyword:str, page:int, searchFilter:str='') -> json:
        # searchFilter="priceRange:2000,15000"

        data = {"pageNumber":page,"keyword":keyword,"fromFilter":False,"rowsPerPage":30,"sortValue":"","sortField":"","customDistance":"","gps":"","propValueStr":{},"customGps":"","searchFilter":searchFilter}
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
        itemTitle = itemDo.get('title',{})
        itemDesc = itemDo.get('desc',{})
        # 存放解析后的商品详情
        result = {}
        if itemList != '未知':
            # 将每个条目的 properties 中的 ##XX 作为键，text 的值作为值，构建一个字典
            for item in itemList:
                properties = item["properties"].split("##")
                for i in range(1, len(properties) - 1):
                    short_key = properties[i].split(':')[0]  # 只保留 ':' 前面的部分
                    result[short_key] = item["text"]


            # 将列表转换为 DataFrame
            df = pd.DataFrame([result])
            df['标题'] = itemTitle
            df['描述'] = itemDesc            
            df['报价'] = soldPrice
            df['商品ID'] = itemId
            return df

        else:
            print('保存失败',data) 
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

    def scrape_itemDetails(self, keyword:str, page_number:int=1, searchFilter:str='')-> pd.DataFrame:
        # 获取列表页商品详情
        data = self.get_data(keyword, page_number, searchFilter)
        # 获取itemIds,用以遍历详情页
        itemIds = self.get_itemId(data)
        
        # 用于存储所有 DataFrame 的列表
        df_list = []
        # 遍历详情页
        for item in itemIds:
            data = self.get_itemDetails(item)
            df = self.parse_Details(item, data)
            df_list.append(df)
            print(f'{item}已保存')
        # 拼接所有 DataFrame
        if df_list:
            # 拼接所有表格
            concatenated_df = pd.concat(df_list, ignore_index=True)
            print(concatenated_df)
            output_path_csv = f'./data/output_{int(time.time())}.csv'
            output_path_html = f'./docs/output_{int(time.time())}.html'
            concatenated_df.to_csv(output_path_csv,encoding='utf-8')
            concatenated_df.to_html(output_path_html)
            return concatenated_df
        else:
            print("没有数据可拼接。")

    def slider(self):


        headers = {
            "accept": "*/*",
            "accept-language": "zh-CN,zh;q=0.9",
            "bx-pp": "78613a38613235666561316666386634356631323034353962396530393430366438393a307c307c617c313732373537313739303430317c6d64357c7177656173647a7863677c317c317c317c686c73495374516b554c6b77764c74457c303a686c73495374516b554c6b77764c74453a303a6231366637323833343232353566633739303135386439643238363335346635636162646138623431343536373435383138326236336439346665663931386639306665643265663364303166363533626637626434306130666133366162663a30",
            "bx_et": "g2dx29q7A0mmNo4z_lMlI0OoTygkBCL2zn8QsGj0C3KJ0w3VjKY66LKB4ivMni49ehtPni1Xs7tJqescjFsG6hK9XiX6ncuT6gL6iOiZuN19m3sflF1623f2ZKVGmm595HftxDcntE8Va1inxlzeEs1dl-GGCtwWuNBK2vGntE84oZgHPX0ZGkKRxG11hOT7Ng7Nl1sb14I5Wwy_ch1sy4Q17rZbGG67PZ711Gt114LSI0FAXrsU6d8HRYDuDRNT6QQAHGFG25KHZWX5ARS7s5jAktLDlgF_1QpzuLvRcvzlbsj2uZKZTS5fBdOcNIiS169e2CBC9A0VOI86LdTzDVIXrnRdGBnYiaXODLOfePN6k_JfFdKxD-SXn3BFPTatTaxhVERXeVrWlHjAGa6oO2L5CLAVLIm7M69eosv6A02ccpQ14KOH9NmuxMQgH438QRWfzELfd-dAeLo5yM0y4RyNea7Rx43UQRWfJaInziyaQTsd.",
            "priority": "u=1, i",
            "referer": "https://h5api.m.goofish.com//h5/mtop.taobao.idle.pc.detail/1.0/_____tmd_____/punish?x5secdata=xd242dda7222b1e064750384bfefbd4f0852fd856b024a7c981727571790a-717315356a-2091428694abaac3en2218612320222a__bx__h5api.m.goofish.com%3A443%2Fh5%2Fmtop.taobao.idle.pc.detail%2F1.0&x5step=2&action=captcha&pureCaptcha=",
            "sec-ch-ua": "\"Google Chrome\";v=\"129\", \"Not=A?Brand\";v=\"8\", \"Chromium\";v=\"129\"",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "\"Windows\"",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
        }
        cookies = {
            "cna": "tnNdH6urfVQCAd5H01Ij8t+V",
            "t": "ad66eaedfd9679a9cc81d3fe246f2255",
            "cookie2": "1a24b62ad1693a5cf82b621940ba933f",
            "_samesite_flag_": "true",
            "_tb_token_": "53867360ee317",
            "sgcookie": "E100Hd1Op8SvgQRQMrPY1C0QhyDzHJhBepUKTcDgiimLJw38T9vDSLudpv%2BHGjIGNbM8xB7KiPtaKsQrQQNk2S%2FM79mX4A78WVi2YPYxXeIeVbI%3D",
            "csg": "7559ab73",
            "havana_lgc2_77": "eyJoaWQiOjIyMTg2MTIzMjAyMjIsInNnIjoiODRhY2NiZjAxY2ZjZjVlY2MzZmRkYTVmMzFlNDlhNWYiLCJzaXRlIjo3NywidG9rZW4iOiIxdVRWVGVDbUtyVDM2dUpaV0tqWFdkZyJ9",
            "_hvn_lgc_": "77",
            "havana_lgc_exp": "1729069497311",
            "xlly_s": "1",
            "mtop_partitioned_detect": "1",
            "_m_h5_tk": "a136015518740092cfc6f2dea057104d_1727579256533",
            "_m_h5_tk_enc": "157a20bdc31e8ccf80a5157463553034",
            "sdkSilent": "1727657383824",
            "x5sectag": "517773",
            "tfstk": "gCAS27cx6uqWx0wyBX3VCud0x41CNHGZ9y_pSeFzJ_C8RSKeJUWpzeEBAnKwz7ReJMtB0ijJYaCJOwKvJ9FEE_WCOnI2zB-ErKTpviReUMkoO2sAR9Idwb4knh8TaQklTW1lt6nZbflZrUfh9XDg-1yukN8AJaQK_tFrHqoZbflZerCIVcJU_IpQhwjAywCdyqsA8iF8vHIRHoQ1S6IpvHIADa7g2WBL9rLAmwCdvHCKBiMfkYs2Pq4o77lna8T5cWFpGZnhXUGztZdRPTs9yQNL99b5FGLRccROStBv-9O3-W6eydxhW3E-AMAXkQp9XmyP2d_B7ptt88bVdQffvQhg5idWRI6k3ueR5_s5BQB77VY1pKOfaQn3IE8f2O123xmPL_tWIGX-nmxBlg-pNtES0MJwuQBXXmPXx99pasd-Dfszu5S6H9wQlOVdlGujlJ2HHHMTq8xI2hBRoZ4ZlqwaKTQcli3jlJqfeZbm8qgbIr1..",
            "isg": "BBERRi7pE9g4zH_i5uBMetA5IB2rfoXwa6yAyfOnqlj3mjTsO87AwGc8PG58kh0o"
        }
        url = "https://h5api.m.goofish.com/h5/mtop.taobao.idle.pc.detail/1.0/_____tmd_____/slide"
        params = {
            "slidedata": "{\"a\":\"X82Y__b7e7d6288d2b2a8ca084a56ab2ecce75\",\"t\":\"750384bfefbd4f0852fd856b024a7c98\",\"n\":\"228\\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\",\"p\":\"{\\\"ncbtn\\\":\\\"61.9921875|197.3046875|41.666664123535156|29.661457061767578|197.3046875|226.96614456176758|61.9921875|103.65885162353516\\\",\\\"umidToken\\\":\\\"T2gAHqaszXZ-YaduU_eOSa9gMlUIRp6RzHr_m5C_JpJFsGJcaxq6kPH7Me4jA5_PmQc=\\\",\\\"ncSessionID\\\":\\\"895d44345ab\\\",\\\"et\\\":\\\"1\\\"}\",\"scene\":\"register\",\"asyn\":0,\"lang\":\"cn\",\"v\":1}",
            "x5secdata": "xd242dda7222b1e064750384bfefbd4f0852fd856b024a7c981727571790a-717315356a-2091428694abaac3en2218612320222a__bx__h5api.m.goofish.com:443/h5/mtop.taobao.idle.pc.detail/1.0",
            "ppt": "0",
            "landscape": "1",
            "ts": "1727571822153",
            "v": "008126185580596368"
        }
        response = requests.get(url, headers=headers, cookies=cookies, params=params)

        print(response.text)
        print(response)


@app.get("/fetch_data/")
def fetch_data(keyword:str, page_number: int):
    xianyu = Xianyu()
    try:
        return xianyu.get_data(keyword, page_number)
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
    import uvicorn
    uvicorn.run(app, port=8000)   
    # xianyu = Xianyu()
    # for i in range(1,2):

    #     xianyu.scrape_itemDetails('Steam Deck OLED',i,searchFilter="priceRange:2500,20000;")

