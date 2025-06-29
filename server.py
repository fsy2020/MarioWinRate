from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import json
import csv
import sqlite3
from database_adapter import DatabaseAdapter

app = Flask(__name__)
CORS(app)

# 初始化数据库适配器
db = DatabaseAdapter()

# 在应用启动时加载cron.log中的玩家名字（仅对本地数据库有效）
if not db.is_s3:
    db.load_player_names_from_cron_log()

# 提供静态文件
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('.', filename)

# API接口：获取所有CSV文件列表（保持向后兼容）
@app.route('/api/files')
def get_files():
    try:
        data_dir = 'data'
        if not os.path.exists(data_dir):
            return jsonify({'error': 'Data directory not found'}), 404
        
        csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
        return jsonify({'files': csv_files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# API接口：获取玩家信息（保持向后兼容）
@app.route('/api/player/<player_id>')
def get_player_info(player_id):
    try:
        # 从数据库获取用户信息
        user = db.get_user_by_code(player_id)
        if user:
            return jsonify({
                'id': user['code'],
                'name': user['name']
            })
        
        # 如果数据库中没有，尝试从API获取
        user_info = db.get_user_info_from_api(player_id)
        if user_info:
            return jsonify({
                'id': user_info['code'],
                'name': user_info['name']
            })
        
        return jsonify({
            'id': player_id,
            'name': player_id
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：获取所有用户列表
@app.route('/api/users')
def get_all_users():
    try:
        users = db.get_all_users()
        return jsonify({'users': users})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：根据用户ID获取用户信息
@app.route('/api/user/<user_id>')
def get_user_by_id(user_id):
    try:
        user = db.get_user_by_id(user_id)
        if user:
            return jsonify({'user': user})
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：获取用户统计数据
@app.route('/api/user/<user_id>/stats')
def get_user_stats(user_id):
    try:
        # 获取用户信息
        user = db.get_user_by_id(user_id) or db.get_user_by_code(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # 获取统计数据
        limit = request.args.get('limit', type=int)
        stats = db.get_user_stats(user['code'], limit)
        
        return jsonify({
            'user': user,
            'stats': stats
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：获取所有用户的最新统计数据
@app.route('/api/latest-stats')
def get_latest_stats():
    try:
        stats = db.get_latest_stats_for_all_users()
        return jsonify({'stats': stats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：通过用户ID获取和更新数据
@app.route('/api/fetch-user-data', methods=['POST'])
def fetch_user_data():
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
        
        # 获取并更新用户数据
        success = db.fetch_and_update_user_data(user_id)
        
        if success:
            # 返回更新后的用户信息
            user = db.get_user_by_id(user_id)
            if user:
                stats = db.get_user_stats(user['code'], limit=1)
                return jsonify({
                    'success': True,
                    'message': 'User data updated successfully',
                    'user': user,
                    'latest_stat': stats[0] if stats else None
                })
            else:
                return jsonify({'success': True, 'message': 'Data updated but user info not found'})
        else:
            return jsonify({'error': 'Failed to fetch user data'}), 500
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：数据库迁移（管理员功能）
@app.route('/api/migrate', methods=['POST'])
def migrate_data():
    try:
        db.migrate_from_csv()
        return jsonify({'success': True, 'message': 'Migration completed successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：批量更新所有用户数据
@app.route('/api/update-all-users', methods=['POST'])
def update_all_users():
    try:
        users = db.get_all_users()
        successful_updates = 0
        failed_updates = []
        
        for user in users:
            try:
                success = db.fetch_and_update_user_data(user['user_id'])
                if success:
                    successful_updates += 1
                else:
                    failed_updates.append(user['user_id'])
            except Exception as e:
                failed_updates.append(f"{user['user_id']}: {str(e)}")
        
        return jsonify({
            'success': True,
            'message': f'Updated {successful_updates} users successfully',
            'successful_updates': successful_updates,
            'failed_updates': failed_updates
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：搜索玩家
@app.route('/api/search-players')
def search_players():
    try:
        query = request.args.get('q', '').strip()
        if not query:
            return jsonify({'players': []})
        
        players = db.search_players(query)
        return jsonify({'players': players})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：重新加载cron.log文件
@app.route('/api/reload-player-names', methods=['POST'])
def reload_player_names():
    try:
        success = db.load_player_names_from_cron_log()
        if success:
            return jsonify({'success': True, 'message': 'Player names reloaded successfully'})
        else:
            return jsonify({'error': 'Failed to reload player names'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：获取所有玩家名字映射
@app.route('/api/player-names')
def get_player_names():
    try:
        users = db.get_all_users()
        name_mapping = {user['code']: user['name'] for user in users}
        return jsonify({'nameMapping': name_mapping})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：获取mario_filtered.db中的player_stats_snapshot数据（分页）
@app.route('/api/player-stats-snapshot')
def get_player_stats_snapshot():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        sort_by = request.args.get('sort_by', 'versus_rating')  # versus_rating, versus_won, versus_plays, win_rate
        sort_order = request.args.get('sort_order', 'desc')  # asc, desc
        search = request.args.get('search', '').strip()
        rank_filter = request.args.get('rank_filter', '').strip()  # 新增：排名过滤 (top10, top100, etc.)
        
        # 限制每页最大数量，防止过度请求
        per_page = min(per_page, 200)
        
        # 使用DatabaseAdapter处理数据库连接
        if db.is_s3:
            # S3数据库查询
            base_query = """
                SELECT p.name, pss.pid, pss.versus_rating, pss.versus_won, pss.versus_plays, pss.stat_date,
                       CASE WHEN pss.versus_plays > 0 THEN (pss.versus_won * 100.0 / pss.versus_plays) ELSE 0 END as win_rate
                FROM player p 
                JOIN player_stats_snapshot pss ON p.pid = pss.pid
            """
            
            # 添加搜索条件
            where_conditions = []
            params = []
            
            # 获取最新日期的数据
            latest_date_query = "SELECT MAX(stat_date) FROM player_stats_snapshot"
            latest_date_result = db.db.execute_query(latest_date_query)
            latest_date = latest_date_result[0][0] if latest_date_result and latest_date_result[0] else None
            
            if latest_date:
                where_conditions.append("pss.stat_date = ?")
                params.append(latest_date)
            
            if search:
                where_conditions.append("(p.name LIKE ? OR pss.pid LIKE ?)")
                params.extend([f'%{search}%', f'%{search}%'])
            
            if where_conditions:
                base_query += " WHERE " + " AND ".join(where_conditions)
            
            # 添加排序
            valid_sort_columns = ['versus_rating', 'versus_won', 'versus_plays', 'name', 'win_rate']
            if sort_by not in valid_sort_columns:
                sort_by = 'versus_rating'
            
            if sort_order.lower() not in ['asc', 'desc']:
                sort_order = 'desc'
            
            order_query = f" ORDER BY {sort_by} {sort_order.upper()}"
            if sort_by != 'name':
                order_query += ", p.name ASC"
            
            # 执行查询
            full_query = base_query + order_query
            all_results = db.db.execute_query(full_query, params)
            
            if not all_results:
                all_results = []
            
            # 应用排名过滤
            if rank_filter:
                if rank_filter == 'top10':
                    filtered_results = all_results[:10]
                elif rank_filter == 'top25':
                    filtered_results = all_results[:25]
                elif rank_filter == 'top50':
                    filtered_results = all_results[:50]
                elif rank_filter == 'top100':
                    filtered_results = all_results[:100]
                else:
                    filtered_results = all_results
                
                total_count = len(filtered_results)
                
                # 应用分页到过滤后的结果
                offset = (page - 1) * per_page
                results = filtered_results[offset:offset + per_page]
            else:
                total_count = len(all_results)
                
                # 应用分页
                offset = (page - 1) * per_page
                results = all_results[offset:offset + per_page]
        else:
            # 本地数据库连接
            import sqlite3
            conn = sqlite3.connect('mario_filtered.db')
            cursor = conn.cursor()
            
            # 构建基础查询 - 添加胜率计算
            base_query = """
                SELECT p.name, pss.pid, pss.versus_rating, pss.versus_won, pss.versus_plays, pss.stat_date,
                       CASE WHEN pss.versus_plays > 0 THEN (pss.versus_won * 100.0 / pss.versus_plays) ELSE 0 END as win_rate
                FROM player p 
                JOIN player_stats_snapshot pss ON p.pid = pss.pid
            """
            
            # 添加搜索条件
            where_conditions = []
            params = []
            
            # 获取最新日期的数据
            cursor.execute("SELECT MAX(stat_date) FROM player_stats_snapshot")
            latest_date = cursor.fetchone()[0]
            if latest_date:
                where_conditions.append("pss.stat_date = ?")
                params.append(latest_date)
            
            if search:
                where_conditions.append("(p.name LIKE ? OR pss.pid LIKE ?)")
                params.extend([f'%{search}%', f'%{search}%'])
            
            if where_conditions:
                base_query += " WHERE " + " AND ".join(where_conditions)
            
            # 添加排序 - 增加胜率排序支持
            valid_sort_columns = ['versus_rating', 'versus_won', 'versus_plays', 'name', 'win_rate']
            if sort_by not in valid_sort_columns:
                sort_by = 'versus_rating'
            
            if sort_order.lower() not in ['asc', 'desc']:
                sort_order = 'desc'
            
            order_query = f" ORDER BY {sort_by} {sort_order.upper()}"
            if sort_by != 'name':
                order_query += ", p.name ASC"
            
            # 如果有排名过滤，需要先获取完整排序结果
            if rank_filter:
                # 获取完整排序的数据用于排名过滤
                full_query = base_query + order_query
                cursor.execute(full_query, params)
                all_results = cursor.fetchall()
                
                # 应用排名过滤
                if rank_filter == 'top10':
                    filtered_results = all_results[:10]
                elif rank_filter == 'top25':
                    filtered_results = all_results[:25]
                elif rank_filter == 'top50':
                    filtered_results = all_results[:50]
                elif rank_filter == 'top100':
                    filtered_results = all_results[:100]
                else:
                    filtered_results = all_results
                
                total_count = len(filtered_results)
                
                # 应用分页到过滤后的结果
                offset = (page - 1) * per_page
                results = filtered_results[offset:offset + per_page]
            else:
                # 获取总数
                count_query = f"SELECT COUNT(*) FROM ({base_query}) as subquery"
                cursor.execute(count_query, params)
                total_count = cursor.fetchone()[0]
                
                # 添加分页
                offset = (page - 1) * per_page
                paginated_query = base_query + order_query + " LIMIT ? OFFSET ?"
                params.extend([per_page, offset])
                
                # 执行查询
                cursor.execute(paginated_query, params)
                results = cursor.fetchall()
                all_results = None
            
            conn.close()
        
        # 格式化数据
        players_data = []
        
        if rank_filter and all_results:
            # 对于排名过滤，排名就是在过滤结果中的位置
            for i, row in enumerate(results):
                name, pid, rating, won, plays, stat_date, win_rate = row
                # 计算在完整排序中的实际排名
                actual_rank = i + 1
                for j, full_row in enumerate(all_results):
                    if full_row[1] == pid:  # 比较pid
                        actual_rank = j + 1
                        break
                        
                players_data.append({
                    'name': name,
                    'pid': pid,
                    'versus_rating': rating,
                    'versus_won': won,
                    'versus_plays': plays,
                    'win_rate': round(win_rate, 2),
                    'stat_date': stat_date,
                    'rank': actual_rank
                })
        else:
            # 常规分页，计算页面排名
            base_rank = (page - 1) * per_page + 1
            for i, row in enumerate(results):
                name, pid, rating, won, plays, stat_date, win_rate = row
                actual_rank = base_rank + i
                    
                players_data.append({
                    'name': name,
                    'pid': pid,
                    'versus_rating': rating,
                    'versus_won': won,
                    'versus_plays': plays,
                    'win_rate': round(win_rate, 2),
                    'stat_date': stat_date,
                    'rank': actual_rank
                })
        
        # 计算分页信息
        total_pages = (total_count + per_page - 1) // per_page
        
        return jsonify({
            'players': players_data,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_count': total_count,
                'total_pages': total_pages,
                'has_next': page < total_pages,
                'has_prev': page > 1
            },
            'filters': {
                'sort_by': sort_by,
                'sort_order': sort_order,
                'search': search,
                'rank_filter': rank_filter
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 新API：获取排名统计信息
@app.route('/api/ranking-stats')
def get_ranking_stats():
    try:
        # 使用DatabaseAdapter处理数据库连接
        if db.is_s3:
            # S3数据库查询
            # 获取最新日期
            latest_date_query = "SELECT MAX(stat_date) FROM player_stats_snapshot"
            latest_date_result = db.db.execute_query(latest_date_query)
            latest_date = latest_date_result[0][0] if latest_date_result and latest_date_result[0] else None
            
            # 获取总玩家数
            stats_query = """
                SELECT COUNT(*) as total_players,
                       AVG(pss.versus_rating) as avg_rating,
                       AVG(CASE WHEN pss.versus_plays > 0 THEN (pss.versus_won * 100.0 / pss.versus_plays) ELSE 0 END) as avg_win_rate,
                       SUM(pss.versus_won) as total_wins,
                       SUM(pss.versus_plays) as total_plays
                FROM player p 
                JOIN player_stats_snapshot pss ON p.pid = pss.pid
                WHERE pss.stat_date = ?
            """
            stats_result = db.db.execute_query(stats_query, (latest_date,))
            stats = stats_result[0] if stats_result else (0, 0, 0, 0, 0)
            total_players, avg_rating, avg_win_rate, total_wins, total_plays = stats
            
            # 获取分数分布
            rating_dist_query = """
                SELECT 
                    COUNT(CASE WHEN pss.versus_rating >= 5000 THEN 1 END) as rating_5000_plus,
                    COUNT(CASE WHEN pss.versus_rating >= 4000 AND pss.versus_rating < 5000 THEN 1 END) as rating_4000_4999,
                    COUNT(CASE WHEN pss.versus_rating >= 3000 AND pss.versus_rating < 4000 THEN 1 END) as rating_3000_3999,
                    COUNT(CASE WHEN pss.versus_rating >= 2000 AND pss.versus_rating < 3000 THEN 1 END) as rating_2000_2999,
                    COUNT(CASE WHEN pss.versus_rating < 2000 THEN 1 END) as rating_under_2000
                FROM player p 
                JOIN player_stats_snapshot pss ON p.pid = pss.pid
                WHERE pss.stat_date = ?
            """
            rating_dist_result = db.db.execute_query(rating_dist_query, (latest_date,))
            rating_distribution = rating_dist_result[0] if rating_dist_result else (0, 0, 0, 0, 0)
            
            # 获取胜率分布
            winrate_dist_query = """
                SELECT 
                    COUNT(CASE WHEN (pss.versus_won * 100.0 / pss.versus_plays) >= 80 THEN 1 END) as winrate_80_plus,
                    COUNT(CASE WHEN (pss.versus_won * 100.0 / pss.versus_plays) >= 60 AND (pss.versus_won * 100.0 / pss.versus_plays) < 80 THEN 1 END) as winrate_60_79,
                    COUNT(CASE WHEN (pss.versus_won * 100.0 / pss.versus_plays) >= 40 AND (pss.versus_won * 100.0 / pss.versus_plays) < 60 THEN 1 END) as winrate_40_59,
                    COUNT(CASE WHEN (pss.versus_won * 100.0 / pss.versus_plays) >= 20 AND (pss.versus_won * 100.0 / pss.versus_plays) < 40 THEN 1 END) as winrate_20_39,
                    COUNT(CASE WHEN (pss.versus_won * 100.0 / pss.versus_plays) < 20 THEN 1 END) as winrate_under_20
                FROM player p 
                JOIN player_stats_snapshot pss ON p.pid = pss.pid
                WHERE pss.stat_date = ? AND pss.versus_plays > 0
            """
            winrate_dist_result = db.db.execute_query(winrate_dist_query, (latest_date,))
            winrate_distribution = winrate_dist_result[0] if winrate_dist_result else (0, 0, 0, 0, 0)
        else:
            # 本地数据库连接
            import sqlite3
            conn = sqlite3.connect('mario_filtered.db')
            cursor = conn.cursor()
            
            # 获取最新日期
            cursor.execute("SELECT MAX(stat_date) FROM player_stats_snapshot")
            latest_date = cursor.fetchone()[0]
            
            # 获取总玩家数
            cursor.execute("""
                SELECT COUNT(*) as total_players,
                       AVG(pss.versus_rating) as avg_rating,
                       AVG(CASE WHEN pss.versus_plays > 0 THEN (pss.versus_won * 100.0 / pss.versus_plays) ELSE 0 END) as avg_win_rate,
                       SUM(pss.versus_won) as total_wins,
                       SUM(pss.versus_plays) as total_plays
                FROM player p 
                JOIN player_stats_snapshot pss ON p.pid = pss.pid
                WHERE pss.stat_date = ?
            """, (latest_date,))
            
            stats = cursor.fetchone()
            total_players, avg_rating, avg_win_rate, total_wins, total_plays = stats
            
            # 获取分数分布
            cursor.execute("""
                SELECT 
                    COUNT(CASE WHEN pss.versus_rating >= 5000 THEN 1 END) as rating_5000_plus,
                    COUNT(CASE WHEN pss.versus_rating >= 4000 AND pss.versus_rating < 5000 THEN 1 END) as rating_4000_4999,
                    COUNT(CASE WHEN pss.versus_rating >= 3000 AND pss.versus_rating < 4000 THEN 1 END) as rating_3000_3999,
                    COUNT(CASE WHEN pss.versus_rating >= 2000 AND pss.versus_rating < 3000 THEN 1 END) as rating_2000_2999,
                    COUNT(CASE WHEN pss.versus_rating < 2000 THEN 1 END) as rating_under_2000
                FROM player p 
                JOIN player_stats_snapshot pss ON p.pid = pss.pid
                WHERE pss.stat_date = ?
            """, (latest_date,))
            
            rating_distribution = cursor.fetchone()
            
            # 获取胜率分布
            cursor.execute("""
                SELECT 
                    COUNT(CASE WHEN (pss.versus_won * 100.0 / pss.versus_plays) >= 80 THEN 1 END) as winrate_80_plus,
                    COUNT(CASE WHEN (pss.versus_won * 100.0 / pss.versus_plays) >= 60 AND (pss.versus_won * 100.0 / pss.versus_plays) < 80 THEN 1 END) as winrate_60_79,
                    COUNT(CASE WHEN (pss.versus_won * 100.0 / pss.versus_plays) >= 40 AND (pss.versus_won * 100.0 / pss.versus_plays) < 60 THEN 1 END) as winrate_40_59,
                    COUNT(CASE WHEN (pss.versus_won * 100.0 / pss.versus_plays) >= 20 AND (pss.versus_won * 100.0 / pss.versus_plays) < 40 THEN 1 END) as winrate_20_39,
                    COUNT(CASE WHEN (pss.versus_won * 100.0 / pss.versus_plays) < 20 THEN 1 END) as winrate_under_20
                FROM player p 
                JOIN player_stats_snapshot pss ON p.pid = pss.pid
                WHERE pss.stat_date = ? AND pss.versus_plays > 0
            """, (latest_date,))
            
            winrate_distribution = cursor.fetchone()
            
            conn.close()
        
        return jsonify({
            'success': True,
            'data': {
                'total_players': total_players,
                'avg_rating': round(avg_rating, 2) if avg_rating else 0,
                'avg_win_rate': round(avg_win_rate, 2) if avg_win_rate else 0,
                'total_wins': total_wins,
                'total_plays': total_plays,
                'latest_date': latest_date,
                'rating_distribution': {
                    '5000+': rating_distribution[0],
                    '4000-4999': rating_distribution[1],
                    '3000-3999': rating_distribution[2],
                    '2000-2999': rating_distribution[3],
                    'Under 2000': rating_distribution[4]
                },
                'winrate_distribution': {
                    '80%+': winrate_distribution[0],
                    '60-79%': winrate_distribution[1],
                    '40-59%': winrate_distribution[2],
                    '20-39%': winrate_distribution[3],
                    'Under 20%': winrate_distribution[4]
                }
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 保持向后兼容的CSV数据读取（如果数据库中没有数据）
def read_csv_data(player_id):
    """读取CSV文件数据作为后备方案"""
    try:
        csv_path = os.path.join('data', f'{player_id}.csv')
        if os.path.exists(csv_path):
            data = []
            with open(csv_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    data.append(row)
            return data
    except Exception as e:
        print(f"Error reading CSV for {player_id}: {e}")
    return []

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000) 