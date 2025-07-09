// 国际化配置
const i18n = {
    currentLanguage: 'en',
    translations: {
        'en': {
            'page-title': 'Super Mario Maker 2 Statistics',
            'page-subtitle': 'Track your multiplayer versus game performance, view rankings and data analysis',
            'search-placeholder': 'Search player name or ID...',
            'sort-rating': 'Sort by Rating',
            'sort-winrate': 'Sort by Win Rate',
            'sort-wins': 'Sort by Wins',
            'sort-plays': 'Sort by Total Games',
            'sort-name': 'Sort by Name',
            'order-desc': 'Descending',
            'order-asc': 'Ascending',
            'filter-all': 'All Rankings',
            'filter-top10': 'Top 10',
            'filter-top25': 'Top 25',
            'filter-top50': 'Top 50',
            'filter-top100': 'Top 100',
            'per-page-suffix': '/page',
            'ranking-stats': 'Ranking Statistics',
            'total-players': 'Total Players',
            'avg-rating': 'Average Rating',
            'avg-winrate': 'Average Win Rate',
            'total-wins': 'Total Wins',
            'loading': 'Loading data...',
            'loading-page': 'Loading Statistics...',
            'loading-subtext': 'Please wait, preparing your game statistics',
            'rank': 'Rank',
            'player-name': 'Player Name',
            'rating': 'Rating',
            'wins': 'Wins',
            'total-plays': 'Total Games',
            'win-rate': 'Win Rate',
            'data-date': 'Data Date',
            'player-details': 'Player Details',
            'current-rating': 'Current Rating',
            'overall-winrate': 'Overall Win Rate',
            'total-games': 'Total Games',
            'data-charts': 'Data Charts',
            'daily-stats': 'Daily Statistics',
            'rating-trend': 'Rating Trend',
            'winrate-trend': 'Win Rate Trend',
            'leaderboard': 'Leaderboard',
            'winrate-ranking': 'Win Rate Ranking',
            'rating-ranking': 'Rating Ranking',
            'error-loading': 'Error loading data',
            'page-info': 'Page {current} of {total} ({count} total records)'
        },
        'zh-CN': {
            'page-title': 'Super Mario Maker 2数据统计',
            'page-subtitle': '追踪你的多人对战游戏表现，查看排名和数据分析',
            'search-placeholder': '搜索玩家名称或ID...',
            'sort-rating': '按分数排序',
            'sort-winrate': '按胜率排序',
            'sort-wins': '按胜利数排序',
            'sort-plays': '按总局数排序',
            'sort-name': '按名称排序',
            'order-desc': '降序',
            'order-asc': '升序',
            'filter-all': '所有排名',
            'filter-top10': '前10名',
            'filter-top25': '前25名',
            'filter-top50': '前50名',
            'filter-top100': '前100名',
            'per-page-suffix': '条/页',
            'ranking-stats': '排名统计',
            'total-players': '总玩家数',
            'avg-rating': '平均分数',
            'avg-winrate': '平均胜率',
            'total-wins': '总胜利数',
            'loading': '正在加载数据...',
            'loading-page': '正在加载统计数据...',
            'loading-subtext': '请稍候，正在准备您的游戏统计数据',
            'rank': '排名',
            'player-name': '玩家名称',
            'rating': '分数',
            'wins': '胜利数',
            'total-plays': '总局数',
            'win-rate': '胜率',
            'data-date': '数据日期',
            'player-details': '玩家详情',
            'current-rating': '当前分数',
            'overall-winrate': '总胜率',
            'total-games': '总游戏数',
            'data-charts': '数据图表',
            'daily-stats': '每日统计',
            'rating-trend': '分数趋势',
            'winrate-trend': '胜率趋势',
            'leaderboard': '排行榜',
            'winrate-ranking': '胜率排名',
            'rating-ranking': '分数排名',
            'error-loading': '加载数据时出现错误',
            'page-info': '第 {current} 页，共 {total} 页 (总计 {count} 条记录)'
        },
        'ja': {
            'page-title': 'Super Mario Maker 2統計',
            'page-subtitle': 'マルチプレイ対戦ゲームのパフォーマンスを追跡し、ランキングとデータ分析を表示',
            'search-placeholder': 'プレイヤー名またはIDを検索...',
            'sort-rating': 'レーティング順',
            'sort-winrate': '勝率順',
            'sort-wins': '勝利数順',
            'sort-plays': '総ゲーム数順',
            'sort-name': '名前順',
            'order-desc': '降順',
            'order-asc': '昇順',
            'filter-all': '全ランキング',
            'filter-top10': 'トップ10',
            'filter-top25': 'トップ25',
            'filter-top50': 'トップ50',
            'filter-top100': 'トップ100',
            'per-page-suffix': '件/ページ',
            'ranking-stats': 'ランキング統計',
            'total-players': '総プレイヤー数',
            'avg-rating': '平均レーティング',
            'avg-winrate': '平均勝率',
            'total-wins': '総勝利数',
            'loading': 'データを読み込み中...',
            'loading-page': '統計データを読み込み中...',
            'loading-subtext': 'お待ちください、ゲーム統計データを準備しています',
            'rank': 'ランク',
            'player-name': 'プレイヤー名',
            'rating': 'レーティング',
            'wins': '勝利数',
            'total-plays': '総ゲーム数',
            'win-rate': '勝率',
            'data-date': 'データ日付',
            'player-details': 'プレイヤー詳細',
            'current-rating': '現在のレーティング',
            'overall-winrate': '総合勝率',
            'total-games': '総ゲーム数',
            'data-charts': 'データチャート',
            'daily-stats': '日別統計',
            'rating-trend': 'レーティング推移',
            'winrate-trend': '勝率推移',
            'leaderboard': 'リーダーボード',
            'winrate-ranking': '勝率ランキング',
            'rating-ranking': 'レーティングランキング',
            'error-loading': 'データの読み込みエラー',
            'page-info': 'ページ {current} / {total} (合計 {count} 件)'
        }
    }
};

