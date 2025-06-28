# Super Mario Maker 2 数据统计系统

这是一个专为 Super Mario Maker 2 多人对战模式设计的数据统计和分析系统，可以追踪玩家的游戏表现，提供详细的统计分析和排行榜功能。

## ✨ 主要功能

- 🏆 **完整玩家数据表格** - 显示所有玩家的最新对战数据
- 🔍 **智能搜索和过滤** - 支持玩家名字和ID的实时搜索
- 📊 **多维度排序** - 支持按分数、胜利数、总局数和名字排序
- 🔄 **高性能分页** - 支持106,000+玩家数据的流畅浏览
- 👤 **玩家详情分析** - 点击玩家名称查看详细统计和图表

## 技术架构

### 后端
- **Flask** - Python Web框架
- **SQLite** - 数据库存储
  - `mario_stats.db` - 用户管理和日常统计
  - `mario_filtered.db` - 大规模玩家数据快照

### 前端
- **原生JavaScript** - 无框架依赖的纯JavaScript
- **Chart.js** - 数据可视化图表库
- **CSS3** - 现代化的响应式样式
- **Font Awesome** - 图标库

## 安装和运行

### 环境要求
- Python 3.7+
- Flask
- Flask-CORS

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd MarioWinRate
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动服务器**
```bash
python server.py
```

4. **访问应用**
- 主页: http://localhost:5001/
- 管理面板: http://localhost:5001/admin.html

## API 接口

### 核心接口

#### 玩家数据快照
```http
GET /api/player-stats-snapshot
```

#### 用户统计数据
```http
GET /api/user/{user_id}/stats
```

#### 搜索玩家
```http
GET /api/search-players?q={query}
```

#### 最新统计数据
```http
GET /api/latest-stats
```

## 数据库结构

### mario_stats.db
- `users` - 用户信息表
- `daily_stats` - 每日统计表

### mario_filtered.db
- `player` - 玩家基本信息 (pid, name)
- `player_stats_snapshot` - 玩家数据快照
- `player_stats_delta` - 数据变化记录
