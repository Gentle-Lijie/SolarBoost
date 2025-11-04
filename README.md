# SolarBoost: 基于AI预测的智能太阳能供电系统

## 📌 项目简介

SolarBoost 是一个为电动车设计的智能能源管理系统演示项目。系统通过柔性太阳能板与机器学习算法的结合，实现对太阳能的智能调度，动态分配电能至动力系统、附件系统或电池充电，以提升续航里程、降低碳排放。

### 核心特性

- 🤖 **智能预测**：能耗预测 + 光伏发电预测
- ⚡ **动态调度**：四种工作模式（自动/节能/性能/手动）
- 🗺️ **路段模拟**：基于真实道路场景的数据生成
- 📊 **现代化UI**：使用DaisyUI组件库重新设计的美观界面
- 🎛️ **手动控制**：支持实时调整所有调度参数和传感器数据
- ⏱️ **可调模拟速度**：0.5-10秒/步的灵活速度控制
- 🎨 **全新能量流动图**：基于进度条的流畅可视化
- 🐳 **Docker一键部署**：快速启动整个系统

### 最新更新（v2.0）

✨ **UI全面重构**
- 采用DaisyUI组件库打造现代化界面
- 重新设计能量流动可视化（使用渐变进度条）
- 优化路网Canvas绘制，防止超出边界
- 响应式布局优化，支持各种屏幕尺寸

⏱️ **模拟速度控制**
- 新增模拟速度调节功能（快速/正常/缓慢）
- 集成在顶部菜单栏的三个按钮
- 点击即时切换，避免进度条卡顿
- 快速(1秒)、正常(2秒)、缓慢(5秒)三档可选

🐳 **Docker支持**
- 提供完整的Docker Compose配置
- 一键启动前后端服务
- 生产级别的Nginx反向代理配置

---

## 🏗️ 系统架构

详见 [项目架构.md](./项目架构.md)

**核心模块：**
1. **数据采集层**：车辆、GPS、环境、光伏传感器
2. **预测层**：能耗预测、光伏预测（可替换为真实ML模型）
3. **调度层**：基于规则的智能能量分配策略
4. **可视化层**：Vue.js前端实时展示

---

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Node.js 16+
- 现代浏览器（Chrome/Edge/Firefox）
- Docker & Docker Compose（可选，用于容器化部署）

### 方法一：Docker一键部署（推荐）

最简单的启动方式，无需手动安装依赖：

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看服务状态
docker-compose ps

# 访问应用
# 前端: http://localhost
# 后端API: http://localhost:5000
```

详细的Docker部署说明请参考 [DOCKER_DEPLOY.md](./DOCKER_DEPLOY.md)

### 方法二：自动化脚本

```powershell
# 1. 安装依赖
.\安装依赖.ps1

