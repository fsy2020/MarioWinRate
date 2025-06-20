import sqlite3
import csv
import os
import time
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import requests
import json

class MarioDatabase:
    def __init__(self, db_path: str = "mario_stats.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """初始化数据库表结构"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 用户信息表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    code TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 每日统计表
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS daily_stats (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_code TEXT NOT NULL,
                    wins INTEGER NOT NULL,
                    plays INTEGER NOT NULL,
                    win_rate REAL NOT NULL,
                    rate INTEGER NOT NULL,
                    rate_change INTEGER NOT NULL,
                    wins_total INTEGER NOT NULL,
                    plays_total INTEGER NOT NULL,
                    record_date DATE NOT NULL,
                    record_time TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_code) REFERENCES users (code),
                    UNIQUE(user_code, record_date)
                )
            """)
            
            # 创建索引
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_stats_user_code ON daily_stats(user_code)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_daily_stats_date ON daily_stats(record_date)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_user_id ON users(user_id)")
            
            conn.commit()
    
    def add_user(self, user_id: str, code: str, name: str) -> bool:
        """添加或更新用户信息"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO users (user_id, code, name, updated_at)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                """, (user_id, code, name))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False
    
    def add_daily_stat(self, user_code: str, wins: int, plays: int, win_rate: float,
                      rate: int, rate_change: int, wins_total: int, plays_total: int,
                      record_time: str) -> bool:
        """添加每日统计数据"""
        try:
            # 解析时间格式
            if "/" in record_time:
                # 格式: 2024/5/8 21:49
                dt = datetime.strptime(record_time, "%Y/%m/%d %H:%M")
            elif "-" in record_time and ":" in record_time:
                # 格式: 2024-05-13 22:04:25
                dt = datetime.strptime(record_time, "%Y-%m-%d %H:%M:%S")
            else:
                dt = datetime.now()
            
            record_date = dt.date().isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO daily_stats 
                    (user_code, wins, plays, win_rate, rate, rate_change, 
                     wins_total, plays_total, record_date, record_time)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_code, wins, plays, win_rate, rate, rate_change,
                      wins_total, plays_total, record_date, record_time))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error adding daily stat: {e}")
            return False
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """根据用户ID获取用户信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0], 'user_id': row[1], 'code': row[2], 
                    'name': row[3], 'created_at': row[4], 'updated_at': row[5]
                }
        return None
    
    def get_user_by_code(self, code: str) -> Optional[Dict]:
        """根据代码获取用户信息"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE code = ?", (code,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0], 'user_id': row[1], 'code': row[2], 
                    'name': row[3], 'created_at': row[4], 'updated_at': row[5]
                }
        return None
    
    def get_user_stats(self, user_code: str, limit: int = None) -> List[Dict]:
        """获取用户的统计数据"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query = """
                SELECT * FROM daily_stats 
                WHERE user_code = ? 
                ORDER BY record_date DESC
            """
            if limit:
                query += f" LIMIT {limit}"
            
            cursor.execute(query, (user_code,))
            rows = cursor.fetchall()
            
            return [{
                'id': row[0], 'user_code': row[1], 'wins': row[2], 'plays': row[3],
                'win_rate': row[4], 'rate': row[5], 'rate_change': row[6],
                'wins_total': row[7], 'plays_total': row[8], 'record_date': row[9],
                'record_time': row[10], 'created_at': row[11]
            } for row in rows]
    
    def get_all_users(self) -> List[Dict]:
        """获取所有用户"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users ORDER BY name")
            rows = cursor.fetchall()
            
            return [{
                'id': row[0], 'user_id': row[1], 'code': row[2], 
                'name': row[3], 'created_at': row[4], 'updated_at': row[5]
            } for row in rows]
    
    def get_latest_stats_for_all_users(self) -> List[Dict]:
        """获取所有用户的最新统计数据"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.user_id, u.code, u.name, ds.*
                FROM users u
                LEFT JOIN daily_stats ds ON u.code = ds.user_code
                WHERE ds.record_date = (
                    SELECT MAX(record_date) 
                    FROM daily_stats ds2 
                    WHERE ds2.user_code = u.code
                )
                ORDER BY u.name
            """)
            rows = cursor.fetchall()
            
            return [{
                'user_id': row[0], 'code': row[1], 'name': row[2],
                'wins': row[5], 'plays': row[6], 'win_rate': row[7],
                'rate': row[8], 'rate_change': row[9], 'wins_total': row[10],
                'plays_total': row[11], 'record_date': row[12], 'record_time': row[13]
            } for row in rows if row[5] is not None]
    
    def migrate_from_csv(self, data_dir: str = "data"):
        """从CSV文件迁移数据到数据库"""
        if not os.path.exists(data_dir):
            print(f"Data directory {data_dir} not found")
            return
        
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        
        for csv_file in csv_files:
            user_code = csv_file.replace('.csv', '')
            csv_path = os.path.join(data_dir, csv_file)
            
            print(f"Migrating {csv_file}...")
            
            # 首先尝试获取用户信息
            user_info = self.get_user_info_from_api(user_code)
            if user_info:
                self.add_user(user_info.get('user_id', user_code), user_code, user_info.get('name', user_code))
            else:
                # 如果API获取失败，使用默认值
                self.add_user(user_code, user_code, user_code)
            
            # 读取CSV数据
            with open(csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    try:
                        self.add_daily_stat(
                            user_code=user_code,
                            wins=int(row['wins']),
                            plays=int(row['plays']),
                            win_rate=float(row['win_rate']),
                            rate=int(row['rate']),
                            rate_change=int(row['rate_change']),
                            wins_total=int(row['wins_total']),
                            plays_total=int(row['plays_total']),
                            record_time=row['time']
                        )
                    except Exception as e:
                        print(f"Error processing row in {csv_file}: {e}")
                        continue
        
        print("Migration completed!")
    
    def get_user_info_from_api(self, user_id: str) -> Optional[Dict]:
        """从API获取用户信息"""
        try:
            url = f"https://tgrcode.com/mm2/user_info/{user_id}"
            response = requests.get(url, timeout=10)
            time.sleep(1)  # 避免频繁请求
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'user_id': user_id,
                    'code': data.get('code', user_id),
                    'name': data.get('name', user_id),
                    'versus_plays': data.get('versus_plays', 0),
                    'versus_won': data.get('versus_won', 0),
                    'versus_rating': data.get('versus_rating', 0)
                }
        except Exception as e:
            print(f"Failed to get user info for {user_id}: {e}")
        
        return None
    
    def fetch_and_update_user_data(self, user_id: str) -> bool:
        """获取并更新单个用户的数据"""
        user_info = self.get_user_info_from_api(user_id)
        if not user_info:
            return False
        
        # 添加或更新用户信息
        self.add_user(user_info['user_id'], user_info['code'], user_info['name'])
        
        # 获取最后一条记录来计算今日变化
        last_stats = self.get_user_stats(user_info['code'], limit=1)
        
        if last_stats:
            last_stat = last_stats[0]
            wins = user_info['versus_won'] - last_stat['wins_total']
            plays = user_info['versus_plays'] - last_stat['plays_total']
            rate_change = user_info['versus_rating'] - last_stat['rate']
        else:
            # 首次记录
            wins = 0
            plays = 0
            rate_change = 0
        
        # 避免除零错误
        if plays == 0:
            plays = 1 if wins > 0 else 0
            win_rate = 0.0
        else:
            win_rate = round(wins / plays, 2) if plays > 0 else 0.0
        
        # 添加今日统计
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return self.add_daily_stat(
            user_code=user_info['code'],
            wins=wins,
            plays=plays,
            win_rate=win_rate,
            rate=user_info['versus_rating'],
            rate_change=rate_change,
            wins_total=user_info['versus_won'],
            plays_total=user_info['versus_plays'],
            record_time=current_time
        )

    def load_player_names_from_cron_log(self, cron_log_path: str = "data/cron.log") -> bool:
        """从cron.log文件加载玩家名字和ID对应关系并更新数据库"""
        try:
            if not os.path.exists(cron_log_path):
                print(f"Cron log file {cron_log_path} not found")
                return False
                
            with open(cron_log_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                for line in lines:
                    line = line.strip()
                    if not line or line.replace('.', '').isdigit():  # 跳过空行和纯数字行
                        continue
                    
                    # 解析格式: "玩家名字 玩家ID"
                    parts = line.rsplit(' ', 1)  # 从右边分割，只分割一次
                    if len(parts) == 2:
                        name, player_id = parts
                        
                        # 更新或插入用户信息
                        cursor.execute("""
                            INSERT OR REPLACE INTO users (user_id, code, name, updated_at)
                            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                        """, (player_id, player_id, name))
                
                conn.commit()
                print(f"Successfully loaded player names from {cron_log_path}")
                return True
                
        except Exception as e:
            print(f"Error loading player names from cron log: {e}")
            return False

    def get_player_name_by_code(self, code: str) -> str:
        """根据玩家ID获取玩家名字，如果没有找到则返回ID本身"""
        user = self.get_user_by_code(code)
        return user['name'] if user else code

    def search_players(self, query: str) -> List[Dict]:
        """根据名字或ID搜索玩家"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM users 
                WHERE LOWER(name) LIKE LOWER(?) OR LOWER(code) LIKE LOWER(?)
                ORDER BY name
            """, (f'%{query}%', f'%{query}%'))
            rows = cursor.fetchall()
            
            return [{
                'id': row[0], 'user_id': row[1], 'code': row[2], 
                'name': row[3], 'created_at': row[4], 'updated_at': row[5]
            } for row in rows]


class MarioAPI:
    """兼容原有API的类"""
    def __init__(self, user_id: str, db: MarioDatabase):
        self.user_id = user_id
        self.db = db
    
    def get_user_info(self, user_id: str) -> Optional[Dict]:
        """获取用户信息（兼容原有方法）"""
        return self.db.get_user_info_from_api(user_id)
    
    def update_user_data(self, user_id: str) -> bool:
        """更新用户数据（新方法）"""
        return self.db.fetch_and_update_user_data(user_id)


if __name__ == "__main__":
    # 测试数据库功能
    db = MarioDatabase()
    
    # 从CSV迁移数据
    print("Starting migration from CSV files...")
    db.migrate_from_csv()
    
    # 显示迁移结果
    users = db.get_all_users()
    print(f"\nMigrated {len(users)} users:")
    for user in users:
        print(f"- {user['name']} ({user['code']})")
    
    print("\nDatabase setup completed!") 