// 全局变量
let playersData = {};
let currentChart = null;
let currentRankingType = 'winrate'; // 'rating' 或 'winrate'
let playerNameMapping = {}; // 存储玩家ID到名字的映射

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
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
    // 搜索功能
    const searchInput = document.getElementById('playerSearch');
    const searchBtn = document.getElementById('searchBtn');
    
    searchInput.addEventListener('input', handleSearchInput);
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleSearch();
        }
    });
    searchBtn.addEventListener('click', handleSearch);
    
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

// 搜索输入处理
function handleSearchInput() {
    const query = document.getElementById('playerSearch').value.toLowerCase();
    const suggestions = document.getElementById('searchSuggestions');
    
    if (query.length < 1) {
        suggestions.style.display = 'none';
        return;
    }
    
    // 搜索匹配的玩家（通过ID或名字）
    const matchedPlayers = Object.keys(playersData).filter(playerId => {
        const playerName = getPlayerDisplayName(playerId);
        return playerId.toLowerCase().includes(query) || 
               playerName.toLowerCase().includes(query);
    });
    
    if (matchedPlayers.length > 0) {
        suggestions.innerHTML = matchedPlayers.map(playerId => {
            const playerName = getPlayerDisplayName(playerId);
            const displayText = playerName !== playerId ? `${playerName} (${playerId})` : playerId;
            return `<div class="suggestion-item" onclick="selectPlayer('${playerId}')">${displayText}</div>`;
        }).join('');
        suggestions.style.display = 'block';
    } else {
        suggestions.style.display = 'none';
    }
}

// 处理搜索
function handleSearch() {
    const query = document.getElementById('playerSearch').value.trim();
    if (!query) return;
    
    // 先尝试直接匹配ID
    if (playersData[query]) {
        selectPlayer(query);
        return;
    }
    
    // 尝试通过名字查找
    const matchedPlayerId = getPlayerIdByName(query);
    if (playersData[matchedPlayerId]) {
        selectPlayer(matchedPlayerId);
        return;
    }
    
    // 如果都没找到，显示提示
    alert('未找到该玩家，请检查输入的名字或ID是否正确');
}

// 选择玩家
function selectPlayer(playerId) {
    const player = playersData[playerId];
    if (!player) return;
    
    // 隐藏搜索建议
    document.getElementById('searchSuggestions').style.display = 'none';
    document.getElementById('playerSearch').value = getPlayerDisplayName(playerId);
    
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
    
    // 获取当前选中的玩家
    const searchValue = document.getElementById('playerSearch').value.trim();
    let selectedPlayer = null;
    
    // 先尝试通过名字查找玩家
    for (const [playerId, player] of Object.entries(playersData)) {
        if (getPlayerDisplayName(playerId) === searchValue || playerId === searchValue) {
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
    
    currentChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: '每日胜利数',
                    data: wins,
                    backgroundColor: 'rgba(255, 215, 0, 0.8)',
                    borderColor: 'rgba(255, 215, 0, 1)',
                    borderWidth: 1
                },
                {
                    label: '每日游戏数',
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
                    text: '最近30天每日游戏统计',
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
    
    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: '分数',
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
                    text: '最近60天分数趋势',
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
    
    currentChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: '每日胜率 (%)',
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
                    text: '最近60天每日胜率趋势',
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
}

// 显示加载动画
function showLoading() {
    const loadingHTML = `
        <h2><i class="fas fa-trophy"></i> 排行榜</h2>
        <div class="loading">
            <div class="spinner"></div>
            <p style="margin-top: 20px; color: #667eea;">正在加载数据...</p>
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
                    <h2><i class="fas fa-trophy"></i> 排行榜</h2>
                    <div class="ranking-tabs">
                        <button class="tab-btn active" data-tab="winrate">胜率排名</button>
                        <button class="tab-btn" data-tab="rating">分数排名</button>
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

// 点击其他地方隐藏搜索建议
document.addEventListener('click', function(event) {
    const searchContainer = document.querySelector('.search-container');
    const suggestions = document.getElementById('searchSuggestions');
    
    if (!searchContainer.contains(event.target)) {
        suggestions.style.display = 'none';
    }
}); 