# 2. 启动项目
.\启动项目.ps1
```

### 方法三：手动启动

**后端：**
```powershell
cd backend
pip install -r requirements.txt
python app.py
```

**前端：**
```powershell
cd frontend
npm install
npm run dev
```

**访问：** http://localhost:3000

---

## 📡 API 接口说明

### 基础接口

#### `GET /api/health`
健康检查

**响应：**
```json
{
  "status": "ok",
  "service": "SolarBoost API"
}
```

---

### 传感器数据接口

#### `POST /api/sensor/simulate`
模拟传感器数据（基于路段）

**请求：**
```json
{
  "dt": 2.0
}
```

**响应：**
```json
{
  "status": "success",
  "data": {
    "vehicle": {
      "speed": 65.2,
      "accel": 0.15,
      "motor_power": 15230,
      "soc": 0.845,
      "aux_power": 820,
      "battery_voltage": 398.5,
      "battery_current": 38.2,
      "battery_temp": 31.2,
      "odometer": 1250.5
    },
    "gps": {
      "lat": 30.5850,
      "lon": 114.2790,
      "altitude": 105.2,
      "speed": 65.2,
      "heading": 85.3
    },
    "env": {
      "grade": 0.02,
      "hour": 14,
      "minute": 23,
      "temp": 27.5,
      "cloud": 0.15,
      "humidity": 0.55,
      "wind_speed": 2.3,
      "weather": "sunny"
    },
    "pv": {
      "power": 1650.5,
      "voltage": 48.2,
      "current": 34.2,
      "temp": 38.5,
      "efficiency": 0.182,
      "daily_energy": 12.5
    },
    "road": {
      "segment_name": "高速公路",
      "segment_index": 1,
      "speed_limit": 120,
      "traffic_density": 0.3,
      "position": 1250.5,
      "total_length": 13500,
      "progress": 9.3
    }
  }
}
```

#### `POST /api/sensor/update`
手动更新传感器数据

**请求：**
```json
{
  "position": 5000
}
```

---

### 道路信息接口

#### `GET /api/road/info`
获取道路路段信息

**响应：**
```json
{
  "status": "success",
  "segments": [
    {
      "name": "城市主干道",
      "length": 3000,
      "speed_limit": 60,
      "grade": 0.0,
      "traffic_density": 0.7,
      "weather": "sunny"
    },
    // ... 更多路段
  ],
  "total_length": 13500,
  "current_position": 1250.5
}
```

---

### 调度接口

#### `POST /api/ingest`
数据采集与能量调度

**请求：**
```json
{
  "vehicle": {
    "speed": 65,
    "accel": 0.2,
    "motor_power": 15000,
    "soc": 0.85,
    "aux_power": 800
  },
  "env": {
    "grade": 0.02,
    "hour": 14,
    "temp": 28,
    "cloud": 0.2,
    "lat": 30.57,
    "lon": 114.27
  },
  "pv": {
    "temp": 38,
    "historical_mean": 1500
  }
}
```

**响应：**
```json
{
  "status": "success",
  "predictions": {
    "energy": {
      "predicted_motor_power": 15500,
      "predicted_aux_power": 820,
      "confidence": 0.87
    },
    "solar": {
      "predicted_pv_power": 1650,
      "confidence": 0.82
    }
  },
  "dispatch": {
    "to_motor": 500,
    "to_aux": 800,
    "to_charge": 350,
    "mode": "auto",
    "reason": "高速巡航：平衡分配太阳能"
  },
  "timestamp": "2025-11-04 14:23:15"
}
```

#### `POST /api/mode`
切换工作模式

**请求：**
```json
{
  "mode": "eco"
}
```

**模式选项：**
- `auto` - 自动模式：根据行驶状态智能分配
- `eco` - 节能模式：优先充电，最大化续航
- `performance` - 性能模式：优先动力系统
- `manual` - 手动模式：用户自定义分配

**响应：**
```json
{
  "status": "success",
  "mode": "eco"
}
```

#### `POST /api/command`
手动控制（仅手动模式）

**请求：**
```json
{
  "to_motor": 600,
  "to_aux": 400,
  "to_charge": 500
}
```

**响应：**
```json
{
  "status": "success",
  "command": {
    "to_motor": 600,
    "to_aux": 400,
    "to_charge": 500
  }
}
```

#### `GET /api/state`
获取系统状态

**响应：**
```json
{
  "status": "success",
  "state": {
    "mode": "auto",
    "last_command": { /* 最近的调度指令 */ },
    "last_update": "2025-11-04 14:23:15",
    "events": [
      {
        "type": "info",
        "message": "切换到自动模式",
        "timestamp": "14:23:15"
      },
      // ... 更多事件
    ]
  }
}
```

---

## 🎮 使用说明

### 界面布局

```
┌────────────────────────────────────────────────────────┐
│  顶部导航栏：标题 | 速度按钮 | SOC | 光伏功率 | 模式    │
├───────────────────────────┬────────────────────────────┤
│                           │                            │
│  左侧：显示区域 (2/3)      │  右侧：控制区域 (1/3)       │
│                           │                            │
│  - 🗺️ 路网与车辆位置      │  - 🎮 工作模式切换          │
│    (优化Canvas绘制)       │  - 📡 传感器数据监控        │
│  - ⚡ 能量流动可视化       │    (支持手动调整)           │
│    (全新进度条设计)       │  - 🎛️ 手动控制面板         │
│  - 🎯 调度策略说明         │  - 📋 系统日志              │
│                           │                            │
└───────────────────────────┴────────────────────────────┘
```

### UI改进亮点

#### 🎨 能量流动可视化
- **旧版**：复杂的箭头和连线，不够清晰
- **新版**：
  - 左侧：太阳能源头（圆形进度指示器）
  - 中间：三条渐变进度条（动画显示能量流向）
  - 右侧：三个能量消耗端（带图标和数值）
  - 流畅的过渡动画，直观显示能量分配比例

#### 🗺️ 路网可视化
- 修复了Canvas超出容器边界的问题
- 添加overflow:hidden确保内容不溢出
- 设置固定高度400px，响应式宽度
- 保持清晰的道路分段和车辆位置指示

#### ⏱️ 模拟速度控制
- 三个快捷按钮：快速(1秒) / 正常(2秒) / 缓慢(5秒)
- 集成在顶部导航栏，节省空间
- 点击即时切换，无需拖动
- 避免了进度条拖动时的卡顿问题

### 路段模拟

系统模拟一条真实的驾驶路线，包括：
1. **城市主干道** (3km) - 速限60km/h，交通密集
2. **高速公路** (5km) - 速限120km/h，畅通
3. **上坡路段** (2km) - 坡度8%
4. **下坡路段** (2km) - 坡度-5%
5. **城市道路** (1.5km) - 速限50km/h，雨天

车辆自动在路段上行驶，传感器数据根据路段特性实时生成。

### 工作模式详解

#### 🤖 自动模式
根据当前行驶状态自动决策：
- **高能耗场景**（加速/高速）：70%太阳能辅助动力
- **低速巡航**：优先附件供电+充电
- **正常行驶**：平衡分配

#### 🌱 节能模式
最大化续航：
- 40%供应附件
- SOC<80%时：80%充电 + 20%动力
- SOC≥80%时：60%充电 + 40%动力

#### 🚀 性能模式
优先动力性能：
- 60%辅助动力系统
- 30%附件
- 10%充电

#### 🎮 手动模式
用户通过滑块自定义分配，系统自动确保总和≤可用光伏功率

---

## 💻 技术栈

### 后端
- **框架**：Flask 3.0.0
- **跨域支持**：Flask-CORS 4.0.0
- **数值计算**：NumPy 2.2.6
- **语言**：Python 3.13

### 前端
- **框架**：Vue.js 3.3.4
- **构建工具**：Vite 4.5.14
- **UI组件库**：DaisyUI 4.12+ (基于Tailwind CSS 3.4)
- **样式框架**：Tailwind CSS 3.4
- **HTTP客户端**：Axios 1.5.0

### 可视化
- **Canvas 2D**：路网和车辆绘制（优化边界控制）
- **CSS动画**：能量流动效果（渐变进度条）
- **实时数据绑定**：Vue响应式系统

### 部署
- **容器化**：Docker & Docker Compose
- **Web服务器**：Nginx (生产环境)
- **反向代理**：Nginx配置API代理

---

## 📂 项目结构

```
SolarBoost/
├── backend/                      # Flask 后端
│   ├── app.py                   # API 服务器
│   ├── models.py                # 预测和调度模型
│   ├── road_simulator.py        # 路段模拟器
│   ├── requirements.txt         # Python 依赖
│   └── Dockerfile               # 后端Docker配置
│
├── frontend/                     # Vue 前端
│   ├── src/
│   │   ├── App.vue              # 主应用组件（DaisyUI重构）
│   │   ├── main.js              # 入口文件
│   │   └── assets/
│   │       └── tailwind.css     # Tailwind样式
│   ├── index.html               # HTML 模板
│   ├── package.json             # Node 依赖
│   ├── vite.config.js           # Vite 配置
│   ├── tailwind.config.js       # Tailwind配置
│   ├── postcss.config.js        # PostCSS配置
│   ├── nginx.conf               # Nginx配置
│   └── Dockerfile               # 前端Docker配置
│
├── docker-compose.yml            # Docker Compose配置
├── .dockerignore                 # Docker忽略文件
├── README.md                     # 项目说明（本文件）
├── DOCKER_DEPLOY.md              # Docker部署指南
├── 项目架构.md                   # 架构设计文档
├── 活动方案.txt                  # 原始活动方案
├── 安装依赖.ps1                  # 自动化安装脚本
└── 启动项目.ps1                  # 自动化启动脚本
```

---

## 🔬 技术实现细节

### 能耗预测模型

使用物理公式模拟：
```python
# 空气阻力功率
P_air = 0.5 * ρ * Cd * A * v³