// 将i18n设置为全局变量，以便HTML中的内联脚本可以访问
window.i18n = i18n;

// 国际化相关函数
function t(key) {
    return i18n.translations[i18n.currentLanguage][key] || key;
}

function updateLanguageDisplay() {
    const languageLabels = {
        'en': 'EN',
        'zh-CN': '中',
        'ja': '日'
    };
    document.getElementById('currentLanguage').textContent = languageLabels[i18n.currentLanguage];
    
    // 更新页面语言属性
    document.documentElement.lang = i18n.currentLanguage;
    
    // 更新页面标题
    document.title = t('page-title');
    
    // 更新所有带有 data-i18n 属性的元素
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        element.textContent = t(key);
    });
    
    // 更新占位符文本
    document.querySelectorAll('[data-i18n-placeholder]').forEach(element => {
        const key = element.getAttribute('data-i18n-placeholder');
        element.placeholder = t(key);
    });
    
    // 更新选择器选项文本
    document.querySelectorAll('option[data-i18n]').forEach(option => {
        const key = option.getAttribute('data-i18n');
        option.textContent = t(key);
    });
    
    // 更新分页选项的后缀
    document.querySelectorAll('#perPageSelect option').forEach(option => {
        const value = option.value;
        option.innerHTML = value + t('per-page-suffix');
    });
    
    // 更新语言选项的显示状态 - 只显示其他语言
    document.querySelectorAll('.language-option').forEach(option => {
        const optionLang = option.getAttribute('data-lang');
        if (optionLang === i18n.currentLanguage) {
            option.style.display = 'none'; // 隐藏当前语言
        } else {
            option.style.display = 'flex'; // 显示其他语言
        }
    });
}

function changeLanguage(language) {
    i18n.currentLanguage = language;
    localStorage.setItem('language', language);
    updateLanguageDisplay();
    
    // 更新动态生成的内容
    updateDynamicContent();
    
    // 如果有图表需要更新，重新绘制
    if (currentChart) {
        const player = currentChart.player;
        const chartType = document.querySelector('.chart-tab-btn.active').getAttribute('data-chart');
        switchChartTab(chartType);
    }
}

function updateDynamicContent() {
    // 更新排行榜标签（如果存在）
    const rankingTabs = document.querySelectorAll('.tab-btn');
    rankingTabs.forEach(btn => {
        const tabType = btn.getAttribute('data-tab');
        if (tabType === 'winrate') {
            btn.textContent = t('winrate-ranking');
        } else if (tabType === 'rating') {
            btn.textContent = t('rating-ranking');
        }
    });
    
    // 更新排行榜标题（如果存在）
    const leaderboardTitle = document.querySelector('.podium-section h2');
    if (leaderboardTitle) {
        leaderboardTitle.innerHTML = `<i class="fas fa-trophy"></i> ${t('leaderboard')}`;
    }
    
    // 更新加载文本（如果正在加载）
    const loadingText = document.querySelector('.loading p');
    if (loadingText) {
        loadingText.textContent = t('loading');
    }
    
    // 更新全页面加载状态文本
    const pageLoadingText = document.querySelector('.page-loading-text');
    const pageLoadingSubtext = document.querySelector('.page-loading-subtext');
    if (pageLoadingText) {
        pageLoadingText.textContent = t('loading-page');
    }
    if (pageLoadingSubtext) {
        pageLoadingSubtext.textContent = t('loading-subtext');
    }
    
    // 更新PlayersDataViewer的加载状态（如果存在）
    if (window.playersDataViewer && typeof window.playersDataViewer.updateLoadingText === 'function') {
        window.playersDataViewer.updateLoadingText();
    }
    
    // 更新分页显示（如果存在）
    if (window.playersDataViewer && typeof window.playersDataViewer.refreshPagination === 'function') {
        window.playersDataViewer.refreshPagination();
    }
}

function initializeLanguageSwitcher() {
    // 从本地存储获取语言设置
    const savedLanguage = localStorage.getItem('language') || 'en';
    i18n.currentLanguage = savedLanguage;
    
    const languageBtn = document.getElementById('languageBtn');
    const languageDropdown = document.getElementById('languageDropdown');
    
    // 语言按钮点击事件
    languageBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        languageDropdown.classList.toggle('show');
        languageBtn.classList.toggle('active');
    });
    
    // 语言选项点击事件
    document.querySelectorAll('.language-option').forEach(option => {
        option.addEventListener('click', function() {
            const language = this.getAttribute('data-lang');
            changeLanguage(language);
            languageDropdown.classList.remove('show');
            languageBtn.classList.remove('active');
        });
    });
    
    // 点击其他地方关闭下拉菜单
    document.addEventListener('click', function() {
        languageDropdown.classList.remove('show');
        languageBtn.classList.remove('active');
    });
    
    // 初始化语言显示
    updateLanguageDisplay();
}

// 全局变量
let playersData = {};
let currentChart = null;
let currentRankingType = 'winrate'; // 'rating' 或 'winrate'
let playerNameMapping = {}; // 存储玩家ID到名字的映射

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeLanguageSwitcher();
    loadPlayersData();
    initializeEventListeners();
    
    // 确保初始状态下没有布局容器
    cleanupPlayerLayout();
});

// 清理玩家布局容器
function cleanupPlayerLayout() {
    const existingLayout = document.querySelector('.player-content-layout');
    if (existingLayout) {
        const playerDetails = document.getElementById('playerDetails');
        const chartsSection = document.getElementById('chartsSection');
        
        // 将元素移回原来的位置
        const container = document.querySelector('.container');
        container.appendChild(playerDetails);
        container.appendChild(chartsSection);
        
        // 移除布局容器
        existingLayout.remove();
        
        // 隐藏元素
        playerDetails.style.display = 'none';
        chartsSection.style.display = 'none';
    }
}

