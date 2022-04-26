from hoshino import Service, priv
from hoshino.typing import CQEvent

sv = Service('_help_', manage_priv=priv.SUPERUSER, visible=False)

TOP_MANUAL = '''
====================
= DunBaoBot使用说明 =
====================
发送[]内的关键词触发
==== 查看详细说明 ====
[头像表情包] # 头像表情包生成器
[表情包帮助] # .jpg图片
[通用rss帮助]
[bili功能]
[色图帮助]
[雀魂帮助]
[股票查询] 
====== 常用指令 ======
[来num张keyword色图] # 来num张keyword的涩图 (不指定数量与关键字发送一张随机涩图)
[查成分] # 查询b站账号关注vtb成分
[今天吃什么]
[小炖搜图]
[打分]
====== 被动技能 ======
入群欢迎* & 退群通知
防撤回*
晨报*
*: 默认关闭
°: 不支持自定义
====== 模块开关 ======
※限群管理/群主控制※
[lssv] 查看各模块开关状态
[启用+空格+service]
[禁用+空格+service]
=====================
※炖宝系列bot，魔改自HoshinoBot,
不定期优化迭代,含有部分隐藏功能
Hoshino开源Project：
github.com/Ice-Cirno/HoshinoBot
'''.strip()
# 魔改请保留 github.com/Ice-Cirno/HoshinoBot 项目地址

def gen_bundle_manual(bundle_name, service_list, gid):
    manual = [bundle_name]
    service_list = sorted(service_list, key=lambda s: s.name)
    for sv in service_list:
        if sv.visible:
            spit_line = '=' * max(0, 18 - len(sv.name))
            manual.append(f"|{'○' if sv.check_enabled(gid) else '×'}| {sv.name} {spit_line}")
            if sv.help:
                manual.append(sv.help)
    return '\n'.join(manual)


@sv.on_prefix('help!', '帮助!')
async def send_help(bot, ev: CQEvent):
    bundle_name = ev.message.extract_plain_text().strip()
    bundles = Service.get_bundles()
    if not bundle_name:
        await bot.send(ev, TOP_MANUAL)
    elif bundle_name in bundles:
        msg = gen_bundle_manual(bundle_name, bundles[bundle_name], ev.group_id)
        await bot.send(ev, msg)
    # else: ignore