# 滚动阻力功率
P_roll = m * g * Cr * v

# 加速功率
P_accel = m * a * v

# 爬坡功率
P_grade = m * g * grade * v

# 总功率
P_total = P_air + P_roll + P_accel + P_grade
```

### 光伏预测模型

基于时间和天气：
```python
# 太阳辐射强度（正弦曲线）
solar_angle = (hour - 6) / 12 * π
intensity = sin(solar_angle)

# 云量影响
cloud_factor = 1 - cloud * 0.7

# 温度影响
temp_factor = 1 - (temp - 25) * 0.002

# 功率
P_pv = P_max * intensity * cloud_factor * temp_factor
```

### 调度策略算法

```python
if mode == 'auto':
    if 加速 or 高速:
        to_motor = pv_power * 0.7
        to_aux = min(remaining, aux_demand)
        to_charge = remaining - to_aux
    elif 低速:
        to_aux = min(pv_power, aux_demand)
        to_charge = pv_power - to_aux
    else:
        # 平衡分配
        ...
```

---

## 🎯 应用场景

### 演示展示
- ✅ 技术路演
- ✅ 产品验证
- ✅ 教学案例

### 实际应用潜力
- 🚗 电动汽车能量管理
- 🚌 新能源公交车
- 🚚 物流配送车辆
- 🏕️ 房车/露营车

---

## 🔄 技术路线

### 当前版本（v1.0 - Demo）
- ✅ 基于规则的模拟预测
- ✅ 固定路段场景
- ✅ 前端可视化
- ✅ 四种工作模式

### 下一步（v2.0 - 实用版）
- 🔲 集成真实ML模型（XGBoost/LSTM）
- 🔲 接入实时天气API
- 🔲 支持自定义路线
- 🔲 历史数据分析

### 未来展望（v3.0 - 生产版）
- 🔲 车辆CAN总线集成
- 🔲 云端训练与推理
- 🔲 OTA更新支持
- 🔲 多车协同调度

---

## 📊 性能指标

- **API 响应时间**：< 50ms
- **前端刷新率**：每2秒
- **Canvas绘制**：60fps
- **内存占用**：< 300MB（前+后端）
- **并发支持**：10+ 用户

---

## 🤝 贡献与反馈

本项目为演示项目，欢迎提出建议和改进意见。

**联系方式：**
- 📧 项目相关问题请通过GitHub Issues提交

---

## 📄 许可证

本项目仅用于学习和演示目的。

---

## 🎉 致谢

感谢所有为新能源汽车和智能能源管理技术发展做出贡献的研究者和工程师！

---

**SolarBoost** - 让每一缕阳光都发挥最大价值 ☀️🚗⚡

---

## 🏗️ 系统架构
1. **数据采集层**
   - 车辆数据：速度、加速度、SOC、电机功率、附件功率
   - 环境数据：GPS/坡度、天气、时间
   - 光伏数据：电压、电流、温度、历史发电量

2. **预测与调度层**
   - **能耗预测模型**：基于历史行驶数据预测未来功率需求
   - **光伏发电预测模型**：基于天气与时间预测太阳能可用功率
   - **调度策略**：动态分配太阳能至动力/附件/充电，保证性能与效率

3. **执行与控制层**
   - 控制功率分配器/继电器
   - 实时监控与日志记录
   - 异常检测与安全回退机制

4. **服务与界面层**
   - **后端**：Flask 提供 RESTful API
   - **前端**：Vue.js 构建实时监控与控制界面
   - **能量流可视化**：展示太阳能、电池、动力与附件之间的能量流动

---

## 🔮 技术细节

### 机器学习算法
- **能耗预测**：
  - 模型：XGBoost / LightGBM / LSTM
  - 输入：速度、加速度、坡度、SOC、历史能耗
  - 输出：未来 30 秒功率需求
- **光伏预测**：
  - 模型：Random Forest / GBDT
  - 输入：时间、天气、温度、历史发电
  - 输出：未来 5–15 分钟光伏功率

### 调度策略
- 高能耗场景（上坡/加速）：太阳能优先辅助动力系统
- 日常巡航：太阳能优先供给附件，剩余部分充电
- 停车/离网：太阳能独立供电，支持应急用电
- 安全约束：限流、过压/欠压保护、过温保护、切换抖动限制

---

## ⚙️ API 设计（Flask）

### 路由
- `POST /api/ingest`  
  输入车辆/环境/光伏数据，返回预测与调度指令
- `POST /api/mode`  
  设置模式（auto/manual/eco/performance）
- `POST /api/command`  
  手动模式下下发自定义功率分配
- `GET /api/state`  
  获取当前系统状态与最近指令

### 数据结构（JSON）
```json
{
  "vehicle": { "speed": 50, "accel": 0.4, "motor_power": 12000, "soc": 0.65, "aux_power": 800 },
  "env": { "grade": 0.03, "hour": 14, "temp": 23, "cloud": 0.2, "lat": 29.87, "lon": 121.55 },
  "pv": { "temp": 35, "historical_mean": 1200 }
}
```

---

## 💻 前端 UI（Vue.js）

### 功能模块
- **模式切换**：Auto / Eco / Performance / Manual
- **能量流动画**：太阳能 → 动力/附件/充电
- **预测曲线**：未来 30 秒功率需求与光伏功率
- **手动控制面板**：滑块控制 to_motor / to_aux / charge
- **日志与告警**：显示调度事件与异常信息

### 页面布局
- 顶部：系统状态栏（SOC、功率、模式）
- 左侧：能量流可视化
- 中间：预测曲线
- 右侧：手动控制与日志

---

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- npm 或 yarn

### 后端启动

1. 进入后端目录并安装依赖：
```powershell
cd backend
pip install -r requirements.txt
```

2. 启动 Flask 服务器：
```powershell
python app.py
```

后端服务将在 `http://localhost:5000` 启动

