
import json
import pandas as pd

with open('./data/userInfo.json','r',encoding='utf-8') as f:
    data = json.load(f)

def parse_Details(itemId:str,data:json):
    
    # 路径 ["data"]["itemDO"]["itemLabelExtList"][2]["properties"]
    # 使用 dict.get() 方法来避免 KeyError
    itemDo = data.get('data', {}).get('itemDO', {})
    itemList = itemDo.get('itemLabelExtList', '未知')
    soldPrice = itemDo.get('soldPrice',{})
    
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
        df['报价'] = soldPrice
        df['商品ID'] = itemId
        return df

    else:
        print('保存失败',data) 

# 调用解析 函数
df = parse_Details('1234567890',data)

# 打印最终结果
print(df)

# 导出csv
df.to_csv('./data/itemDetail.csv')
# 导出html
df.to_html('./data/itemDetail.html')