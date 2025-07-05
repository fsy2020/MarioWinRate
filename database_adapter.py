import os
from typing import List, Dict, Optional
from database import MarioDatabase
from s3_database import S3Database
import logging

logger = logging.getLogger(__name__)

class DatabaseAdapter:
    
    def __init__(self):
        self.db = self._get_database()
        self.is_s3 = isinstance(self.db, S3Database)
        
        # 缓存表结构信息
        self._table_info = {}
        self._load_table_info()
    
    def _get_database(self):
        """根据环境变量选择数据库类型"""
        # 检查是否有S3环境变量
        if (os.environ.get('AWS_ACCESS_KEY_ID') and 
            os.environ.get('AWS_SECRET_ACCESS_KEY') and
            os.environ.get('S3_BUCKET_NAME') and
            os.environ.get('S3_DB_KEY')):
            
            # 使用S3数据库
            bucket_name = os.environ.get('S3_BUCKET_NAME')
            db_key = os.environ.get('S3_DB_KEY', 'mario_filtered.db')
            region_name = os.environ.get('AWS_REGION', 'us-east-1')
            
            print(f"Using S3 database: s3://{bucket_name}/{db_key}")
            return S3Database(bucket_name, db_key, region_name)
        else:
            # 使用本地数据库
            print("Using local database: mario_filtered.db")
            return MarioDatabase()
    
    def _load_table_info(self):
        """加载表结构信息"""
        try:
            if self.is_s3:
                tables = self.db.get_table_names()
                for table in tables:
                    schema = self.db.get_table_schema(table)
                    self._table_info[table] = schema
                logger.info(f"Loaded table info for tables: {tables}")
            else:
                self.db.load_table_info()
        except Exception as e:
            logger.error(f"Failed to load table info: {e}")
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """根据用户ID获取用户信息"""
        if self.is_s3:
            # S3数据库查询 - 使用player表
            query = "SELECT * FROM player WHERE pid = ?"
            result = self.db.execute_query(query, (user_id,))
            if result and result[0]:
                row = result[0]
                return {
                    'pid': row[0], 'name': row[1]
                }
        else:
            # 本地数据库查询
            return self.db.get_user_by_id(user_id)
        return None
    
    def get_user_by_code(self, code: str) -> Optional[Dict]:
        """根据代码获取用户信息"""
        if self.is_s3:
            # S3数据库查询 - 使用player表
            query = "SELECT * FROM player WHERE pid = ?"
            result = self.db.execute_query(query, (code,))
            if result and result[0]:
                row = result[0]
                return {
                    'pid': row[0], 'name': row[1]
                }
        else:
            # 本地数据库查询
            return self.db.get_user_by_code(code)
        return None
    
    def get_user_stats(self, user_code: str, limit: int = None) -> List[Dict]:
        """获取用户的统计数据"""
        if self.is_s3:
            # S3数据库查询 - 使用player_stats_snapshot表
            query = """
                SELECT * FROM player_stats_snapshot 
                WHERE pid = ? 
                ORDER BY stat_date DESC
            """
            if limit:
                query += f" LIMIT {limit}"
            
            result = self.db.execute_query(query, (user_code,))
            if result:
                return [{
                    'pid': row[0], 'stat_date': row[1], 'versus_rating': row[2], 
                    'versus_won': row[3], 'versus_plays': row[4],
                    'win_rate': round(row[3] / row[4] * 100, 2) if row[4] > 0 else 0
                } for row in result]
        else:
            # 本地数据库查询
            return self.db.get_user_stats(user_code, limit)
        return []
    
    def get_all_users(self) -> List[Dict]:
        """获取所有用户"""
        if self.is_s3:
            # S3数据库查询 - 使用player表
            query = "SELECT * FROM player ORDER BY name"
            result = self.db.execute_query(query)
            if result:
                return [{
                    'pid': row[0], 'name': row[1]
                } for row in result]
        else:
            # 本地数据库查询
            return self.db.get_all_users()
        return []
    
    def get_latest_stats_for_all_users(self) -> List[Dict]:
        """获取所有用户的最新统计数据"""
        if self.is_s3:
            # S3数据库查询 - 使用player和player_stats_snapshot表
            query = """
                SELECT p.pid, p.name, ps.*
                FROM player p
                LEFT JOIN player_stats_snapshot ps ON p.pid = ps.pid
                WHERE ps.stat_date = (
                    SELECT MAX(stat_date) 
                    FROM player_stats_snapshot ps2 
                    WHERE ps2.pid = p.pid
                )
                ORDER BY p.name
            """
            result = self.db.execute_query(query)
            if result:
                return [{
                    'pid': row[0], 'name': row[1],
                    'versus_rating': row[4], 'versus_won': row[5], 'versus_plays': row[6],
                    'win_rate': round(row[5] / row[6] * 100, 2) if row[6] > 0 else 0,
                    'stat_date': row[3]
                } for row in result if row[4] is not None]
        else:
            # 本地数据库查询
            return self.db.get_latest_stats_for_all_users()
        return []
    
    def search_players(self, query: str) -> List[Dict]:
        """搜索玩家"""
        if self.is_s3:
            # S3数据库查询 - 使用player表
            search_query = f"%{query}%"
            sql_query = """
                SELECT DISTINCT p.pid, p.name
                FROM player p
                WHERE p.name LIKE ? OR p.pid LIKE ? OR p.code LIKE ?
                ORDER BY p.name
                LIMIT 20
            """
            result = self.db.execute_query(sql_query, (search_query, search_query, search_query))
            if result:
                return [{
                    'pid': row[0], 'name': row[1]
                } for row in result]
        else:
            # 本地数据库查询
            return self.db.search_players(query)
        return []
    
    def get_player_stats_delta(self, user_code: str, limit: int = None) -> List[Dict]:
        """获取用户的统计变化数据"""
        if self.is_s3:
            # S3数据库查询 - 使用player_stats_delta表
            query = """
                SELECT * FROM player_stats_delta 
                WHERE pid = ? 
                ORDER BY stat_date DESC
            """
            if limit:
                query += f" LIMIT {limit}"
            
            result = self.db.execute_query(query, (user_code,))
            if result:
                return [{
                    'pid': row[0], 'stat_date': row[1], 'delta_rating': row[2], 
                    'delta_won': row[3], 'delta_plays': row[4]
                } for row in result]
        else:
            # 本地数据库查询 - 如果本地数据库支持的话
            return []
        return []
    
    def get_user_info_from_api(self, user_id: str) -> Optional[Dict]:
        """从API获取用户信息（仅本地数据库支持）"""
        if not self.is_s3:
            return self.db.get_user_info_from_api(user_id)
        return None
    
    def fetch_and_update_user_data(self, user_id: str) -> bool:
        """获取并更新用户数据（仅本地数据库支持）"""
        if not self.is_s3:
            return self.db.fetch_and_update_user_data(user_id)
        return False
    
    def load_player_names_from_cron_log(self, cron_log_path: str = "data/cron.log") -> bool:
        """加载玩家名字（仅本地数据库支持）"""
        if not self.is_s3:
            return self.db.load_player_names_from_cron_log(cron_log_path)
        return False
    
    def get_player_name_by_code(self, code: str) -> str:
        """根据代码获取玩家名字"""
        if self.is_s3:
            # S3数据库查询 - 使用player表
            query = "SELECT name FROM player WHERE pid = ?"
            result = self.db.execute_query(query, (code,))
            if result and result[0]:
                return result[0][0]
            return code
        else:
            # 本地数据库查询
            return self.db.get_player_name_by_code(code)
    
    def close(self):
        """关闭数据库连接"""
        if self.is_s3:
            self.db.close() 