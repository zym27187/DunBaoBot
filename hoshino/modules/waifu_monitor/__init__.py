from hoshino import HoshinoBot, Service
from .models import UserInfo
from .download import download_url, download_avatar
import os
import yaml
import base64
from io import BytesIO
from PIL import Image
import asyncio
sv = Service("waifu_monitor")
absPath = './hoshino/modules/waifu_monitor/'
_current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')

@sv.on_fullmatch("老婆测试")
async def get_user_info(bot: HoshinoBot, user: UserInfo):
    #glist_info = await bot.get_group_list()
    #for each_g in glist_info:
    #    group_id = each_g['group_id']
    group_id = user['group_id']
    data = {'Info': {}}
    data['Info'].setdefault(group_id, [])
    group_info = await bot.get_group_member_list(group_id = group_id, no_cache = True)
    for each_mem in group_info:
        uid = int(each_mem['user_id'])
        res = download_avatar(uid)
        bytes_stream = BytesIO(res)
        ava = Image.open(bytes_stream)
        mem_data = {
            'member':{
                'user_id':uid,
                'user_ava':ava
            }
        }
        data['Info'][group_id].append(mem_data)
    with open(_current_dir,'w',encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True)

