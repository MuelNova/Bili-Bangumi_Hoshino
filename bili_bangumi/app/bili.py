import requests
from datetime import datetime

from nonebot import MessageSegment

week_c = ['','一','二','三','四','五','六','日']

class BBangumi(object):
    def __init__(self):
        self.data = self.get_data()
    
    def get_data(self):
        k = requests.get('https://bangumi.bilibili.com/web_api/timeline_global')
        n = k.json()
        if n.get('message') == 'success':
            return n.get('result')
        print('BiliBangumi: 获取番剧失败')
        return False
        
    def get_today(self):
        msg = ''
        if not self.data:
            self.data = self.get_data()
        for i in self.data:
            if i.get('is_today'):
                msg = '{} | 星期{}\n'.format(i.get('date'),week_c[int(i.get('day_of_week'))])
                for k in i['seasons']:
                    msg = msg + MessageSegment.image(k.get('cover'))
                    msg = msg + '{}\n    {} 更新 {} \n\n'.format(k.get('title'),k.get('pub_time'),k.get('pub_index'))
                return msg
     
    def get_date(self,s):
        msg = ''
        if not self.data:
            self.data = self.get_data()
        for i in self.data:
            if s == week_c[int(i.get('day_of_week'))]:
                msg = '{} | 星期{}\n'.format(i.get('date'),week_c[int(i.get('day_of_week'))])
                for k in i['seasons']:
                    msg = msg + MessageSegment.image(k.get('cover'))
                    msg = msg + '{}\n    {} 更新 {} \n\n'.format(k.get('title'),k.get('pub_time'),k.get('pub_index'))
        return msg
    
    def get_today_data(self):
        if not self.data:
            self.data = self.get_data()
        for i in self.data:
            if i.get('is_today'):
                return i.get('seasons')
    
