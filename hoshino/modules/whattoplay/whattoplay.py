import requests,random,os,json
from hoshino import Service,R,priv
from hoshino.typing import CQEvent
from hoshino.util import DailyNumberLimiter
import hoshino

sv_help = '''
[今天玩什么] 看看今天玩啥
'''.strip()

sv = Service(
    name = '今天玩什么',  #功能名
    use_priv = priv.NORMAL, #使用权限
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #可见性
    enable_on_default = True, #默认启用
    bundle = '娱乐', #分组归类
    help_ = sv_help #帮助说明
    )

_day_limit = 3
_lmt = DailyNumberLimiter(_day_limit)
absPath = './hoshino/modules/whattoplay/'

def get_games():
    if os.path.exists(absPath + 'games.json'):
        with open(absPath + 'games.json',"r",encoding='utf-8') as dump_f:
            try:
                words = json.load(dump_f)
            except Exception as e:
                hoshino.logger.error(f'读取游戏列表时发生错误{type(e)}')
                return None
    else:
        hoshino.logger.error(f'目录下未找到游戏列表')
    keys = list(words.keys())
    key = random.choice(keys)
    return words[key]["name"]

@sv.on_rex(r'^(今天|早上|中午|晚上|夜宵|今晚)玩(什么|啥|点啥)')
async def net_ease_cloud_word(bot,ev:CQEvent):
    uid = ev.user_id
    if not _lmt.check(uid):
        return
    _lmt.increase(uid)
    game_name = get_games()
    to_eat = f'今天去玩{game_name}吧~没有的人都可以问小炖爸爸要哦☆'
    try:
        foodimg = ' '.join(map(str, [R.img(f'games/{game_name}.jpg').cqcode,]))
        to_eat += f'\n{foodimg}'
    except Exception as e:
        hoshino.logger.error(f'读取游戏图片时发生错误{type(e)}')
    await bot.send(ev, to_eat)
