#!/usr/bin/python
# coding=utf-8

import time
import sqlite3
import telepot
from pprint import pprint
from datetime import date, datetime

import noti


class SportFinderBot:
    def __init__(self):
        self.bot = telepot.Bot(noti.TOKEN)
        self.bookmark = []
        self.running = False

    def StadiumData(self, user, loc_param='시흥시'):
        res_list = noti.getData(loc_param)
        find = False
        for r in res_list:
            mess = "시설명: " + r[0] + "\n지역: " + r[1] + "\n면적: " + r[2] + "\n바닥 재질: " + r[3] + "\n위도: " + r[
                4] + "\n경도: " + r[5] + "\n주소: " + r[6] + "\n"
            noti.sendMessage(user, mess)
            find = True

        if not find:
            noti.sendMessage(user, loc_param + "에 해당하는 데이터가 없습니다.\n")
            pass
    def add_bookmark(self,data):
        if data not in self.bookmark:
            self.bookmark.append(data)
    def erase_bookmark(self,data):
        for i, favorite in enumerate(self.bookmark):
            if favorite[0] == data[0]:
                del self.bookmark[i]
                break
    def bookmarkdata(self, user, bookmark):
        noti.sendMessage(user, "즐겨찾기 목록입니다.\n")
        for r in bookmark:
            mess = "시설명: " + r[0] + "\n지역: " + r[1] + "\n면적: " + r[2] + "\n바닥 재질: " + r[3] + "\n위도: " + r[
                4] + "\n경도: " + r[5] + "\n주소: " + r[6] + "\n"
            noti.sendMessage(user, mess)

    def handle(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type != 'text':
            noti.sendMessage(chat_id, '난 텍스트 이외의 메시지는 처리하지 못해요.')
            return

        text = msg['text']
        args = text.split(' ')

        if text.startswith('지역') and len(args) > 1:
            print('try to 지역', args[1])
            self.StadiumData(chat_id, args[1])
        elif text.startswith('즐겨찾기'):
            self.bookmarkdata(chat_id,self.bookmark)
        elif text.startswith('종료'):
            self.running=False
            noti.sendMessage(chat_id, '봇을 종료합니다.')
        else:
            noti.sendMessage(chat_id, '모르는 명령어입니다.\n지역 ex)지역 시흥시 or 지역 시흥\n 즐겨찾기 \n 종료 중 하나의 명령을 입력하세요.')

    def run(self):
        pprint(self.bot.getMe())
        self.bot.message_loop(self.handle)
        self.running = True
        while self.running:
            time.sleep(10)
