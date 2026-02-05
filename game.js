// ゲーム設定
const CANVAS_WIDTH = 800;
const CANVAS_HEIGHT = 600;
const MAX_SPEED = 8;
const ACCELERATION = 0.15;
const BRAKE_POWER = 0.3;
const FRICTION = 0.02;
const TURN_SPEED = 0.05;
const TOTAL_LAPS = 3;

// キャンバス設定
const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
canvas.width = CANVAS_WIDTH;
canvas.height = CANVAS_HEIGHT;

// UI要素
const uiOverlay = document.getElementById('ui-overlay');
const lapCounter = document.getElementById('lap-counter');
const positionDisplay = document.getElementById('position');
const itemBox = document.getElementById('item-box');
const speedBar = document.getElementById('speed-bar');
const startScreen = document.getElementById('start-screen');
const startBtn = document.getElementById('start-btn');
const countdown = document.getElementById('countdown');
const resultScreen = document.getElementById('result-screen');
const resultTitle = document.getElementById('result-title');
const resultTime = document.getElementById('result-time');
const resultPosition = document.getElementById('result-position');
const restartBtn = document.getElementById('restart-btn');

// ゲーム状態
let gameState = 'menu'; // menu, countdown, playing, finished
let gameTime = 0;

// コース定義（サーキット型）
const TRACK_WIDTH = 200;
const trackPoints = [
    { x: 400, y: 100 },
    { x: 700, y: 150 },
    { x: 750, y: 400 },
    { x: 600, y: 600 },
    { x: 300, y: 650 },
    { x: 100, y: 500 },
    { x: 50, y: 250 },
    { x: 200, y: 100 }
];

// チェックポイント
const checkpoints = [
    { x: 550, y: 125, angle: Math.PI * 0.1 },
    { x: 725, y: 275, angle: Math.PI * 0.5 },
    { x: 675, y: 500, angle: Math.PI * 0.7 },
    { x: 450, y: 625, angle: Math.PI },
    { x: 200, y: 575, angle: Math.PI * 1.2 },
    { x: 75, y: 375, angle: Math.PI * 1.5 },
    { x: 125, y: 175, angle: Math.PI * 1.8 },
    { x: 300, y: 100, angle: 0 }
];

// アイテムボックスの位置
const itemBoxPositions = [
    { x: 600, y: 150 },
    { x: 700, y: 400 },
    { x: 450, y: 625 },
    { x: 100, y: 400 },
    { x: 150, y: 150 }
];

// プレイヤー
const player = {
    x: 400,
    y: 150,
    angle: Math.PI * 0.5,
    speed: 0,
    lap: 1,
    checkpoint: 0,
    item: null,
    hitTimer: 0,
    finishTime: 0
};

// CPUカート
const cpuKarts = [];
const CPU_COLORS = ['#ff4444', '#44ff44', '#4444ff', '#ffff44', '#ff44ff'];
const CPU_NAMES = ['レッド', 'グリーン', 'ブルー', 'イエロー', 'ピンク'];

// アイテム
const items = ['🍌', '🐢', '⭐', '🍄'];
const activeItems = []; // 地面に置かれたアイテム（バナナなど）
const flyingItems = []; // 飛んでいるアイテム（甲羅など）

// キー入力
const keys = {
    up: false,
    down: false,
    left: false,
    right: false,
    space: false
};

// キーボードイベント
document.addEventListener('keydown', (e) => {
    switch(e.key) {
        case 'ArrowUp': keys.up = true; break;
        case 'ArrowDown': keys.down = true; break;
        case 'ArrowLeft': keys.left = true; break;
        case 'ArrowRight': keys.right = true; break;
        case ' ': keys.space = true; e.preventDefault(); break;
    }
});

document.addEventListener('keyup', (e) => {
    switch(e.key) {
        case 'ArrowUp': keys.up = false; break;
        case 'ArrowDown': keys.down = false; break;
        case 'ArrowLeft': keys.left = false; break;
        case 'ArrowRight': keys.right = false; break;
        case ' ': keys.space = false; break;
    }
});