### 前端启动

1. 打开新的终端，进入前端目录并安装依赖：
```powershell
cd frontend
npm install
```

2. 启动开发服务器：
```powershell
npm run dev
```

前端应用将在 `http://localhost:3000` 启动

3. 在浏览器中访问 `http://localhost:3000` 查看系统界面

---

## 📂 项目结构

```
SolarBoost/
├── backend/                  # Flask 后端
│   ├── app.py               # 主应用和 API 路由
│   ├── models.py            # 预测模型和调度策略
│   └── requirements.txt     # Python 依赖
├── frontend/                 # Vue 前端
│   ├── src/
│   │   ├── App.vue         # 主应用组件
│   │   └── main.js         # 入口文件
│   ├── index.html          # HTML 模板
│   ├── package.json        # Node 依赖
│   └── vite.config.js      # Vite 配置
├── README.md                # 项目文档
└── 活动方案.txt             # 活动方案

```

---

## 🎮 功能演示

### 1. 自动模式
系统根据车辆状态和环境自动分配太阳能：
- **高能耗场景**（加速/高速）：太阳能优先辅助动力系统
- **低速巡航**：太阳能优先供给附件并充电
- **正常行驶**：平衡分配能量

### 2. 节能模式
最大化太阳能利用率，优先充电和附件供电，适合日常通勤。

