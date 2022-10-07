import requests
import json
import time
import csv

class API():
    def __init__(self,path,time_n):
        self.path = path
        self.time_n = time_n

    def read_lastline(self):
        with open(self.path) as csvfile:
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

    def get_versus_plays(self,user_id):
        url = "https://tgrcode.com/mm2/user_info/%s" % user_id
        res = requests.get(url)
        win = json.loads(res.text)
        return win['versus_plays']

    def get_versus_won(self,user_id):
        url = "https://tgrcode.com/mm2/user_info/%s" % user_id
        res = requests.get(url)
        win = json.loads(res.text)
        return win['versus_won']

    def get_print(self,user_id):
        res = api.get_user_info(user_id)
        begin_won, begin_plays, begin_rate = api.read_lastline()
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
        with open(self.path, 'a+', newline='') as csvfile:
            win, plays, rate, rate_change, win_total, plays_total, versus_rating = api.get_print(user_id)
            writer = csv.writer(csvfile)
            writer.writerow([win, plays, versus_rating, rate ,rate_change, win_total, plays_total, self.time_n])

    def create_csv(self,user_id):
        with open(user_id + ".csv", "w") as csvfile:
            writer = csv.writer(csvfile)

            # 先写入header
            writer.writerow(["wins","plays","win_rate","rate","rate_change","wins_total","plays_total","time"])
            self.write_to_csv(user_id)



if __name__ == '__main__':
    path = "C:\\Users\\Codex\\Desktop\\mario.csv"
    time_n = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #user_id = "Y9P7BN4JF"
    user_id = "0MMCG9V4G"


    api = API(path,time_n)

    api.create_csv(user_id)
    win,plays,rate,rate_change,win_total,plays_total,versus_rating = api.get_print(user_id)

    if (plays != -1):
        api.write_to_csv(user_id)
        print("今日胜利数:{}    今日总局数:{}   胜率:{:.2f}   分数{}   分数变动{}   胜利数:{}    总局数:{}    测试时间:{} ".format(win,plays,versus_rating,rate,rate_change, win_total,plays_total,time_n))
