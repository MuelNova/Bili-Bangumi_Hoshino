# Bili-Bangumi_Hoshino
A plugin for Hoshinobot to seek bangumi on Bilibili

# Installation
 - 将`bili_bangumi`放入`.hoshino/modules/`文件夹中
 - 在`.hoshino/config/__bot__.py`文件的`modules`条目下加入`'bili_bangumi',`
 - 重启`Hoshino`
 
# Features
 - 推送新番更新 (需要开启服务`bili_bangumi_broadcast`(默认不开启))
 - 每日推送当日新番(需要开启服务`bili_bangumi_broadcast`)

# Usage
 - `周几/星期几新番`查询该日番剧时间表
 - `今日新番`查询当天的番剧时间表
 - `番剧(取消)订阅`对番剧进行订阅/取消订阅
 - `查询番剧订阅`查询本群订阅的番剧
 - `番剧订阅 all/!all`对所有番剧订阅/取消订阅