### 3. 性能模式
优先将太阳能分配给动力系统，提供更强劲的加速性能。

### 4. 手动模式
用户可以通过滑块自定义功率分配，实时控制能量流向。

---

## 🔧 技术实现

### 后端（Flask）
- **能耗预测模型**：基于车速、加速度、坡度等参数预测未来功率需求
- **光伏预测模型**：基于时间、云量、温度预测太阳能可用功率
- **调度策略**：实现 4 种模式的智能能量分配算法
- **API 接口**：RESTful API 提供数据采集、模式切换、手动控制等功能

### 前端（Vue 3）
- **实时数据可视化**：动态显示能量流动和系统状态
- **模式切换界面**：一键切换不同工作模式
- **手动控制面板**：滑块控制功率分配
- **事件日志系统**：实时显示系统事件和告警
- **响应式设计**：适配不同屏幕尺寸

### 模拟数据
前端每 2 秒自动生成模拟的车辆遥测数据，包括：
- 车辆状态：速度、加速度、SOC、功率等
- 环境数据：时间、温度、云量、坡度等
- 光伏数据：温度、历史平均值等

---

## 📊 API 接口说明

### POST /api/ingest
接收数据并返回预测和调度指令

**请求体：**
```json
{
  "vehicle": {
    "speed": 50,
    "accel": 0.4,
    "motor_power": 12000,
    "soc": 0.65,
    "aux_power": 800
  },
  "env": {
    "grade": 0.03,
    "hour": 14,
    "temp": 23,
    "cloud": 0.2,
    "lat": 29.87,
    "lon": 121.55
  },
  "pv": {
    "temp": 35,
    "historical_mean": 1200
  }
}
```

