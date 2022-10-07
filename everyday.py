import requests
import json
import time
import csv
import os


class API():
    def __init__(self,user_id):
        self.user_id = user_id

    def read_lastline(self,user_id):
        with open( name + ".csv") as csvfile:
            mlines = csvfile.readlines()
            targetline = mlines[-1]
            list = targetline.split(',')
            begin_plays = int(list[6])
            begin_won = int(list[5])
            begin_rate = int(list[3])
            return begin_won, begin_plays,begin_rate


    def get_user_info(self,user_id):
        url = "https://tgrcode.com/mm2/user_info/%s" % user_id
        res = requests.get(url)
        try:
            return json.loads(res.text)
        except Exception:
            return res.text


    def get_print(self,user_id):
        res = api.get_user_info(user_id)
        begin_won, begin_plays, begin_rate = api.read_lastline(user_id)
        plays = res['versus_plays'] - begin_plays
        win = res['versus_won'] - begin_won
        rate = res['versus_rating']
        rate_change = res['versus_rating'] - begin_rate
        win_total = res['versus_won']
        plays_total = res['versus_plays']
        if(plays==0):
            plays -=1
        versus_rating = round(win / float(plays), 2)
        return win,plays,rate,rate_change,win_total,plays_total,versus_rating


    def write_to_csv(self,user_id):
        with open( name + ".csv", 'a+', newline='') as csvfile:
            win, plays, rate, rate_change, win_total, plays_total, versus_rating = api.get_print(user_id)
            writer = csv.writer(csvfile)
            writer.writerow([win, plays, versus_rating, rate ,rate_change, win_total, plays_total,time_n])


    def first_line(self,user_id):
        res = api.get_user_info(user_id)
        rate = res['versus_rating']
        win_total = res['versus_won']
        plays_total = res['versus_plays']
        return rate,win_total,plays_total


    def create_csv(self,user_id):
        with open( name + ".csv", "w",newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["wins","plays","win_rate","rate","rate_change","wins_total","plays_total","time"])
            rate, win_total, plays_total= api.first_line(user_id)
            writer.writerow([0, 0, 0, rate ,0, win_total,plays_total,time_n])


if __name__ == '__main__':
    start = time.time()
    time_n = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    user_id = "Y9P7BN4JF"
    user_ids = ["Y9P7BN4JF", "0MMCG9V4G", "SQW0796SF", "GDH8R4V4G", "D221SPHLF","Q5MBL99QG","D049HCB8G"]

    for user_id in user_ids:

        api = API(user_id)
        name = api.get_user_info(user_id)['name']
        path =  name + ".csv"
        if (os.path.exists( name + ".csv") == False):
            api.create_csv(user_id)
        elif (os.path.exists( name + ".csv") ):
            win, plays, rate, rate_change, win_total, plays_total, versus_rating = api.get_print(user_id)
            if(plays != -1):
                api.write_to_csv(user_id)
                print("今日胜利数:{}    今日总局数:{}   胜率:{:.2f}   分数{}   分数变动{}   胜利数:{}    总局数:{}    测试时间:{} ".format(win, plays,
                                                                                                               versus_rating,
                                                                                                               rate,
                                                                                                               rate_change,
                                                                                                               win_total,
                                                                                                               plays_total,
                                                                                                               time_n))




