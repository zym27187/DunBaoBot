import time
from nonebot import MessageSegment
import pytz
from datetime import datetime
import hoshino
from hoshino import Service, get_bot
from hoshino import R
import json
import os
import glob
import random

sv = Service('lunchcall', enable_on_default=False, help_='时报')
tz = pytz.timezone('Asia/Shanghai')
absPath = '~\.hoshino\service_config\lunchcall.json'
group_list = []

def get_group_list():
    if os.path.exists(os.path.expanduser(absPath)):
        with open(os.path.expanduser(absPath) ,"r",encoding='utf-8') as dump_f:
            try:
                group_list = json.load(dump_f)['enable_group']
            except Exception as e:
                hoshino.logger.error(f'读取群号时发生错误{type(e)}')
                return None
    else:
        hoshino.logger.error(f'目录下缺少json文件')
    return group_list


@sv.scheduled_job('cron', hour='*', day_of_week='0-4')
async def lunch_call():
    bot = get_bot()
    now = datetime.now(tz)
    group_list = get_group_list()
    if now.hour == 11:
        path = os.path.join(hoshino.config.RES_DIR, 'img/lunchcall')
        length = len(glob.glob(pathname=f'{path}/*.jpg'))
        number = random.randint(1, length)
        msg = f'[CQ:at,qq=522034848]'+'11点了傻卵该恰饭了'
        lunch_img = R.img(f'lunchcall/lunchtime{number}.jpg').cqcode
        msg += f'{lunch_img}'
        for gid in group_list:
            await bot.send_group_msg(group_id=int(gid), message=msg)

#@sv.scheduled_job('cron', hour='14', minute='*/5', day_of_week='0-4')
#async def fundation_call():
#    now_time = time.strftime('%H:%M')
#    bot = get_bot()
#    msg = '基金关闭提醒'
#    if now_time == '14:45':
#        await bot.send_private_msg(user_id=451534947, message=msg)
#    elif now_time == '14:40':
#        await bot.send_private_msg(user_id=120888797, message=msg)