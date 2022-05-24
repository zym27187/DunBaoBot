from hoshino import HoshinoBot, Service
from .models import UserInfo
from .download import download_url, download_avatar
import os
from .utils import to_image
from .utils import fit_size
from hoshino.typing import MessageSegment
from PIL import Image
from PIL import ImageChops
from base64 import b64encode
import base64
from io import BytesIO
import asyncio
sv = Service("waifu_monitor")
resPath = './hoshino/modules/waifu_monitor/groupid/'
_current_dir = os.path.join(os.path.dirname(__file__), 'config.yml')

async def download_image(user, convert: bool = True):
    img = None
    img = await download_avatar(user)
    if img:
        img = to_image(img, convert)
    return img

def bytesio2b64(im) -> str:
    im = im.getvalue()
    return f"base64://{b64encode(im).decode()}"

@sv.on_fullmatch("老婆测试")
async def get_user_info(bot: HoshinoBot, user: UserInfo):
    #glist_info = await bot.get_group_list()
    #for each_g in glist_info:
    #    group_id = each_g['group_id']
    #    print(group_id)                以上获取所有群号
    #group_id = user['group_id']
    group_id = 234191077
    group_info = await bot.get_group_member_list(group_id = group_id, no_cache = True)
    for each_mem in group_info:
        uid = int(each_mem['user_id'])
        res = await download_image(uid)
        res.save(f'{resPath}{group_id}/{uid}.png')

@sv.on_fullmatch("老婆检查")
async def check_waifu(bot,ev):
    group_id = 234191077
    uid = 120888797
    old_ava = Image.open(f'{resPath}{group_id}/{uid}.png').convert('RGB')
    new_ava = await download_image(uid)
    new_ava = new_ava.convert('RGB')
    #new_ava.save(f'{resPath}{group_id}/{uid}+.png')
    #new_ava = Image.open(f'{resPath}{group_id}/{uid}+.png').convert('RGB')
    diff = ImageChops.difference(old_ava, new_ava)
    if diff.getbbox() is None:
        msg = '通过了老婆检查'
        print(msg)
        #await bot.send_group_msg(group_id=int(234191077), message=msg)
    else:
        buffer_1 = BytesIO()
        buffer_2 = BytesIO()
        new = await download_image(uid,convert=False)
        new = fit_size(new,(100,100))
        old = Image.open(f'{resPath}{group_id}/{uid}.png').convert('RGB')
        old = fit_size(old,(100,100))
        old = old.convert('RGB')
        new = new.convert('RGB')
        old.save(buffer_1, format='JPEG')
        old_ava = buffer_1.getvalue()
        new.save(buffer_2, format='JPEG')
        new_ava = buffer_2.getvalue()
        old_ava = base64.b64encode(old_ava).decode()
        new_ava = base64.b64encode(new_ava).decode()
        old_str = f"base64://{old_ava}"
        new_str = f"base64://{new_ava}"
        msg_1 = MessageSegment.image(old_str)
        msg_2 = MessageSegment.image(new_str)
        await bot.send(ev, str(f'{msg_1}' + f'{msg_2}'))
        #await bot.send_group_msg(group_id=int(234191077), message=msg)
        #print(msg)
        #await bot.send_group_msg(group_id=int(234191077), message=msg)
    # try:
    #     diff = ImageChops.difference(old_ava, new_ava)
    #     if diff.getbbox() is None:
    #         msg = '通过了老婆检查'
    #         print(msg)
    #         #await bot.send_group_msg(group_id=int(234191077), message=msg)
    #     else:
    #         msg = '这人换老婆啦'
    #         print(msg)
    #         #await bot.send_group_msg(group_id=int(234191077), message=msg)
    # except ValueError as e:
    #     text = ("表示图片大小和box对应的宽度不一致，参考API说明：Pastes another image into this image."
    #             "The box argument is either a 2-tuple giving the upper left corner, a 4-tuple defining the left, upper, "
    #             "right, and lower pixel coordinate, or None (same as (0, 0)). If a 4-tuple is given, the size of the pasted "
    #             "image must match the size of the region.使用2纬的box避免上述问题")
    #     print("【{0}】{1}".format(e, text))


