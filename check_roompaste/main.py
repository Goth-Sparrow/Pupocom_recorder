# -*- coding: utf-8 -*-
############################################################
# Author: Goth Sparrow                                     #
# WeChat： Sugar_orange_Yummy                              #
# QQ: 198266237                                            #
# email: liuqingffffff@gmail.com                           #
# If you have any suggestions ,Welcome to contact with me  #
############################################################

"""软件分为两个部分。玩家行为：进入游戏，点一起玩，复制房间号，输入while true 不再复制，进入房间

1.不断检测剪贴板最后一个数据并记录，上传云端，比对。
2.不断爬取组队页面房间号，房主信息，并对应时间，储存在云端。

"""

import pyperclip
import re 
from datetime import datetime
import time
#剪贴板检测
def check_room():
    pattern =  r'^[A-Z0-9]{6}$'
    #定义一个样式，6位数字大写字母组合
    room = pyperclip.paste().strip()
    #定义一个变量储存剪贴板并去除空格
    if re.match(pattern,room):
        print(f"捕获到房间号：{room}")
        return room
    #匹配是否为房间号，若是返回房间号
    else:
        print(f"未捕获房间号：{room}，或房间号不满足大写字母与数字组合")
        return None
    #不是就返回空

#数据存储函数
def save_room(room_checked):
    t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #调用datetime方法获取当前时间
    with open("roomdata.txt","a",encoding="utf-8") as file:
        file.write(f"{t}：你进入了房间，房间号为{room_checked}\n")
    #写入roomdata.txt文件，追加模式，utf-8编码

#入口函数
if __name__ =="__main__":
    while True:
        room_number = check_room()
    #存储房间号检测结果
        if room_number:
            #检测到有房间号返回
            save_room(room_number)
            #调用save_room函数记录数据
        time.sleep(3)