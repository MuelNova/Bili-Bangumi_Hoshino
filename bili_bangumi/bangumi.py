import re

from hoshino import Service, MessageSegment
import hoshino
from .app.bili import BBangumi
from .app.util import SQL

sv = Service('bili_bangumi_broadcast',enable_on_default=False)
bot = hoshino.get_bot()
cache = list()
sub_user = list()
unsub_user = list()
st = set()

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
        
@sv.on_message()
async def sub(bot,ctx):
    msg = ctx['raw_message']
    m_id = str(ctx['message_id'])
    global st,sub_user,unsub_user
    if re.match('查[看询]*番剧订阅',msg):
        o = SQL('Subscription')
        bgms = list()
        for k in o.iterkeys():
            if ctx['group_id'] in o.get(k):
                bgms.append(k)
        o = SQL('All_Sub')
        await bot.send(ctx,'群{}番剧订阅列表:\n⛩⛩全部推送:{}\n⛩'.format(str(ctx['group_id']),ctx['group_id'] in o.get('data')) + '\n⛩'.join(i for i in bgms))
        
    elif msg == '番剧订阅 all':
        o = SQL('All_Sub')
        gid = ctx['group_id']
        grps = set() if not o.get('data') else o.get('data')
        grps.add(gid)
        o['data'] = grps
        await bot.send(ctx,'已经为群{}添加全部订阅'.format(str(gid)))
    elif msg == '番剧订阅 !all':
        o = SQL('All_Sub')
        gid = ctx['group_id']
        grps = set() if not o.get('data') else o.get('data')
        grps.discard(gid)
        o['data'] = grps
        await bot.send(ctx,'已经为群{}取消全部订阅'.format(str(gid)))
        
    elif re.match('番剧(取消)*订阅',msg):
        m = BBangumi()
        n = m.get_data()
        st = set()
        for i in n:
            for b in i.get('seasons'):
                st.add(b.get('title'))
        if re.match('番剧(取消)*订阅',msg).group(1):
            unsub_user.append({'id':ctx['user_id'],'gid':ctx['group_id']})
        else:
            sub_user.append({'id':ctx['user_id'],'gid':ctx['group_id']})
        st = list(st)
        await bot.send(ctx,'番剧列表:\n⛩' + '\n⛩'.join('{}.{}⛩'.format(i+1,st[i]) for i in range(len(st))))
        
        
    elif {'id':ctx['user_id'],'gid':ctx['group_id']} in sub_user:
        sub_user.remove({'id':ctx['user_id'],'gid':ctx['group_id']})
        if msg.isdigit() and (int(msg)-1 <= len(st) and int(msg)-1 >= 0):
            o = SQL('Subscription')
            bgm = st[int(msg)-1]
            grp = set() if not o.get(bgm) else o.get(bgm)
            grp.add(ctx['group_id'])
            o[bgm]=grp
            await bot.send(ctx,'已为群{}添加番剧订阅：\n⛩{}⛩'.format(str(ctx['group_id']),bgm))
        else:
            await bot.send(ctx,'你发的是什么鸡掰啦バカー')
    elif {'id':ctx['user_id'],'gid':ctx['group_id']} in unsub_user:
        unsub_user.remove({'id':ctx['user_id'],'gid':ctx['group_id']})
        if msg.isdigit() and (int(msg)-1 <= len(st) and int(msg)-1 >= 0):
            o = SQL('Subscription')
            bgm = st[int(msg)-1]
            grp = set() if not o.get(bgm) else o.get(bgm)
            grp.discard(ctx['group_id'])
            o[bgm]=grp
            await bot.send(ctx,'已为群{}取消番剧订阅：\n⛩{}⛩'.format(str(ctx['group_id']),bgm))
        else:
            await bot.send(ctx,'你发的是什么鸡掰啦バカー')
        
        
'''
@sv.on_command('番剧更新测试')
async def test_d(se):
    n=BBangumi()
    new_data = n.get_today_data()
    k = new_data[0]
    print(k)
    sv.logger.info('检测到番剧更新:{}'.format(k.get('title')))
    msg = MessageSegment.image(k.get('cover'))
    msg = msg + '⛩{}⛩\n   更新了 {} \n\n{}'.format(k.get('title'),k.get('pub_index'),k.get('url'))
    o = SQL('Subscription')
    grps = set() if not o.get(k.get('title')) else o.get(k.get('title'))
    o = SQL('All_Sub')
    grps2 = set() if not o.get('data') else o.get('data')
    grps = list(grps | grps2)
    for i in grps:
        await bot.send_group_msg(group_id=i,message='有番剧更新啦(*•̀ᴗ•́*)و\n\n' + msg)
'''

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
                    k = new_data[i]
                    sv.logger.info('检测到番剧更新:{}'.format(k.get('title')))
                    msg = MessageSegment.image(k.get('cover'))
                    msg = msg + '⛩{}⛩\n   更新了 {} \n\n{}'.format(k.get('title'),k.get('pub_index'),k.get('url'))
                    o = SQL('Subscription')
                    grps = set() if not o.get(k.get('title')) else o.get(k.get('title'))
                    o = SQL('All_Sub')
                    grps2 = set() if not o.get('data') else o.get('data')
                    grps = list(grps | grps2)
                    for i in grps:
                        await bot.send_group_msg(group_id=i,message='有番剧更新啦(*•̀ᴗ•́*)و\n\n' + msg)