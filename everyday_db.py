#!/usr/bin/env python3
"""
Mario Maker 2 数据统计 - 数据库版本
使用SQLite数据库存储数据，支持单个用户和批量更新
"""

import sys
import time
import argparse
from database import MarioDatabase, MarioAPI

def update_single_user(user_id: str, db: MarioDatabase) -> bool:
    """更新单个用户数据"""
    print(f"正在更新用户 {user_id} 的数据...")
    
    success = db.fetch_and_update_user_data(user_id)
    
    if success:
        # 获取用户信息和最新统计
        user = db.get_user_by_id(user_id)
        if user:
            stats = db.get_user_stats(user['code'], limit=1)
            if stats:
                stat = stats[0]
                print(f"✅ {user['name']} ({user['code']}):")
                print(f"   今日胜利数: {stat['wins']}")
                print(f"   今日总局数: {stat['plays']}")
                print(f"   今日胜率: {stat['win_rate']:.2f}")
                print(f"   当前分数: {stat['rate']}")
                print(f"   分数变动: {stat['rate_change']:+d}")
                print(f"   总胜利数: {stat['wins_total']}")
                print(f"   总局数: {stat['plays_total']}")
                print(f"   记录时间: {stat['record_time']}")
            else:
                print(f"✅ {user['name']} ({user['code']}) - 用户信息已更新")
        else:
            print(f"✅ 用户 {user_id} 数据已更新")
    else:
        print(f"❌ 更新用户 {user_id} 失败")
    
    return success

def update_all_users(db: MarioDatabase, user_ids: list = None) -> dict:
    """批量更新用户数据"""
    if user_ids is None:
        # 使用默认用户列表
        user_ids = [
            "Y9P7BN4JF", "SQW0796SF", "GDH8R4V4G", "D221SPHLF", 
            "Q5MBL99QG", "4QVF9V6RF", "D049HCB8G", "1VVRCXQPF", 
            "D8CJ2W62H", "LDMLC6RLG", "0JR5R5BJG", "08VW66RLF"
        ]
    
    print(f"开始批量更新 {len(user_ids)} 个用户的数据...")
    
    successful_updates = 0
    failed_updates = []
    start_time = time.time()
    
    for i, user_id in enumerate(user_ids, 1):
        print(f"\n[{i}/{len(user_ids)}] ", end="")
        
        try:
            success = update_single_user(user_id, db)
            if success:
                successful_updates += 1
            else:
                failed_updates.append(user_id)
        except Exception as e:
            print(f"❌ 更新用户 {user_id} 时出错: {e}")
            failed_updates.append(f"{user_id}: {str(e)}")
        
        # 避免频繁请求API
        if i < len(user_ids):
            time.sleep(1)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"\n" + "="*50)
    print(f"批量更新完成!")
    print(f"总用时: {elapsed_time:.2f} 秒")
    print(f"成功更新: {successful_updates} 个用户")
    print(f"失败: {len(failed_updates)} 个用户")
    
    if failed_updates:
        print(f"失败列表: {failed_updates}")
    
    return {
        'successful_updates': successful_updates,
        'failed_updates': failed_updates,
        'elapsed_time': elapsed_time
    }

def migrate_csv_to_db(db: MarioDatabase):
    """从CSV文件迁移数据到数据库"""
    print("开始从CSV文件迁移数据到数据库...")
    db.migrate_from_csv()
    print("迁移完成!")

def show_user_info(user_id: str, db: MarioDatabase):
    """显示用户信息和统计"""
    user = db.get_user_by_id(user_id) or db.get_user_by_code(user_id)
    
    if not user:
        print(f"未找到用户 {user_id}")
        return
    
    print(f"\n用户信息:")
    print(f"  用户ID: {user['user_id']}")
    print(f"  代码: {user['code']}")
    print(f"  姓名: {user['name']}")
    print(f"  创建时间: {user['created_at']}")
    print(f"  更新时间: {user['updated_at']}")
    
    # 获取最近的统计数据
    stats = db.get_user_stats(user['code'], limit=10)
    
    if stats:
        print(f"\n最近 {len(stats)} 条记录:")
        print("日期          胜利  游戏  胜率   分数   变动   总胜利  总游戏")
        print("-" * 65)
        for stat in stats:
            print(f"{stat['record_date']} {stat['wins']:4d} {stat['plays']:4d} "
                  f"{stat['win_rate']:5.2f} {stat['rate']:6d} {stat['rate_change']:+5d} "
                  f"{stat['wins_total']:6d} {stat['plays_total']:7d}")
    else:
        print("  暂无统计数据")

def main():
    parser = argparse.ArgumentParser(description='Mario Maker 2 数据统计工具 (数据库版本)')
    parser.add_argument('--user-id', '-u', help='指定要更新的用户ID')
    parser.add_argument('--batch', '-b', action='store_true', help='批量更新所有默认用户')
    parser.add_argument('--migrate', '-m', action='store_true', help='从CSV文件迁移数据到数据库')
    parser.add_argument('--show', '-s', help='显示指定用户的信息和统计')
    parser.add_argument('--user-list', nargs='+', help='自定义用户ID列表进行批量更新')
    parser.add_argument('--db-path', default='mario_stats.db', help='数据库文件路径')
    
    args = parser.parse_args()
    
    # 初始化数据库
    db = MarioDatabase(args.db_path)
    
    # 显示当前时间
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"Mario Maker 2 数据统计工具 - {current_time}")
    print(f"数据库: {args.db_path}")
    print("=" * 50)
    
    if args.migrate:
        # 迁移CSV数据
        migrate_csv_to_db(db)
        
    elif args.show:
        # 显示用户信息
        show_user_info(args.show, db)
        
    elif args.user_id:
        # 更新单个用户
        update_single_user(args.user_id, db)
        
    elif args.batch or args.user_list:
        # 批量更新
        user_list = args.user_list if args.user_list else None
        update_all_users(db, user_list)
        
    else:
        # 默认行为：显示帮助
        parser.print_help()
        print("\n示例用法:")
        print("  python3 everyday_db.py --user-id Y9P7BN4JF          # 更新单个用户")
        print("  python3 everyday_db.py --batch                      # 批量更新所有默认用户")
        print("  python3 everyday_db.py --show Y9P7BN4JF             # 显示用户信息")
        print("  python3 everyday_db.py --migrate                    # 从CSV迁移数据")
        print("  python3 everyday_db.py --user-list A B C            # 更新指定用户列表")

if __name__ == "__main__":
    main() 