import requests
import json


def slider():
    


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

if __name__ == '__main__':
    slider()