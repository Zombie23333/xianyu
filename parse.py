
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

    if itemList != '未知':
        # print('商品报价：',soldPrice)
        # print('型号信息：',itemList)

        # 将列表转换为 DataFrame
        df = pd.DataFrame(itemList)
        df['报价'] = soldPrice
        df['商品ID'] = itemId
        return df

    else:
        print('保存失败',data) 


df = parse_Details('1234567890',data)

# 合并相同 itemId 的行
result_df = df.groupby('商品ID').agg(lambda x: x.iloc[0] if len(x.unique()) == 1 else ' '.join(x)).reset_index()

# 移除重复的 itemId 列
result_df.drop_duplicates(subset='商品ID', keep='first', inplace=True)


# 打印最终结果
print(result_df)

# 导出
result_df.to_csv('./data/itemDetail.csv')