**响应：**
```json
{
  "status": "success",
  "predictions": {
    "energy": {
      "predicted_motor_power": 15000,
      "predicted_aux_power": 800,
      "confidence": 0.85
    },
    "solar": {
      "predicted_pv_power": 1500,
      "confidence": 0.80
    }
  },
  "dispatch": {
    "to_motor": 500,
    "to_aux": 700,
    "to_charge": 300,
    "mode": "auto",
    "reason": "正常行驶：平衡分配太阳能"
  }
}
```

### POST /api/mode
切换系统模式

**请求体：**
```json
{
  "mode": "eco"
}
```

### POST /api/command
手动模式下发送控制指令

**请求体：**
```json
{
  "to_motor": 500,
  "to_aux": 300,
  "to_charge": 200
}
```

### GET /api/state
获取当前系统状态和事件日志

---

## 🎯 下一步优化方向

1. **真实机器学习模型**：用 XGBoost/LSTM 替换当前的模拟预测逻辑
2. **历史数据分析**：记录并分析历史调度效果
3. **更多安全约束**：添加过压/欠压/过温保护逻辑
4. **移动端适配**：优化触摸屏操作体验
5. **数据持久化**：使用数据库存储历史数据
6. **WebSocket 实时推送**：减少轮询，提高实时性
7. **地图集成**：集成真实地图API显示实际路线
8. **多语言支持**：添加国际化i18n支持
9. **性能优化**：Canvas离屏渲染，减少重绘
10. **Kubernetes部署**：提供K8s部署配置

---

## 📝 许可证

本项目仅用于学习和演示目的。
