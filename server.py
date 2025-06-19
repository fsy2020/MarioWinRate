from flask import Flask, jsonify, send_from_directory, request
from flask_cors import CORS
import os
import json
import csv
from database import MarioDatabase

app = Flask(__name__)
CORS(app)

# 初始化数据库
db = MarioDatabase()

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