// 初始化事件监听器
function initializeEventListeners() {
    // 排名标签切换
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabType = this.getAttribute('data-tab');
            switchRankingTab(tabType);
        });
    });
    
    // 图表标签切换
    const chartTabBtns = document.querySelectorAll('.chart-tab-btn');
    chartTabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const chartType = this.getAttribute('data-chart');
            switchChartTab(chartType);
        });
    });
}

// 加载玩家数据
async function loadPlayersData() {
    try {
        // 显示加载动画
        showLoading();
        
        // 首先加载玩家名字映射
        await loadPlayerNameMapping();
        
        // 获取所有CSV文件列表
        const csvFiles = await fetchCSVFilesList();
        
        // 加载每个玩家的数据
        for (const file of csvFiles) {
            const playerId = file.replace('.csv', '');
            const playerData = await loadPlayerData(playerId);
            if (playerData) {
                playersData[playerId] = playerData;
            }
        }
        
        // 恢复podium界面并初始化排名
        hideLoading();
        updateRanking();
        
    } catch (error) {
        console.error('加载数据失败:', error);
        hideLoading();
    }
}

// 加载玩家名字映射
async function loadPlayerNameMapping() {
    try {
        const response = await fetch('/api/player-names');
        if (response.ok) {
            const data = await response.json();
            playerNameMapping = data.nameMapping || {};
        } else {
            throw new Error('API调用失败');
        }
    } catch (error) {
        console.error('加载玩家名字映射失败:', error);
        console.log('使用后备名字映射');
        // 使用后备的静态名字映射
        playerNameMapping = {
            'Y9P7BN4JF': 'Panzi°',
            'SQW0796SF': 'yuan☆',
            'GDH8R4V4G': 'Chenfeng!',
            'D221SPHLF': 'BuBuLine',
            'Q5MBL99QG': 'DY_XiaoJie',
            '4QVF9V6RF': 'ΒOチ',
            'D049HCB8G': 'Sister♪',
            '1VVRCXQPF': 'ただのpiyo',
            'D8CJ2W62H': 'Nxs Syo。',
            'LDMLC6RLG': '∞マジシャンΚ∞',
            '0JR5R5BJG': '【MC×】Selen',
            '08VW66RLF': '⊂●Mr.クロス●⊃',
            '0MMCG9V4G': 'Panzi\'',
            '7CPDNC72G': 'CN★ΜPlayer',
            '135CFSJTG': 'MPlayerAlt',
            '66NT81CTF': 'buhuai008',
            'XDL02BC6G': 'Yangcilang',
            'BSHMC4PKF': 'yuan dian',
            'S52QN7JXF': '†™†'
        };
    }
}

// 获取玩家显示名称
function getPlayerDisplayName(playerId) {
    return playerNameMapping[playerId] || playerId;
}

// 获取玩家ID（用于搜索）
function getPlayerIdByName(playerName) {
    for (const [id, name] of Object.entries(playerNameMapping)) {
        if (name.toLowerCase().includes(playerName.toLowerCase())) {
            return id;
        }
    }
    return playerName; // 如果没找到，假设输入的就是ID
}

// 获取CSV文件列表
async function fetchCSVFilesList() {
    try {
        const response = await fetch('/api/files');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data = await response.json();
        return data.files;
    } catch (error) {
        console.error('获取文件列表失败:', error);
        // 如果API失败，使用备用列表
        return [
            'LDMLC6RLG.csv', '08VW66RLF.csv', '4QVF9V6RF.csv', 
            '66NT81CTF.csv', 'Q5MBL99QG.csv', 'D8CJ2W62H.csv',
            'Y9P7BN4JF.csv', 'SQW0796SF.csv', 'D221SPHLF.csv'
        ];
    }
}

// 加载单个玩家数据
async function loadPlayerData(playerId) {
    try {
        const response = await fetch(`data/${playerId}.csv`);
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        const csvText = await response.text();
        return parseCSVData(csvText, playerId);
    } catch (error) {
        console.error(`加载玩家 ${playerId} 数据失败:`, error);
        return null;
    }
}

// 解析CSV数据
function parseCSVData(csvText, playerId) {
    const lines = csvText.trim().split('\n');
    const headers = lines[0].split(',');
    const data = [];
    
    for (let i = 1; i < lines.length; i++) {
        const values = lines[i].split(',');
        const row = {};
        headers.forEach((header, index) => {
            row[header.trim()] = values[index] ? values[index].trim() : '';
        });
        data.push(row);
    }
    
    // 计算统计数据
    const latestData = data[data.length - 1];
    const totalWins = parseInt(latestData.wins_total) || 0;
    const totalPlays = parseInt(latestData.plays_total) || 0;
    const currentRating = parseInt(latestData.rate) || 0;
    const overallWinRate = totalPlays > 0 ? (totalWins / totalPlays * 100).toFixed(2) : 0;
    
    return {
        playerId: playerId,
        playerName: getPlayerDisplayName(playerId), // 使用真实姓名
        data: data,
        stats: {
            totalWins: totalWins,
            totalPlays: totalPlays,
            currentRating: currentRating,
            overallWinRate: parseFloat(overallWinRate)
        }
    };
}

// 选择玩家
function selectPlayer(playerId) {
    const player = playersData[playerId];
    if (!player) return;

    // 显示玩家详情
    showPlayerDetails(player);
    showPlayerCharts(player);
    
    // 滚动到玩家详情
    document.getElementById('playerDetails').scrollIntoView({ behavior: 'smooth' });
}

