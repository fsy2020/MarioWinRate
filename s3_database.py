import sqlite3
import os
import tempfile
import boto3
from botocore.exceptions import ClientError
import hashlib
import time
from typing import Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3Database:
    def __init__(self, bucket_name: str, db_key: str, region_name: str = 'us-east-1'):
        """
        初始化S3数据库连接
        
        Args:
            bucket_name: S3存储桶名称
            db_key: 数据库文件在S3中的键名
            region_name: AWS区域
        """
        self.bucket_name = bucket_name
        self.db_key = db_key
        self.region_name = region_name
        self.local_db_path = None
        self.last_download_time = 0
        self.download_interval = 300  # 5分钟下载间隔
        
        # 初始化S3客户端
        self.s3_client = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        
        # 确保本地数据库文件存在
        self._ensure_local_db()
    
    def _get_temp_db_path(self) -> str:
        """获取临时数据库文件路径"""
        if not self.local_db_path:
            # 在/tmp目录下创建临时文件（Vercel环境）
            temp_dir = '/tmp' if os.path.exists('/tmp') else tempfile.gettempdir()
            self.local_db_path = os.path.join(temp_dir, f'mario_filtered_{hashlib.md5(self.db_key.encode()).hexdigest()[:8]}.db')
        return self.local_db_path
    
    def _should_download_db(self) -> bool:
        """判断是否需要重新下载数据库"""
        local_path = self._get_temp_db_path()
        
        # 如果本地文件不存在，需要下载
        if not os.path.exists(local_path):
            return True
        
        # 检查下载间隔
        current_time = time.time()
        if current_time - self.last_download_time > self.download_interval:
            return True
        
        return False
    
    def _download_db_from_s3(self) -> bool:
        """从S3下载数据库文件"""
        try:
            local_path = self._get_temp_db_path()
            
            logger.info(f"Downloading database from s3://{self.bucket_name}/{self.db_key}")
            
            # 下载文件
            self.s3_client.download_file(
                self.bucket_name,
                self.db_key,
                local_path
            )
            
            self.last_download_time = time.time()
            logger.info(f"Database downloaded successfully to {local_path}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to download database from S3: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error downloading database: {e}")
            return False
    
    def _ensure_local_db(self) -> bool:
        """确保本地数据库文件存在且是最新的"""
        if self._should_download_db():
            return self._download_db_from_s3()
        return True
    
    def get_connection(self) -> Optional[sqlite3.Connection]:
        """获取数据库连接"""
        if not self._ensure_local_db():
            logger.error("Failed to ensure local database exists")
            return None
        
        try:
            local_path = self._get_temp_db_path()
            return sqlite3.connect(local_path)
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return None
    
    def execute_query(self, query: str, params: tuple = ()) -> Optional[list]:
        """执行查询并返回结果"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                conn.commit()
                return []
                
        except Exception as e:
            logger.error(f"Query execution failed: {e}")
            return None
        finally:
            conn.close()
    
    def get_table_names(self) -> list:
        """获取所有表名"""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        result = self.execute_query(query)
        return [row[0] for row in result] if result else []
    
    def get_table_schema(self, table_name: str) -> list:
        """获取表结构"""
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query) or []
    
    def close(self):
        """清理资源"""
        if self.local_db_path and os.path.exists(self.local_db_path):
            try:
                os.remove(self.local_db_path)
                logger.info(f"Removed temporary database file: {self.local_db_path}")
            except Exception as e:
                logger.warning(f"Failed to remove temporary database file: {e}") 