// CPUカート初期化
function initCPUKarts() {
    cpuKarts.length = 0;
    for (let i = 0; i < 5; i++) {
        cpuKarts.push({
            x: 350 + (i % 3) * 30,
            y: 180 + Math.floor(i / 3) * 40,
            angle: Math.PI * 0.5,
            speed: 0,
            lap: 1,
            checkpoint: 0,
            color: CPU_COLORS[i],
            name: CPU_NAMES[i],
            targetCheckpoint: 0,
            hitTimer: 0,
            finishTime: 0,
            finished: false
        });
    }
}

// プレイヤー初期化
function initPlayer() {
    player.x = 400;
    player.y = 150;
    player.angle = Math.PI * 0.5;
    player.speed = 0;
    player.lap = 1;
    player.checkpoint = 0;
    player.item = null;
    player.hitTimer = 0;
    player.finishTime = 0;
}

// アイテムボックス初期化
function initItemBoxes() {
    activeItems.length = 0;
    flyingItems.length = 0;
}

// コース上かどうかチェック
function isOnTrack(x, y) {
    // コースのスプライン曲線に沿って距離をチェック
    let minDist = Infinity;

    for (let i = 0; i < trackPoints.length; i++) {
        const p1 = trackPoints[i];
        const p2 = trackPoints[(i + 1) % trackPoints.length];

        // 線分との最短距離を計算
        const dx = p2.x - p1.x;
        const dy = p2.y - p1.y;
        const len = Math.sqrt(dx * dx + dy * dy);

        if (len === 0) continue;

        let t = ((x - p1.x) * dx + (y - p1.y) * dy) / (len * len);
        t = Math.max(0, Math.min(1, t));

        const nearX = p1.x + t * dx;
        const nearY = p1.y + t * dy;
        const dist = Math.sqrt((x - nearX) ** 2 + (y - nearY) ** 2);

        minDist = Math.min(minDist, dist);
    }

    return minDist < TRACK_WIDTH / 2;
}

// チェックポイント通過チェック
function checkCheckpoint(kart) {
    const cp = checkpoints[kart.checkpoint];
    const dist = Math.sqrt((kart.x - cp.x) ** 2 + (kart.y - cp.y) ** 2);

    if (dist < 80) {
        kart.checkpoint = (kart.checkpoint + 1) % checkpoints.length;

        // ラップ完了チェック
        if (kart.checkpoint === 0) {
            kart.lap++;
            if (kart.lap > TOTAL_LAPS) {
                kart.finishTime = gameTime;
                if (kart === player) {
                    finishRace();
                } else {
                    kart.finished = true;
                }
            }
        }
        return true;
    }
    return false;
}

// プレイヤー更新
function updatePlayer() {
    if (player.hitTimer > 0) {
        player.hitTimer--;
        player.speed *= 0.9;
        return;
    }

    // 加速・減速
    if (keys.up) {
        player.speed = Math.min(player.speed + ACCELERATION, MAX_SPEED);
    }
    if (keys.down) {
        player.speed = Math.max(player.speed - BRAKE_POWER, -MAX_SPEED / 2);
    }

    // 摩擦
    if (!keys.up && !keys.down) {
        player.speed *= (1 - FRICTION);
    }

    // ステアリング
    const turnAmount = TURN_SPEED * (player.speed / MAX_SPEED);
    if (keys.left) {
        player.angle -= turnAmount;
    }
    if (keys.right) {
        player.angle += turnAmount;
    }

    // 移動
    const newX = player.x + Math.cos(player.angle) * player.speed;
    const newY = player.y + Math.sin(player.angle) * player.speed;

    // コース外判定
    if (isOnTrack(newX, newY)) {
        player.x = newX;
        player.y = newY;
    } else {
        player.speed *= 0.5; // コース外で減速
        player.x = newX;
        player.y = newY;
    }

    // チェックポイント
    checkCheckpoint(player);

    // アイテム使用
    if (keys.space && player.item) {
        useItem(player);
        keys.space = false;
    }

    // アイテムボックス取得
    checkItemBoxCollision(player);

    // アイテム衝突
    checkItemHit(player);
}

