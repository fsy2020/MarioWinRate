## 超级马里奥制造2 胜率统计教程
## 中文
* 需要的前置知识包括一台可运行的服务器，linux命令基本操作，和简单的python知识。
* 感谢[tgrcode](https://tgrcode.com/mm2/docs/)提供的数据库和api，这个程序主要是统计每天的马造胜利数和总游玩数，并进行自动记录。

### 方法
* 在everyday.py文件中的user_ids数组中添加自己的马造游玩ID。  
![image](./user_id.png)
### 运行
* 我是放在树莓派上用crontab命令每天5点和6点自动运行everyday.py文件，并自动记录每天的log，计算上一天的胜利数，游玩总数，胜率，分数变动和时间等参数，crontab的命令如下，请修改文件地址。 需要对生成的每一个文件赋予权限，chmod 777
```
sudo apt-get install vim
```  
```
su root
```  
```
chomod 777 everyday.py
```  
```
crontab -e
```  
```
0 5,6 * * * /usr/bin/python3 /home/pi/everyday.py >> /home/pi/cron_$(date +\%Y-\%m-\%d).log 2>&1
```  
```
service cron restart
``` 
### 结果
第一次运行只会记录当前的信息，无法获得前一天胜率。
此后在每天的5点和6点运行，每运行一次就会记录上一天到当前时间点的胜率数据。
如果成功运行并记录，最后的结果如下图所示，这是我最近一段时间的游玩记录：  
![image](https://github.com/user-attachments/assets/554ac569-f438-42fe-9be1-1259655f08d9)

![image](./Panzi.png)

## Super Mario Maker 2 Winning Statistics Tutorial
### English version
* Count the number of wins and totals per day, run and record them daily.

### Method
* Add your own player ID to the user_ids array.  

![image](./user_id.png)

### How to run
* I am putting it on the Raspberry Pi with the crontab command to run the everyday.py file automatically every day at 8:00. The crontab command is as follows, please change the file address. 
vim installing, and the task will be done in in 5:00,6:00.
```
sudo apt-get install vim
```  
```
su root
```  
```
chomod 777 everyday.py
```  
```
crontab -e
```  
```
0 5,6 * * * /usr/bin/python3 /home/pi/everyday.py >> /home/pi/cron_$(date +\%Y-\%m-\%d).log 2>&1
```  
```
service cron restart
```  

### Result
The first run will record the current information, each run will record win rate data from the previous day to the current point in time.

![image](https://github.com/user-attachments/assets/518cb9a6-8537-485b-bb25-7d796f3016a6)