// 显示玩家详情
function showPlayerDetails(player) {
    const playerDetails = document.getElementById('playerDetails');
    const playerNameDisplay = document.getElementById('playerNameDisplay');
    const chartsSection = document.getElementById('chartsSection');
    const stats = player.stats;
    
    // 显示玩家名字
    playerNameDisplay.textContent = getPlayerDisplayName(player.playerId);
    
    document.getElementById('totalWins').textContent = stats.totalWins.toLocaleString();
    document.getElementById('totalPlays').textContent = stats.totalPlays.toLocaleString();
    document.getElementById('overallWinRate').textContent = stats.overallWinRate + '%';
    document.getElementById('currentRating').textContent = stats.currentRating.toLocaleString();
    
    // 创建组合布局容器
    if (!document.querySelector('.player-content-layout')) {
        const layoutContainer = document.createElement('div');
        layoutContainer.className = 'player-content-layout';
        
        // 将玩家详情和图表放入布局容器
        const container = document.querySelector('.container');
        container.appendChild(layoutContainer);
        layoutContainer.appendChild(playerDetails);
        layoutContainer.appendChild(chartsSection);
    }
    
    playerDetails.style.display = 'block';
}

// 显示玩家图表
function showPlayerCharts(player) {
    const chartsSection = document.getElementById('chartsSection');
    chartsSection.style.display = 'block';
    
    // 默认显示每日统计图表
    drawDailyStatsChart(player);
}

// 切换排名标签
function switchRankingTab(tabType) {
    currentRankingType = tabType;
    
    // 更新标签样式
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-tab') === tabType) {
            btn.classList.add('active');
        }
    });
    
    // 更新排名
    updateRanking();
}

// 更新排名显示
function updateRanking() {
    const players = Object.values(playersData);
    if (players.length === 0) return;
    
    // 根据排名类型排序
    let sortedPlayers;
    if (currentRankingType === 'winrate') {
        sortedPlayers = players
            .filter(p => p.stats.totalPlays >= 100) // 至少100局游戏才参与胜率排名
            .sort((a, b) => b.stats.overallWinRate - a.stats.overallWinRate);
    } else {
        sortedPlayers = players.sort((a, b) => b.stats.currentRating - a.stats.currentRating);
    }
    
    // 更新颁奖台
    updatePodium(sortedPlayers);
    
    // 更新完整排名列表
    updateFullRanking(sortedPlayers);
}

// 更新颁奖台
function updatePodium(sortedPlayers) {
    const positions = ['first-place', 'second-place', 'third-place'];
    
    positions.forEach((positionId, index) => {
        const element = document.getElementById(positionId);
        const player = sortedPlayers[index];
        
        if (player) {
            const nameElement = element.querySelector('.player-name');
            const statsElement = element.querySelector('.player-stats');
            
            nameElement.textContent = getPlayerDisplayName(player.playerId);
            
            if (currentRankingType === 'winrate') {
                statsElement.textContent = `胜率: ${player.stats.overallWinRate}%`;
            } else {
                statsElement.textContent = `分数: ${player.stats.currentRating.toLocaleString()}`;
            }
        } else {
            const nameElement = element.querySelector('.player-name');
            const statsElement = element.querySelector('.player-stats');
            nameElement.textContent = '-';
            statsElement.textContent = '-';
        }
    });
}