// CPU更新
function updateCPU(cpu) {
    if (cpu.finished) return;

    if (cpu.hitTimer > 0) {
        cpu.hitTimer--;
        cpu.speed *= 0.9;
        return;
    }

    // ターゲットチェックポイントに向かう
    const target = checkpoints[cpu.checkpoint];
    const dx = target.x - cpu.x;
    const dy = target.y - cpu.y;
    const targetAngle = Math.atan2(dy, dx);

    // 角度差を計算
    let angleDiff = targetAngle - cpu.angle;
    while (angleDiff > Math.PI) angleDiff -= Math.PI * 2;
    while (angleDiff < -Math.PI) angleDiff += Math.PI * 2;

    // ステアリング
    const turnSpeed = 0.04;
    if (angleDiff > 0.1) {
        cpu.angle += turnSpeed;
    } else if (angleDiff < -0.1) {
        cpu.angle -= turnSpeed;
    }

    // 加速（ランダム性を追加）
    const targetSpeed = MAX_SPEED * (0.7 + Math.random() * 0.2);
    if (cpu.speed < targetSpeed) {
        cpu.speed += ACCELERATION * 0.8;
    }

    // 摩擦
    cpu.speed *= (1 - FRICTION);

    // 移動
    cpu.x += Math.cos(cpu.angle) * cpu.speed;
    cpu.y += Math.sin(cpu.angle) * cpu.speed;

    // チェックポイント
    checkCheckpoint(cpu);

    // アイテム衝突
    checkItemHit(cpu);
}

// アイテムボックス衝突チェック
function checkItemBoxCollision(kart) {
    if (kart.item) return;

    for (const box of itemBoxPositions) {
        const dist = Math.sqrt((kart.x - box.x) ** 2 + (kart.y - box.y) ** 2);
        if (dist < 40) {
            // アイテムルーレット
            kart.item = items[Math.floor(Math.random() * items.length)];
            break;
        }
    }
}

// アイテム使用
function useItem(kart) {
    const item = kart.item;
    kart.item = null;

    switch(item) {
        case '🍌':
            // バナナを後ろに設置
            activeItems.push({
                type: 'banana',
                x: kart.x - Math.cos(kart.angle) * 50,
                y: kart.y - Math.sin(kart.angle) * 50,
                emoji: '🍌'
            });
            break;
        case '🐢':
            // 甲羅を前に発射
            flyingItems.push({
                type: 'shell',
                x: kart.x,
                y: kart.y,
                angle: kart.angle,
                speed: 12,
                emoji: '🐢',
                life: 200
            });
            break;
        case '⭐':
            // スター（一時的にスピードアップ＆無敵）
            kart.speed = MAX_SPEED * 1.5;
            kart.hitTimer = -60; // 負の値で無敵
            break;
        case '🍄':
            // キノコ（スピードブースト）
            kart.speed = Math.min(kart.speed + 5, MAX_SPEED * 1.3);
            break;
    }
}

// アイテム衝突チェック
function checkItemHit(kart) {
    if (kart.hitTimer < 0) return; // 無敵中

    // バナナチェック
    for (let i = activeItems.length - 1; i >= 0; i--) {
        const item = activeItems[i];
        const dist = Math.sqrt((kart.x - item.x) ** 2 + (kart.y - item.y) ** 2);
        if (dist < 30) {
            kart.hitTimer = 60;
            kart.speed = 0;
            activeItems.splice(i, 1);
        }
    }

    // 甲羅チェック
    for (let i = flyingItems.length - 1; i >= 0; i--) {
        const item = flyingItems[i];
        const dist = Math.sqrt((kart.x - item.x) ** 2 + (kart.y - item.y) ** 2);
        if (dist < 40) {
            kart.hitTimer = 60;
            kart.speed = 0;
            flyingItems.splice(i, 1);
        }
    }
}

// 飛んでいるアイテム更新
function updateFlyingItems() {
    for (let i = flyingItems.length - 1; i >= 0; i--) {
        const item = flyingItems[i];
        item.x += Math.cos(item.angle) * item.speed;
        item.y += Math.sin(item.angle) * item.speed;
        item.life--;

        if (item.life <= 0 || !isOnTrack(item.x, item.y)) {
            flyingItems.splice(i, 1);
        }
    }
}

// 順位計算
function calculatePositions() {
    const allKarts = [
        { kart: player, type: 'player' },
        ...cpuKarts.map(k => ({ kart: k, type: 'cpu' }))
    ];

    // 進行度でソート
    allKarts.sort((a, b) => {
        const progressA = a.kart.lap * 100 + a.kart.checkpoint;
        const progressB = b.kart.lap * 100 + b.kart.checkpoint;
        return progressB - progressA;
    });

    const playerPos = allKarts.findIndex(k => k.type === 'player') + 1;
    return playerPos;
}

