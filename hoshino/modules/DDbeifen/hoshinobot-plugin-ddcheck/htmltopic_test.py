import os.path
import requests
import httpx
import htmlrender
from PIL import Image
from io import BytesIO
import base64
import asyncio
absPath = './res/img/morning_news/'
htmlPath = 'C:/Hoshino/HoshinoBot/hoshino/modules/hoshinobot-plugin-ddcheck'#'./hoshino/modules/hoshinobot-plugin-ddcheck'

def get_meadls(uid):
    try:
        url = "https://api.live.bilibili.com/xlive/web-ucenter/user/MedalWall"
        params = {"target_id": uid}
        headers = {"cookie":''}
        r = httpx.get(url,params=params,headers=headers)
        all = r.json()
        print(all)
        return all["data"]["list"]
    except (KeyError, IndexError) as e:
        return []

def get_user_info(uid: int) -> dict:
    try:
        url = "https://account.bilibili.com/api/member/getCardByMid"
        params = {"mid": uid}
        r = httpx.get(url, params=params)
        result = r.json()
        print(result)
        return result["card"]
    except (KeyError, IndexError) as e:
        return {}

async def others1():
    with open(f'{htmlPath}/html.txt','r',encoding='utf8') as ht:
        content = ht.read()
        result = htmlrender.html_to_pic(html=content)
        print(type(result))
        img = Image.open(BytesIO(result))
        img_base64 = base64.b64encode(img).decode('utf8')

async def others2():
    print('others2')
async def main():
    r1 = await others1()
    r2 = await others2()
if __name__ == '__main__':
    r=main(); asyncio.run(r)