// 更新完整排名列表
function updateFullRanking(sortedPlayers) {
    const rankingList = document.getElementById('rankingList');
    
    const rankingHTML = sortedPlayers.map((player, index) => {
        const statValue = currentRankingType === 'winrate' 
            ? `${player.stats.overallWinRate}%` 
            : player.stats.currentRating.toLocaleString();
        
        const statLabel = currentRankingType === 'winrate' ? '胜率' : '分数';
        const playerDisplayName = getPlayerDisplayName(player.playerId);
        
        return `
            <div class="ranking-item" onclick="selectPlayer('${player.playerId}')">
                <div class="rank-number">${index + 1}</div>
                <div class="rank-info">
                    <div class="rank-name">${playerDisplayName}</div>
                    <div class="rank-stats">
                        ${statLabel}: ${statValue} | 
                        胜利: ${player.stats.totalWins.toLocaleString()} | 
                        总局: ${player.stats.totalPlays.toLocaleString()}
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    rankingList.innerHTML = rankingHTML;
}

// 切换图表标签
function switchChartTab(chartType) {
    // 更新标签样式
    document.querySelectorAll('.chart-tab-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.getAttribute('data-chart') === chartType) {
            btn.classList.add('active');
        }
    });
    
    // 获取当前显示的玩家
    const playerNameDisplay = document.getElementById('playerNameDisplay');
    if (!playerNameDisplay || !playerNameDisplay.textContent || playerNameDisplay.textContent === '') {
        return; // 没有选中的玩家
    }
    
    let selectedPlayer = null;
    
    // 通过显示的名字查找玩家
    for (const [playerId, player] of Object.entries(playersData)) {
        if (getPlayerDisplayName(playerId) === playerNameDisplay.textContent) {
            selectedPlayer = player;
            break;
        }
    }
    
    if (!selectedPlayer) return;
    
    // 根据图表类型绘制相应图表
    switch (chartType) {
        case 'dailyStats':
            drawDailyStatsChart(selectedPlayer);
            break;
        case 'ratingTrend':
            drawRatingTrendChart(selectedPlayer);
            break;
        case 'winRateTrend':
            drawWinRateTrendChart(selectedPlayer);
            break;
    }
}

// 绘制每日统计图表
function drawDailyStatsChart(player) {
    const ctx = document.getElementById('mainChart');
    
    if (currentChart) {
        currentChart.destroy();
    }
    
    const data = player.data.slice(-30); // 最近30天
    const labels = data.map(d => d.time ? d.time.split(' ')[0] : '');
    const wins = data.map(d => parseInt(d.wins) || 0);
    const plays = data.map(d => parseInt(d.plays) || 0);
    
    // 多语言图表标签
    const chartLabels = {
        'en': {
            winsLabel: 'Daily Wins',
            playsLabel: 'Daily Games',
            title: 'Daily Game Statistics (Last 30 Days)'
        },
        'zh-CN': {
            winsLabel: '每日胜利数',
            playsLabel: '每日游戏数',
            title: '最近30天每日游戏统计'
        },
        'ja': {
            winsLabel: '日別勝利数',
            playsLabel: '日別ゲーム数',
            title: '過去30日間の日別ゲーム統計'
        }
    };
    
    const labels_i18n = chartLabels[i18n.currentLanguage];
    
    currentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: labels_i18n.winsLabel,
                    data: wins,
                    backgroundColor: 'rgba(255, 215, 0, 0.8)',
                    borderColor: 'rgba(255, 215, 0, 1)',
                    borderWidth: 1
                },
                {
                    label: labels_i18n.playsLabel,
                    data: plays,
                    backgroundColor: 'rgba(102, 126, 234, 0.6)',
                    borderColor: 'rgba(102, 126, 234, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: labels_i18n.title,
                    font: { size: 16, weight: 'bold' }
                },
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                },
                x: {
                    ticks: {
                        maxTicksLimit: 10
                    }
                }
            }
        }
    });
    
    // 存储当前图表信息用于语言切换
    currentChart.player = player;
}

// 绘制分数趋势图表
function drawRatingTrendChart(player) {
    const ctx = document.getElementById('mainChart');
    
    if (currentChart) {
        currentChart.destroy();
    }
    
    const data = player.data.slice(-60); // 最近60天
    const labels = data.map(d => d.time ? d.time.split(' ')[0] : '');
    const ratings = data.map(d => parseInt(d.rate) || 0);
    
    // 多语言图表标签
    const chartLabels = {
        'en': {
            ratingLabel: 'Rating',
            title: 'Rating Trend (Last 60 Days)'
        },
        'zh-CN': {
            ratingLabel: '分数',
            title: '最近60天分数趋势'
        },
        'ja': {
            ratingLabel: 'レーティング',
            title: '過去60日間のレーティング推移'
        }
    };
    
    const labels_i18n = chartLabels[i18n.currentLanguage];
    
    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: labels_i18n.ratingLabel,
                data: ratings,
                borderColor: 'rgba(102, 126, 234, 1)',
                backgroundColor: 'rgba(102, 126, 234, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgba(102, 126, 234, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: labels_i18n.title,
                    font: { size: 16, weight: 'bold' }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: false,
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString();
                        }
                    }
                },
                x: {
                    ticks: {
                        maxTicksLimit: 10
                    }
                }
            }
        }
    });
    
    // 存储当前图表信息用于语言切换
    currentChart.player = player;
}

// 绘制胜率趋势图表
function drawWinRateTrendChart(player) {
    const ctx = document.getElementById('mainChart');
    
    if (currentChart) {
        currentChart.destroy();
    }
    
    const data = player.data.slice(-60); // 最近60天
    const labels = data.map(d => d.time ? d.time.split(' ')[0] : '');
    const winRates = data.map(d => {
        const rate = parseFloat(d.win_rate) || 0;
        return rate * 100; // 转换为百分比
    });
    
    // 多语言图表标签
    const chartLabels = {
        'en': {
            winRateLabel: 'Daily Win Rate (%)',
            title: 'Win Rate Trend (Last 60 Days)'
        },
        'zh-CN': {
            winRateLabel: '每日胜率 (%)',
            title: '最近60天胜率趋势'
        },
        'ja': {
            winRateLabel: '日別勝率 (%)',
            title: '過去60日間の勝率推移'
        }
    };
    
    const labels_i18n = chartLabels[i18n.currentLanguage];
    
    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: labels_i18n.winRateLabel,
                data: winRates,
                borderColor: 'rgba(255, 99, 132, 1)',
                backgroundColor: 'rgba(255, 99, 132, 0.1)',
                borderWidth: 3,
                fill: true,
                tension: 0.4,
                pointBackgroundColor: 'rgba(255, 99, 132, 1)',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 5
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: labels_i18n.title,
                    font: { size: 16, weight: 'bold' }
                },
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                },
                x: {
                    ticks: {
                        maxTicksLimit: 10
                    }
                }
            }
        }
    });
    
    // 存储当前图表信息用于语言切换
    currentChart.player = player;
}

// 显示加载动画
function showLoading() {
    const loadingHTML = `
        <h2><i class="fas fa-trophy"></i> ${t('leaderboard')}</h2>
        <div class="loading">
            <div class="spinner"></div>
            <p style="margin-top: 20px; color: #667eea;">${t('loading')}</p>
        </div>
    `;
    document.querySelector('.podium-section').innerHTML = loadingHTML;
}

// 隐藏加载动画并恢复原始内容
function hideLoading() {
    const podiumSection = document.querySelector('.podium-section');
    podiumSection.innerHTML = `
        <div class="podium-main-layout">
            <!-- 左侧内容 -->
            <div class="podium-left-content">
                <div>
                    <h2><i class="fas fa-trophy"></i> ${t('leaderboard')}</h2>
                    <div class="ranking-tabs">
                        <button class="tab-btn active" data-tab="winrate">${t('winrate-ranking')}</button>
                        <button class="tab-btn" data-tab="rating">${t('rating-ranking')}</button>
                    </div>
                </div>
                
                <div class="full-ranking">
                    <div class="ranking-list" id="rankingList"></div>
                </div>
            </div>
            
            <!-- 右侧颁奖台 -->
            <div class="podium-right-content">
                <div class="podium-container">
                    <div class="podium">
                        <div class="podium-place second">
                            <div class="podium-player" id="second-place">
                                <div class="medal silver"><i class="fas fa-medal"></i></div>
                                <div class="player-info">
                                    <div class="player-name">-</div>
                                    <div class="player-stats">-</div>
                                </div>
                            </div>
                            <div class="podium-base silver-base">2</div>
                        </div>
                        <div class="podium-place first">
                            <div class="podium-player" id="first-place">
                                <div class="medal gold"><i class="fas fa-crown"></i></div>
                                <div class="player-info">
                                    <div class="player-name">-</div>
                                    <div class="player-stats">-</div>
                                </div>
                            </div>
                            <div class="podium-base gold-base">1</div>
                        </div>
                        <div class="podium-place third">
                            <div class="podium-player" id="third-place">
                                <div class="medal bronze"><i class="fas fa-medal"></i></div>
                                <div class="player-info">
                                    <div class="player-name">-</div>
                                    <div class="player-stats">-</div>
                                </div>
                            </div>
                            <div class="podium-base bronze-base">3</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // 重新绑定事件监听器
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabType = this.getAttribute('data-tab');
            switchRankingTab(tabType);
        });
    });
}