// コース描画
function drawTrack() {
    // 背景（草）
    ctx.fillStyle = '#228B22';
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);

    // コースの道路
    ctx.strokeStyle = '#555555';
    ctx.lineWidth = TRACK_WIDTH;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';

    ctx.beginPath();
    ctx.moveTo(trackPoints[0].x, trackPoints[0].y);
    for (let i = 1; i < trackPoints.length; i++) {
        ctx.lineTo(trackPoints[i].x, trackPoints[i].y);
    }
    ctx.closePath();
    ctx.stroke();

    // コースのライン
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 3;
    ctx.setLineDash([20, 20]);
    ctx.beginPath();
    ctx.moveTo(trackPoints[0].x, trackPoints[0].y);
    for (let i = 1; i < trackPoints.length; i++) {
        ctx.lineTo(trackPoints[i].x, trackPoints[i].y);
    }
    ctx.closePath();
    ctx.stroke();
    ctx.setLineDash([]);

    // スタート/ゴールライン
    ctx.strokeStyle = '#ffffff';
    ctx.lineWidth = 10;
    ctx.beginPath();
    ctx.moveTo(380, 80);
    ctx.lineTo(420, 80);
    ctx.stroke();

    // チェッカーフラッグパターン
    for (let i = 0; i < 4; i++) {
        ctx.fillStyle = i % 2 === 0 ? '#000000' : '#ffffff';
        ctx.fillRect(380 + i * 10, 75, 10, 10);
        ctx.fillStyle = i % 2 === 0 ? '#ffffff' : '#000000';
        ctx.fillRect(380 + i * 10, 85, 10, 10);
    }
}

// アイテムボックス描画
function drawItemBoxes() {
    for (const box of itemBoxPositions) {
        ctx.fillStyle = 'rgba(255, 215, 0, 0.8)';
        ctx.strokeStyle = '#ff8c00';
        ctx.lineWidth = 3;

        // 回転するボックス
        ctx.save();
        ctx.translate(box.x, box.y);
        ctx.rotate(Date.now() / 500);
        ctx.fillRect(-15, -15, 30, 30);
        ctx.strokeRect(-15, -15, 30, 30);
        ctx.fillStyle = '#ffffff';
        ctx.font = '16px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('?', 0, 0);
        ctx.restore();
    }
}

// カート描画
function drawKart(kart, color, isPlayer = false) {
    ctx.save();
    ctx.translate(kart.x, kart.y);
    ctx.rotate(kart.angle);

    // ヒット時は点滅
    if (kart.hitTimer > 0 && Math.floor(kart.hitTimer / 5) % 2 === 0) {
        ctx.globalAlpha = 0.5;
    }

    // スター時は虹色
    if (kart.hitTimer < 0) {
        const hue = (Date.now() / 10) % 360;
        color = `hsl(${hue}, 100%, 50%)`;
    }

    // カート本体
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.moveTo(25, 0);
    ctx.lineTo(-15, -15);
    ctx.lineTo(-15, 15);
    ctx.closePath();
    ctx.fill();
    ctx.strokeStyle = '#000000';
    ctx.lineWidth = 2;
    ctx.stroke();

    // タイヤ
    ctx.fillStyle = '#333333';
    ctx.fillRect(-12, -18, 8, 6);
    ctx.fillRect(-12, 12, 8, 6);
    ctx.fillRect(8, -18, 8, 6);
    ctx.fillRect(8, 12, 8, 6);

    // プレイヤーマーカー
    if (isPlayer) {
        ctx.fillStyle = '#ffff00';
        ctx.beginPath();
        ctx.arc(0, -25, 8, 0, Math.PI * 2);
        ctx.fill();
        ctx.fillStyle = '#000000';
        ctx.font = '10px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('P', 0, -25);
    }

    ctx.restore();
}

// 地面のアイテム描画
function drawGroundItems() {
    for (const item of activeItems) {
        ctx.font = '30px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(item.emoji, item.x, item.y);
    }
}

