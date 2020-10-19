import re

from hoshino import Service, MessageSegment
import hoshino
from .app.bili import BBangumi

sv = Service('bili_bangumi_broadcast',enable_on_default=False)
bot = hoshino.get_bot()
cache = list()


@bot.on_message()
async def main(ctx):
    msg = ctx['raw_message']
    m_id = str(ctx['message_id'])
    if msg == '今日新番':
        n = BBangumi()
        
        await bot.send(ctx,MessageSegment(type_='reply',data={'id':m_id}) + n.get_today())
    elif re.match('(星期([一二三四五六日天])|周([一二三四五六日]))+?新番',msg):
        k = re.match('(星期([一二三四五六日天])|周([一二三四五六日]))+?新番',msg)
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
    
@sv.scheduled_job('cron',minute='*/5')
async def update_report():
    global cache
    #grps = await sv.get_enable_groups()
    n = BBangumi()
    new_data = n.get_today_data()
    if not cache or (len(cache) != len(new_data)):
        sv.logger.info('番剧缓存池已经更新')
        cache = new_data
    else:
        for i in range(len(new_data)):
            if new_data[i].get('is_published'):
                if not cache[i].get('is_published'):
                    cache = new_data
                    sv.logger.info('番剧缓存池已经更新')
                    k = new_data[i]
                    msg = MessageSegment.image(k.get('cover'))
                    msg = msg + '{}\n   更新了 {} \n\n{}'.format(k.get('title'),k.get('pub_index'),k.get('url'))
                    await sv.broadcast('有番剧更新啦(*•̀ᴗ•́*)و\n\n' + msg,'bili_bangumi_broadcast',0)