// 新增：玩家历史数据相关函数
async function showPlayerHistoryModal(pid, playerName) {
    try {
        // 显示加载状态
        const modal = document.getElementById('playerHistoryModal');
        if (!modal) {
            createPlayerHistoryModal();
        }
        
        document.getElementById('playerHistoryModal').style.display = 'block';
        document.getElementById('historyPlayerName').textContent = playerName;
        document.getElementById('historyContent').innerHTML = '<div class="loading">Loading player history...</div>';
        
        // 获取玩家历史数据
        const response = await fetch(`/api/player-history/${pid}?days=30`);
        if (!response.ok) {
            throw new Error('Failed to fetch player history');
        }
        
        const data = await response.json();
        displayPlayerHistory(data);
        
    } catch (error) {
        console.error('Error loading player history:', error);
        document.getElementById('historyContent').innerHTML = '<div class="error">Error loading player history</div>';
    }
}

function createPlayerHistoryModal() {
    const modalHTML = `
        <div id="playerHistoryModal" class="modal">
            <div class="modal-content">
                <div class="modal-header">
                    <h2 id="historyPlayerName">Player History</h2>
                    <span class="close" onclick="closePlayerHistoryModal()">&times;</span>
                </div>
                <div id="historyContent" class="modal-body">
                    <!-- Content will be loaded here -->
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHTML);
    
    // 点击模态框外部关闭
    document.getElementById('playerHistoryModal').onclick = function(event) {
        if (event.target === this) {
            closePlayerHistoryModal();
        }
    };
}

function closePlayerHistoryModal() {
    document.getElementById('playerHistoryModal').style.display = 'none';
}

function displayPlayerHistory(data) {
    const { player, history, stats, days } = data;
    
    let historyHTML = `
        <div class="player-summary">
            <div class="summary-item">
                <label>Current Rating:</label>
                <span class="rating">${player.current_rating}</span>
            </div>
            <div class="summary-item">
                <label>Current Win Rate:</label>
                <span class="win-rate">${player.current_win_rate}%</span>
            </div>
            <div class="summary-item">
                <label>Total Games:</label>
                <span>${player.current_plays}</span>
            </div>
            <div class="summary-item">
                <label>Code:</label>
                <span>${player.code || 'N/A'}</span>
            </div>
        </div>
        
        <div class="history-tabs">
            <button class="tab-button active" onclick="showHistoryTab('table')">Data Table</button>
            <button class="tab-button" onclick="showHistoryTab('chart')">Performance Chart</button>
        </div>
        
        <div id="historyTable" class="tab-content active">
            <div class="stats-summary">
                <h3>${getI18nTextForModal('daily-stats-title', '30-Day Daily Performance Statistics')}</h3>
                <div class="stats-grid">
                    <div class="stat-item">
                        <label>Max Rating:</label>
                        <span>${stats.max_rating || 'N/A'}</span>
                    </div>
                    <div class="stat-item">
                        <label>Min Rating:</label>
                        <span>${stats.min_rating || 'N/A'}</span>
                    </div>
                    <div class="stat-item">
                        <label>Avg Rating:</label>
                        <span>${stats.avg_rating || 'N/A'}</span>
                    </div>
                    <div class="stat-item">
                        <label>Avg Win Rate:</label>
                        <span>${stats.avg_win_rate || 'N/A'}%</span>
                    </div>
                </div>
            </div>
            
            <div class="history-data-table">
                <table>
                    <thead>
                        <tr>
                            <th>${getI18nTextForModal('date', 'Date')}</th>
                            <th>${getI18nTextForModal('rating', 'Rating')}</th>
                            <th>${getI18nTextForModal('todays-wins', "Today's Wins")}</th>
                            <th>${getI18nTextForModal('todays-games', "Today's Games")}</th>
                            <th>${getI18nTextForModal('todays-winrate', "Today's Win Rate")}</th>
                        </tr>
                    </thead>
                    <tbody>
    `;
    
    // 计算每日的增量数据并显示
    history.forEach((record, index) => {
        // 修复日期显示 - 加1天
        const dateObj = new Date(record.created_at);
        dateObj.setDate(dateObj.getDate() + 1);
        const date = dateObj.toLocaleDateString();
        
        // 计算当日新增的wins和plays
        let dailyWins = 0;
        let dailyPlays = 0;
        
        if (index === 0) {
            // 最新一天（今天）：如果只有一条记录，显示累计值；如果有多条记录，计算与前一天的差值
            if (history.length === 1) {
                dailyWins = record.versus_won;
                dailyPlays = record.versus_plays;
            } else {
                const prevRecord = history[1];
                dailyWins = record.versus_won - prevRecord.versus_won;
                dailyPlays = record.versus_plays - prevRecord.versus_plays;
            }
        } else {
            // 历史数据：计算与下一条记录的差值
            if (index < history.length - 1) {
                const nextRecord = history[index + 1];
                dailyWins = record.versus_won - nextRecord.versus_won;
                dailyPlays = record.versus_plays - nextRecord.versus_plays;
            } else {
                // 最早的记录，显示累计值
                dailyWins = record.versus_won;
                dailyPlays = record.versus_plays;
            }
        }
        
        // 确保增量数据不为负数
        dailyWins = Math.max(0, dailyWins);
        dailyPlays = Math.max(0, dailyPlays);
        
        // 计算当日胜率
        const dailyWinRate = dailyPlays > 0 ? ((dailyWins / dailyPlays) * 100).toFixed(2) : 0;
        
        historyHTML += `
            <tr>
                <td>${date}</td>
                <td>${record.versus_rating}</td>
                <td>${dailyWins}</td>
                <td>${dailyPlays}</td>
                <td>${dailyWinRate}%</td>
            </tr>
        `;
    });
    
    historyHTML += `
                    </tbody>
                </table>
            </div>
        </div>
        
        <div id="historyChart" class="tab-content">
            <canvas id="playerHistoryChart" width="800" height="400"></canvas>
        </div>
    `;
    
    document.getElementById('historyContent').innerHTML = historyHTML;
    
    // 绘制图表
    drawPlayerHistoryChart(history);
}

function showHistoryTab(tabName) {
    // 更新标签按钮状态
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[onclick="showHistoryTab('${tabName}')"]`).classList.add('active');
    
    // 更新内容显示
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(tabName === 'chart' ? 'historyChart' : 'historyTable').classList.add('active');
}

