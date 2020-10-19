import re

from hoshino import Service, MessageSegment
import hoshino
from .app.bili import BBangumi

sv = Service('bili_bangumi_broadcast',enable_on_default=False)
bot = hoshino.get_bot()

@bot.on_message()
async def main(ctx):
    msg = ctx['raw_message']
    m_id = str(ctx['message_id'])
    if msg == '今日新番':
        n = BBangumi()
        
        await bot.send(ctx,MessageSegment(type_='reply',data={'id':m_id}) + n.get_today())
    elif re.match('(星期([一二三四五六日天])|周([一二三四五六日]))?新番',msg):
        k = re.match('(星期([一二三四五六日天])|周([一二三四五六日]))?新番',msg)
        if k.group(2):
            if k.group(2) == '天':
                el = '日'
            else:
                el = k.group(2)
        elif k.group(3):
            el = k.group(3)
        n = BBangumi()
        await bot.send(ctx,MessageSegment(type_='reply',data={'id':m_id}) + n.get_date(el))
        

@sv.scheduled_job('cron',hour='0',minute='5')
async def daily_report():
    #grps = await sv.get_enable_groups()
    n = BBangumi()
    await sv.broadcast('又是美好的一天(*•̀ᴗ•́*)و\n今天的新番有\n' + n.get_today(),'bili_bangumi_broadcast',0)