// 飛んでいるアイテム描画
function drawFlyingItems() {
    for (const item of flyingItems) {
        ctx.font = '25px Arial';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(item.emoji, item.x, item.y);
    }
}

// ミニマップ描画
function drawMinimap() {
    const mapX = CANVAS_WIDTH - 120;
    const mapY = CANVAS_HEIGHT - 120;
    const mapSize = 100;
    const scale = mapSize / 800;

    // 背景
    ctx.fillStyle = 'rgba(0, 0, 0, 0.5)';
    ctx.fillRect(mapX, mapY, mapSize, mapSize);

    // コース
    ctx.strokeStyle = '#888888';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(mapX + trackPoints[0].x * scale, mapY + trackPoints[0].y * scale);
    for (let i = 1; i < trackPoints.length; i++) {
        ctx.lineTo(mapX + trackPoints[i].x * scale, mapY + trackPoints[i].y * scale);
    }
    ctx.closePath();
    ctx.stroke();

    // CPUカート
    for (const cpu of cpuKarts) {
        ctx.fillStyle = cpu.color;
        ctx.beginPath();
        ctx.arc(mapX + cpu.x * scale, mapY + cpu.y * scale, 3, 0, Math.PI * 2);
        ctx.fill();
    }

    // プレイヤー
    ctx.fillStyle = '#ffffff';
    ctx.beginPath();
    ctx.arc(mapX + player.x * scale, mapY + player.y * scale, 4, 0, Math.PI * 2);
    ctx.fill();
}

// UI更新
function updateUI() {
    lapCounter.textContent = `LAP: ${Math.min(player.lap, TOTAL_LAPS)}/${TOTAL_LAPS}`;

    const position = calculatePositions();
    const positionText = ['1st', '2nd', '3rd', '4th', '5th', '6th'][position - 1];
    positionDisplay.textContent = `順位: ${positionText}`;

    itemBox.textContent = player.item || '';

    const speedPercent = Math.abs(player.speed) / MAX_SPEED * 100;
    speedBar.style.width = `${Math.min(speedPercent, 100)}%`;
}

// レース終了
function finishRace() {
    gameState = 'finished';
    const position = calculatePositions();
    const positionText = ['1位', '2位', '3位', '4位', '5位', '6位'][position - 1];

    resultTitle.textContent = position === 1 ? '🏆 優勝! 🏆' : 'ゴール!';
    resultTime.textContent = `タイム: ${(gameTime / 60).toFixed(2)}秒`;
    resultPosition.textContent = `最終順位: ${positionText}`;

    resultScreen.style.display = 'flex';
    uiOverlay.style.display = 'none';
}

// カウントダウン
async function startCountdown() {
    gameState = 'countdown';
    countdown.style.display = 'block';

    for (let i = 3; i > 0; i--) {
        countdown.textContent = i;
        await new Promise(r => setTimeout(r, 1000));
    }

    countdown.textContent = 'GO!';
    await new Promise(r => setTimeout(r, 500));

    countdown.style.display = 'none';
    gameState = 'playing';
    gameTime = 0;
}

// ゲーム初期化
function initGame() {
    initPlayer();
    initCPUKarts();
    initItemBoxes();
    gameTime = 0;
}

// メインゲームループ
function gameLoop() {
    // 描画
    drawTrack();
    drawItemBoxes();
    drawGroundItems();
    drawFlyingItems();

    // カート描画（CPUカート）
    for (const cpu of cpuKarts) {
        drawKart(cpu, cpu.color);
    }

    // プレイヤーカート
    drawKart(player, '#ffffff', true);

    // ミニマップ
    drawMinimap();

    // ゲームロジック
    if (gameState === 'playing') {
        gameTime++;
        updatePlayer();
        for (const cpu of cpuKarts) {
            updateCPU(cpu);
        }
        updateFlyingItems();
        updateUI();
    }

    requestAnimationFrame(gameLoop);
}

// イベントリスナー
startBtn.addEventListener('click', async () => {
    startScreen.style.display = 'none';
    uiOverlay.style.display = 'block';
    initGame();
    await startCountdown();
});

restartBtn.addEventListener('click', async () => {
    resultScreen.style.display = 'none';
    uiOverlay.style.display = 'block';
    initGame();
    await startCountdown();
});

// ゲーム開始
gameLoop();