function drawPlayerHistoryChart(history) {
    const canvas = document.getElementById('playerHistoryChart');
    const ctx = canvas.getContext('2d');
    
    // 清空画布
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    if (history.length === 0) {
        ctx.fillStyle = '#666';
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.fillText('No historical data available', canvas.width / 2, canvas.height / 2);
        return;
    }
    
    // 准备数据
    const ratings = history.map(h => h.versus_rating);
    const winRates = history.map(h => h.win_rate);
    const dates = history.map(h => new Date(h.created_at));
    
    // 计算图表区域
    const padding = 60;
    const chartWidth = canvas.width - 2 * padding;
    const chartHeight = canvas.height - 2 * padding;
    
    // 计算数据范围
    const minRating = Math.min(...ratings);
    const maxRating = Math.max(...ratings);
    const minWinRate = Math.min(...winRates);
    const maxWinRate = Math.max(...winRates);
    
    // 绘制坐标轴
    ctx.strokeStyle = '#ddd';
    ctx.lineWidth = 1;
    
    // X轴
    ctx.beginPath();
    ctx.moveTo(padding, canvas.height - padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();
    
    // Y轴 (左侧 - Rating)
    ctx.beginPath();
    ctx.moveTo(padding, padding);
    ctx.lineTo(padding, canvas.height - padding);
    ctx.stroke();
    
    // Y轴 (右侧 - Win Rate)
    ctx.beginPath();
    ctx.moveTo(canvas.width - padding, padding);
    ctx.lineTo(canvas.width - padding, canvas.height - padding);
    ctx.stroke();
    
    // 绘制Rating曲线
    ctx.strokeStyle = '#2196F3';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    ratings.forEach((rating, index) => {
        const x = padding + (index / (ratings.length - 1)) * chartWidth;
        const y = canvas.height - padding - ((rating - minRating) / (maxRating - minRating)) * chartHeight;
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.stroke();
    
    // 绘制Win Rate曲线
    ctx.strokeStyle = '#4CAF50';
    ctx.lineWidth = 2;
    ctx.beginPath();
    
    winRates.forEach((winRate, index) => {
        const x = padding + (index / (winRates.length - 1)) * chartWidth;
        const y = canvas.height - padding - ((winRate - minWinRate) / (maxWinRate - minWinRate)) * chartHeight;
        
        if (index === 0) {
            ctx.moveTo(x, y);
        } else {
            ctx.lineTo(x, y);
        }
    });
    ctx.stroke();
    
    // 添加图例
    ctx.fillStyle = '#2196F3';
    ctx.fillRect(padding, 10, 20, 10);
    ctx.fillStyle = '#333';
    ctx.font = '12px Arial';
    ctx.textAlign = 'left';
    ctx.fillText('Rating', padding + 25, 20);
    
    ctx.fillStyle = '#4CAF50';
    ctx.fillRect(padding + 80, 10, 20, 10);
    ctx.fillStyle = '#333';
    ctx.fillText('Win Rate (%)', padding + 105, 20);
    
    // 添加Y轴标签
    ctx.fillStyle = '#666';
    ctx.font = '10px Arial';
    ctx.textAlign = 'right';
    
    // Rating标签 (左侧)
    for (let i = 0; i <= 5; i++) {
        const rating = minRating + (maxRating - minRating) * (i / 5);
        const y = canvas.height - padding - (i / 5) * chartHeight;
        ctx.fillText(Math.round(rating), padding - 5, y + 3);
    }
    
    // Win Rate标签 (右侧)
    ctx.textAlign = 'left';
    for (let i = 0; i <= 5; i++) {
        const winRate = minWinRate + (maxWinRate - minWinRate) * (i / 5);
        const y = canvas.height - padding - (i / 5) * chartHeight;
        ctx.fillText(Math.round(winRate) + '%', canvas.width - padding + 5, y + 3);
    }
}

// 更新现有的renderPlayersTable函数，添加点击事件
function renderPlayersTable(players) {
    const tbody = document.getElementById('playersTableBody');
    tbody.innerHTML = '';
    
    players.forEach(player => {
        const row = document.createElement('tr');
        
        // 添加点击事件到玩家名称
        const nameCell = document.createElement('td');
        nameCell.innerHTML = `<a href="#" class="player-name-link" onclick="showPlayerHistoryModal('${player.pid}', '${player.name}'); return false;">${player.name}</a>`;
        
        row.innerHTML = `
            <td>${player.rank}</td>
        `;
        row.appendChild(nameCell);
        row.innerHTML += `
            <td>${player.versus_rating}</td>
            <td>${player.versus_won}</td>
            <td>${player.versus_plays}</td>
            <td>${player.win_rate}%</td>
            <td>${(() => {
                const dateObj = new Date(player.created_at);
                dateObj.setDate(dateObj.getDate() + 1);
                return dateObj.toLocaleDateString();
            })()}</td>
        `;
        
        tbody.appendChild(row);
    });
}

// 更新现有的loadRankingData函数
async function loadRankingData() {
    try {
        showLoading();
        
        const searchParams = new URLSearchParams();
        searchParams.append('page', currentPage);
        searchParams.append('per_page', perPage);
        searchParams.append('sort_by', sortBy);
        searchParams.append('sort_order', sortOrder);
        
        if (searchQuery) {
            searchParams.append('search', searchQuery);
        }
        
        if (rankFilter) {
            searchParams.append('rank_filter', rankFilter);
        }
        
        const response = await fetch(`/api/player-stats-snapshot?${searchParams}`);
        if (!response.ok) {
            throw new Error('Failed to fetch ranking data');
        }
        
        const data = await response.json();
        
        renderPlayersTable(data.players);
        updatePagination(data.pagination);
        
        hideLoading();
        
    } catch (error) {
        console.error('Error loading ranking data:', error);
        hideLoading();
        document.getElementById('playersTableBody').innerHTML = 
            '<tr><td colspan="7" class="error">Error loading data</td></tr>';
    }
}

// 全局变量
let currentPage = 1;
let perPage = 50;
let sortBy = 'versus_rating';
let sortOrder = 'desc';
let searchQuery = '';
let rankFilter = '';

// 分页相关函数
function updatePagination(pagination) {
    const paginationContainer = document.getElementById('pagination');
    if (!paginationContainer) return;
    
    let paginationHTML = '';
    
    // 上一页按钮
    if (pagination.has_prev) {
        paginationHTML += `<button onclick="goToPage(${pagination.current_page - 1})">Previous</button>`;
    }
    
    // 页码按钮
    const startPage = Math.max(1, pagination.current_page - 2);
    const endPage = Math.min(pagination.total_pages, pagination.current_page + 2);
    
    for (let i = startPage; i <= endPage; i++) {
        const activeClass = i === pagination.current_page ? 'active' : '';
        paginationHTML += `<button class="${activeClass}" onclick="goToPage(${i})">${i}</button>`;
    }
    
    // 下一页按钮
    if (pagination.has_next) {
        paginationHTML += `<button onclick="goToPage(${pagination.current_page + 1})">Next</button>`;
    }
    
    paginationContainer.innerHTML = paginationHTML;
    
    // 更新页面信息
    const pageInfo = document.getElementById('pageInfo');
    if (pageInfo) {
        pageInfo.textContent = `Page ${pagination.current_page} of ${pagination.total_pages} (${pagination.total_count} total records)`;
    }
}

function goToPage(page) {
    currentPage = page;
    loadRankingData();
}

// 搜索和过滤函数
function handleSearch() {
    const searchInput = document.getElementById('searchInput');
    searchQuery = searchInput.value.trim();
    currentPage = 1;
    loadRankingData();
}

function handleSortChange() {
    const sortSelect = document.getElementById('sortSelect');
    const orderSelect = document.getElementById('orderSelect');
    
    sortBy = sortSelect.value;
    sortOrder = orderSelect.value;
    currentPage = 1;
    loadRankingData();
}

function handleRankFilterChange() {
    const rankFilterSelect = document.getElementById('rankFilterSelect');
    rankFilter = rankFilterSelect.value;
    currentPage = 1;
    loadRankingData();
}

function handlePerPageChange() {
    const perPageSelect = document.getElementById('perPageSelect');
    perPage = parseInt(perPageSelect.value);
    currentPage = 1;
    loadRankingData();
}

// 初始化函数
function initializeRankingPage() {
    // 绑定事件监听器
    document.getElementById('searchInput').addEventListener('input', handleSearch);
    document.getElementById('sortSelect').addEventListener('change', handleSortChange);
    document.getElementById('orderSelect').addEventListener('change', handleSortChange);
    document.getElementById('rankFilterSelect').addEventListener('change', handleRankFilterChange);
    document.getElementById('perPageSelect').addEventListener('change', handlePerPageChange);
    
    // 加载初始数据
    loadRankingData();
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    initializeRankingPage();
});

// 将必要的函数暴露到全局范围，供HTML内联事件使用
window.showPlayerHistoryModal = showPlayerHistoryModal;
window.closePlayerHistoryModal = closePlayerHistoryModal;
window.showHistoryTab = showHistoryTab; 

// 历史模态框的国际化辅助函数
function getI18nTextForModal(key, defaultText) {
    const modalTexts = {
        'en': {
            'date': 'Date',
            'rating': 'Rating', 
            'todays-wins': "Today's Wins",
            'todays-games': "Today's Games",
            'todays-winrate': "Today's Win Rate",
            'daily-stats-title': '30-Day Daily Performance Statistics'
        },
        'zh-CN': {
            'date': '日期',
            'rating': '分数',
            'todays-wins': '今日胜利数',
            'todays-games': '今日游戏数',
            'todays-winrate': '今日胜率',
            'daily-stats-title': '30天每日表现统计'
        },
        'ja': {
            'date': '日付',
            'rating': 'レーティング',
            'todays-wins': '今日の勝利数',
            'todays-games': '今日のゲーム数',
            'todays-winrate': '今日の勝率',
            'daily-stats-title': '30日間の日別パフォーマンス統計'
        }
    };
    
    const currentLang = i18n.currentLanguage;
    return modalTexts[currentLang] && modalTexts[currentLang][key] ? modalTexts[currentLang][key] : defaultText;
} 