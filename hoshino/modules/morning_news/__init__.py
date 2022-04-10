import os.path
import hoshino
import requests,json
from hoshino import Service,R,priv, get_bot
from hoshino.util import DailyNumberLimiter
sv_help = '''
[晨报] 晨报
'''.strip()

sv = Service(
    name = '晨报',  #功能名
    use_priv = priv.NORMAL, #使用权限
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #可见性
    enable_on_default = False, #默认启用
    bundle = '娱乐', #分组归类
    help_ = sv_help #帮助说明
    )
absPath = './res/img/morning_news/'
group_path = '~\.hoshino\service_config\晨报.json'
# _day_limit = 3
# _lmt = DailyNumberLimiter(_day_limit)

def get_group_list():
    if os.path.exists(os.path.expanduser(group_path)):
        with open(os.path.expanduser(group_path) ,"r",encoding='utf-8') as dump_f:
            try:
                group_list = json.load(dump_f)['enable_group']
            except Exception as e:
                hoshino.logger.error(f'读取群号时发生错误{type(e)}')
                return None
    else:
        hoshino.logger.error(f'目录下缺少json文件')
    return group_list

def get_pic():
    url = 'https://v2.alapi.cn/api/zaobao'
    data = {'token':'mc5C57wOhC2SyUls', 'format':'json'}
    r = requests.post(url, data)
    all = r.json()
    if all['code'] != 200:
        code = '晨报错误' + str(all['code'])
        return code
    else:
        pic_url = r.json()['data']['image']
        pic = requests.get(pic_url)
        if os.path.isdir(absPath):
            try:
                with open(f'{absPath}img.png', "wb") as dump_f:
                    dump_f.write(pic.content)
            except:
                print('图片下载失败')
        else:print('路径错误')
def check_pic():
    size = os.path.getsize(f'{absPath}img.png')
    if size < 3000:
        return False
    return True

@sv.scheduled_job('cron', hour='9', minute='30', day_of_week='0-6')
async def send_news():
    if check_pic() == False:
        await bot.send_group_msg('图片大小异常，请检查')
    else:
        code = get_pic()
        if code:
            await bot.send_group_msg(code)
        else:
            bot = get_bot()
            group_list = get_group_list()
            msg = f'读晨报啦~'
            pic = R.img(f'morning_news/img.png').cqcode
            msg += f'{pic}'
            for gid in group_list:
                await bot.send_group_msg(group_id=int(gid), message=msg)

@sv.on_fullmatch("手动晨报")
async def hand_send_news(bot,ev):
    if check_pic() == False:
        await bot.send_group_msg('图片大小异常，请检查')
    else:
        code = get_pic()
        if code:
            await bot.send_group_msg(code)
        else:
            group_list = get_group_list()
            msg = f'读晨报啦~'
            pic = R.img(f'morning_news/img.png').cqcode
            msg += f'{pic}'
            for gid in group_list:
                await bot.send_group_msg(group_id=int(gid), message=msg)