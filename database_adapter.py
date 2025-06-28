import os
from typing import List, Dict, Optional
from database import MarioDatabase
from s3_database import S3Database
import logging

logger = logging.getLogger(__name__)

class DatabaseAdapter:
    """数据库适配器，统一S3数据库和本地数据库的接口"""
    
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
            print("Using local database: mario_stats.db")
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
            # S3数据库查询
            query = "SELECT * FROM users WHERE user_id = ?"
            result = self.db.execute_query(query, (user_id,))
            if result and result[0]:
                row = result[0]
                return {
                    'id': row[0], 'user_id': row[1], 'code': row[2], 
                    'name': row[3], 'created_at': row[4], 'updated_at': row[5]
                }
        else:
            # 本地数据库查询
            return self.db.get_user_by_id(user_id)
        return None
    
    def get_user_by_code(self, code: str) -> Optional[Dict]:
        """根据代码获取用户信息"""
        if self.is_s3:
            # S3数据库查询
            query = "SELECT * FROM users WHERE code = ?"
            result = self.db.execute_query(query, (code,))
            if result and result[0]:
                row = result[0]
                return {
                    'id': row[0], 'user_id': row[1], 'code': row[2], 
                    'name': row[3], 'created_at': row[4], 'updated_at': row[5]
                }
        else:
            # 本地数据库查询
            return self.db.get_user_by_code(code)
        return None
    
    def get_user_stats(self, user_code: str, limit: int = None) -> List[Dict]:
        """获取用户的统计数据"""
        if self.is_s3:
            # S3数据库查询
            query = """
                SELECT * FROM daily_stats 
                WHERE user_code = ? 
                ORDER BY record_date DESC
            """
            if limit:
                query += f" LIMIT {limit}"
            
            result = self.db.execute_query(query, (user_code,))
            if result:
                return [{
                    'id': row[0], 'user_code': row[1], 'wins': row[2], 'plays': row[3],
                    'win_rate': row[4], 'rate': row[5], 'rate_change': row[6],
                    'wins_total': row[7], 'plays_total': row[8], 'record_date': row[9],
                    'record_time': row[10], 'created_at': row[11]
                } for row in result]
        else:
            # 本地数据库查询
            return self.db.get_user_stats(user_code, limit)
        return []
    
    def get_all_users(self) -> List[Dict]:
        """获取所有用户"""
        if self.is_s3:
            # S3数据库查询
            query = "SELECT * FROM users ORDER BY name"
            result = self.db.execute_query(query)
            if result:
                return [{
                    'id': row[0], 'user_id': row[1], 'code': row[2], 
                    'name': row[3], 'created_at': row[4], 'updated_at': row[5]
                } for row in result]
        else:
            # 本地数据库查询
            return self.db.get_all_users()
        return []
    
    def get_latest_stats_for_all_users(self) -> List[Dict]:
        """获取所有用户的最新统计数据"""
        if self.is_s3:
            # S3数据库查询
            query = """
                SELECT u.user_id, u.code, u.name, ds.*
                FROM users u
                LEFT JOIN daily_stats ds ON u.code = ds.user_code
                WHERE ds.record_date = (
                    SELECT MAX(record_date) 
                    FROM daily_stats ds2 
                    WHERE ds2.user_code = u.code
                )
                ORDER BY u.name
            """
            result = self.db.execute_query(query)
            if result:
                return [{
                    'user_id': row[0], 'code': row[1], 'name': row[2],
                    'wins': row[5], 'plays': row[6], 'win_rate': row[7],
                    'rate': row[8], 'rate_change': row[9], 'wins_total': row[10],
                    'plays_total': row[11], 'record_date': row[12], 'record_time': row[13]
                } for row in result if row[5] is not None]
        else:
            # 本地数据库查询
            return self.db.get_latest_stats_for_all_users()
        return []
    
    def search_players(self, query: str) -> List[Dict]:
        """搜索玩家"""
        if self.is_s3:
            # S3数据库查询
            search_query = f"%{query}%"
            sql_query = """
                SELECT DISTINCT u.user_id, u.code, u.name
                FROM users u
                WHERE u.name LIKE ? OR u.code LIKE ? OR u.user_id LIKE ?
                ORDER BY u.name
                LIMIT 20
            """
            result = self.db.execute_query(sql_query, (search_query, search_query, search_query))
            if result:
                return [{
                    'user_id': row[0], 'code': row[1], 'name': row[2]
                } for row in result]
        else:
            # 本地数据库查询
            return self.db.search_players(query)
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
        """根据代码获取玩家名字（仅本地数据库支持）"""
        if not self.is_s3:
            return self.db.get_player_name_by_code(code)
        return code
    
    def close(self):
        """关闭数据库连接"""
        if self.is_s3:
            self.db.close() 