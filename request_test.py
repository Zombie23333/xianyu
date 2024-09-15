import requests
import hashlib
import json
import time


def encrypt(token, timestamp, data):
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
    

cookies = {
    '_m_h5_tk': '88e05480d6cc21133a9854b3f6c023f0_1725343615524',
    '_m_h5_tk_enc': 'c07401e74bc18be181c71eccdb1eee19',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/x-www-form-urlencoded',
    # 'cookie': 'cna=tnNdH6urfVQCAd5H01Ij8t+V; _samesite_flag_=true; cookie2=1c8531de57286dcb6c1c48dd37e1a1c1; t=ad66eaedfd9679a9cc81d3fe246f2255; _tb_token_=5d6053ebb36b; xlly_s=1; mtop_partitioned_detect=1; _m_h5_tk=88e05480d6cc21133a9854b3f6c023f0_1725343615524; _m_h5_tk_enc=c07401e74bc18be181c71eccdb1eee19; tfstk=fOzZ9-1GtNQZcz2orf3qTHvS7b0tlVX5urMjiSVm1ADM5F90Y82KCoZsCIrUnJnsIlMXuruTRlTjCO34i8gVFT_5P5FtJqX5FvgYXQumiZMDYGCvBq3cF9tBocQrk8t84lf4t6ljgKvgnfvntvhxnqDimpxnZv0mn-D0tXcraFYMomfUtvhmoxcRdmmy8jnGae-2J5Qn6ckuTgLDuPLSbYVILEXu8fW-E5DeoED9pMjbT56wyWgTP8l7CwYaUSV8mDz2KTkY8W4gmWpNnXE0C2DsrGAE5PFgqm4lHn2r7-ouSDRDr5Fi32l3rst-dyk_nPohNUoj-zioSksdCmgZa-4TQI80EWN7WDUVUpDYfb3ngrCk0xoc4VJxtH2TklJD0ccKTY1FTGm5KShJZTI9Dnn6pXk5s1xvDccKTY1FTnKxfghEF1fG.; isg=BAgI5n6R-v14LBZ59x81gZH-2XYasWy7edD0c8K5UgN2nagHasBwS4mbEXXtrSST',
    'origin': 'https://www.goofish.com',
    'priority': 'u=1, i',
    'referer': 'https://www.goofish.com/',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}


itemId = {"itemId":"709665954065"}
itemId = json.dumps(itemId).replace(' ', '')
data = {'data': itemId}

# 加密token
token = '88e05480d6cc21133a9854b3f6c023f0'
timestamp = 1725335081201
timestamp = int(time.time()*1000)
print("timestamp:",timestamp)

sign = encrypt(token, timestamp, itemId)
print(sign)


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
    'spm_pre': 'a21ybx.search.searchFeedList.15.587c3da62DaXfi',
    'log_id': '587c3da62DaXfi',
}

response = requests.post(
    'https://h5api.m.goofish.com/h5/mtop.taobao.idle.pc.detail/1.0/',
    params=params,
    cookies=cookies,
    headers=headers,
    data=data,
)

print(response.json()['data']['sellerDO'])