<template>
    <div class="min-h-screen bg-base-200">
    <!-- 顶部导航栏 -->
    <div class="navbar bg-primary text-primary-content shadow-lg backdrop-blur-sm bg-opacity-90">
      <div class="flex-1">
        <a class="btn btn-ghost normal-case text-xl">
          <span class="text-2xl">🌞</span>
          <span class="ml-2">SolarBoost 智能太阳能调度系统</span>
        </a>
        <div class="badge badge-secondary ml-4">AI驱动</div>
        
        <!-- 模拟速度按钮组 -->
        <div class="ml-6 flex items-center gap-2">
          <span class="text-xs opacity-70">模拟速度:</span>
          <div class="btn-group">
            <button 
              :class="['btn btn-xs', simulationSpeed === 1 ? 'btn-active' : '']"
              @click="setSimulationSpeed(1)"
            >
              快速
            </button>
            <button 
              :class="['btn btn-xs', simulationSpeed === 2 ? 'btn-active' : '']"
              @click="setSimulationSpeed(2)"
            >
              正常
            </button>
            <button 
              :class="['btn btn-xs', simulationSpeed === 5 ? 'btn-active' : '']"
              @click="setSimulationSpeed(5)"
            >
              缓慢
            </button>
          </div>
        </div>
      </div>
      <div class="flex-none gap-2">
        <!-- 主题切换按钮 -->
        <button 
          class="btn btn-circle btn-ghost mr-2"
          @click="toggleTheme"
          :title="isDarkTheme ? '切换到亮色主题' : '切换到暗色主题'"
        >
          <span class="text-2xl">{{ isDarkTheme ? '☀️' : '🌙' }}</span>
        </button>
        
        <div class="stats stats-horizontal shadow">
          <div class="stat py-2 px-4">
            <div class="stat-title text-xs">电池SOC</div>
            <div class="stat-value text-lg" :class="sensorData.vehicle?.soc > 0.8 ? 'text-success' : sensorData.vehicle?.soc > 0.3 ? 'text-warning' : 'text-error'">
              {{ (sensorData.vehicle?.soc * 100 || 0).toFixed(1) }}%
            </div>
          </div>
          <div class="stat py-2 px-4">
            <div class="stat-title text-xs">光伏功率</div>
            <div class="stat-value text-lg text-warning">{{ sensorData.pv?.power || 0 }}W</div>
          </div>
          <div class="stat py-2 px-4">
            <div class="stat-title text-xs">当前模式</div>
            <div class="stat-value text-lg font-bold">{{ modeText }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="container mx-auto p-4 max-w-[1920px]">
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-4">
        <!-- 左侧列：地图和能量流 -->
        <div class="xl:col-span-2 space-y-4">
          <!-- 路网与车辆位置 -->
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title">
                <span class="text-2xl">🗺️</span>
                路网与车辆位置
                <div class="badge badge-info">{{ sensorData.road?.segment_name || '-' }}</div>
              </h2>
              <div class="w-full overflow-hidden rounded-lg bg-neutral" style="height: 400px;">
                <canvas ref="roadCanvas" style="width: 100%; height: 100%;"></canvas>
              </div>
              <div class="flex justify-between text-sm mt-2">
                <div class="stat-desc flex items-center gap-2">
                  <span class="text-lg">🚗</span>
                  速度: {{ sensorData.vehicle?.speed?.toFixed(1) || 0 }} km/h
                </div>
                <div class="stat-desc flex items-center gap-2">
                  <span class="text-lg">📍</span>
                  进度: {{ ((sensorData.road?.position / sensorData.road?.total_length * 100) || 0).toFixed(1) }}%
                </div>
              </div>
            </div>
          </div>

          <!-- 能量流动可视化 -->
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title">
                <span class="text-2xl">⚡</span>
                能量流动可视化
              </h2>
              <div class="flex items-center justify-around py-8">
                <!-- 太阳能源 -->
                <div class="flex flex-col items-center">
                  <div class="radial-progress text-warning" :style="`--value:${Math.min((sensorData.pv?.power || 0) / 50, 100)};`" role="progressbar">
                    <span class="text-3xl">☀️</span>
                  </div>
                  <div class="text-center mt-2">
                    <div class="font-bold text-lg">{{ sensorData.pv?.power || 0 }}W</div>
                    <div class="text-xs opacity-70">太阳能输入</div>
                  </div>
                </div>

                <!-- 流动指示器 -->
                <div class="flex flex-col gap-4">
                  <div class="flex items-center gap-2">
                    <div class="w-32 h-2 bg-base-300 rounded-full overflow-hidden">
                      <div class="h-full bg-gradient-to-r from-warning to-info" 
                           :style="`width: ${getFlowWidth('motor')}%`"></div>
                    </div>
                    <span class="text-sm font-mono">{{ dispatchCommand.to_motor?.toFixed(0) || 0 }}W</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <div class="w-32 h-2 bg-base-300 rounded-full overflow-hidden">
                      <div class="h-full bg-gradient-to-r from-warning to-secondary" 
                           :style="`width: ${getFlowWidth('aux')}%`"></div>
                    </div>
                    <span class="text-sm font-mono">{{ dispatchCommand.to_aux?.toFixed(0) || 0 }}W</span>
                  </div>
                  <div class="flex items-center gap-2">
                    <div class="w-32 h-2 bg-base-300 rounded-full overflow-hidden">
                      <div class="h-full bg-gradient-to-r from-warning to-success" 
                           :style="`width: ${getFlowWidth('charge')}%`"></div>
                    </div>
                    <span class="text-sm font-mono">{{ dispatchCommand.to_charge?.toFixed(0) || 0 }}W</span>
                  </div>
                </div>

                <!-- 能量消耗端 -->
                <div class="flex flex-col gap-4">
                  <div class="flex items-center gap-3">
                    <div class="avatar placeholder">
                      <div class="bg-info text-neutral-content rounded-full w-12">
                        <span class="text-xl">⚡</span>
                      </div>
                    </div>
                    <div>
                      <div class="font-bold">{{ sensorData.vehicle?.motor_power || 0 }}W</div>
                      <div class="text-xs opacity-70">动力系统</div>
                    </div>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="avatar placeholder">
                      <div class="bg-secondary text-neutral-content rounded-full w-12">
                        <span class="text-xl">❄️</span>
                      </div>
                    </div>
                    <div>
                      <div class="font-bold">{{ sensorData.vehicle?.aux_power || 0 }}W</div>
                      <div class="text-xs opacity-70">附件系统</div>
                    </div>
                  </div>
                  <div class="flex items-center gap-3">
                    <div class="avatar placeholder">
                      <div class="bg-success text-neutral-content rounded-full w-12">
                        <span class="text-xl">🔋</span>
                      </div>
                    </div>
                    <div>
                      <div class="font-bold">{{ dispatchCommand.to_charge?.toFixed(0) || 0 }}W</div>
                      <div class="text-xs opacity-70">电池充电</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 调度策略 -->
          <div class="alert alert-info shadow-2xl border border-info/20 bg-gradient-to-r from-info/10 to-info/5 hover:shadow-3xl transition-all duration-300">
            <div class="flex items-center gap-3">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current flex-shrink-0 w-8 h-8">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <div class="flex-1">
                <h3 class="font-bold text-lg mb-1">智能调度策略</h3>
                <div class="text-sm opacity-90">{{ dispatchCommand.reason || '等待数据...' }}</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 右侧列：控制面板 -->
        <div class="space-y-4">
          <!-- 工作模式切换 -->
          <div class="card bg-gradient-to-br from-base-100 to-base-200 shadow-2xl hover:shadow-3xl transition-all duration-300 border border-base-300">
            <div class="card-body">
              <h2 class="card-title">
                <span class="text-3xl">🎮</span>
                工作模式切换
              </h2>
              <div class="grid grid-cols-2 gap-4">
                <button 
                  v-for="mode in modes" 
                  :key="mode.value"
                  :class="[
                    'btn m-2 hover:scale-105 transition-all duration-200 shadow-md hover:shadow-lg',
                    currentMode === mode.value 
                      ? 'btn-primary btn-active shadow-primary/50' 
                      : 'btn-outline hover:bg-base-200'
                  ]"
                  @click="switchMode(mode.value)"
                >
                  <span class="text-2xl mr-2">{{ mode.icon }}</span>
                  <span class="font-bold">{{ mode.name }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 传感器控制 -->
          <div class="card bg-gradient-to-br from-base-100 to-base-200 shadow-2xl hover:shadow-3xl transition-all duration-300 border border-base-300">
            <div class="card-body max-h-[600px] overflow-y-auto">
              <h2 class="card-title">
                <span class="text-3xl">📡</span>
                传感器数据控制
              </h2>
              <div class="btn-group btn-group-horizontal w-full mb-4 gap-2">
                <button 
                  :class="['btn btn-sm flex-1 hover:scale-105 transition-transform', sensorMode === 'auto' ? 'btn-active btn-success' : 'btn-outline']"
                  @click="setSensorMode('auto')"
                >
                  🤖 自动模式
                </button>
                <button 
                  :class="['btn btn-sm flex-1 hover:scale-105 transition-transform', sensorMode === 'manual' ? 'btn-active btn-warning' : 'btn-outline']"
                  @click="setSensorMode('manual')"
                >
                  🎛️ 手动模式
                </button>
              </div>
              
              <div class="divider">车辆系统</div>
              <div class="space-y-2">
                <div v-for="(value, key) in sensorData.vehicle" :key="key" class="form-control">
                  <label class="label py-1">
                    <span class="label-text text-xs">{{ getSensorLabel(key) }}</span>
                    <span class="label-text-alt font-mono text-xs">{{ formatValue(sensorMode === 'manual' ? manualSensorData.vehicle[key] : value, key) }}</span>
                  </label>
                  <input v-if="sensorMode === 'manual'" 
                         type="range" 
                         :value="manualSensorData.vehicle[key]" 
                         @input="updateManualSensor('vehicle', key, $event.target.value)"
                         :min="getSensorMin(key)"
                         :max="getSensorMax(key)"
                         :step="getSensorStep(key)"
                         class="range range-xs range-accent" />
                </div>
              </div>

              <div class="divider">环境监测</div>
              <div class="space-y-2">
                <div v-for="(value, key) in sensorData.env" :key="key" class="form-control">
                  <label class="label py-1">
                    <span class="label-text text-xs">{{ getSensorLabel(key) }}</span>
                    <span class="label-text-alt font-mono text-xs">{{ formatValue(sensorMode === 'manual' ? manualSensorData.env[key] : value, key) }}</span>
                  </label>
                  <input v-if="sensorMode === 'manual' && key !== 'weather'" 
                         type="range" 
                         :value="manualSensorData.env[key]" 
                         @input="updateManualSensor('env', key, $event.target.value)"
                         :min="getSensorMin(key)"
                         :max="getSensorMax(key)"
                         :step="getSensorStep(key)"
                         class="range range-xs range-accent" />
                  <select v-if="sensorMode === 'manual' && key === 'weather'" 
                          :value="manualSensorData.env[key]"
                          @change="updateManualSensor('env', key, $event.target.value)"
                          class="select select-xs select-bordered">
                    <option value="sunny">晴天</option>
                    <option value="cloudy">多云</option>
                    <option value="rainy">雨天</option>
                  </select>
                </div>
              </div>

              <div v-if="sensorMode === 'manual'" class="card-actions justify-end mt-4 gap-2">
                <button class="btn btn-sm btn-success" @click="applyManualSensors">应用设置</button>
                <button class="btn btn-sm btn-ghost" @click="resetManualSensors">重置</button>
              </div>
            </div>
          </div>

          <!-- 手动控制面板 -->
          <div v-if="currentMode === 'manual'" class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title">
                <span class="text-2xl">🎛️</span>
                手动控制
              </h2>
              <div class="space-y-4">
                <div class="form-control">
                  <label class="label">
                    <span class="label-text">动力系统</span>
                    <span class="label-text-alt">{{ manualCommand.to_motor }}W</span>
                  </label>
                  <input type="range" min="0" :max="sensorData.pv?.power || 2000" 
                         v-model.number="manualCommand.to_motor"
                         @input="updateManualCommand"
                         class="range range-info" />
                </div>
                <div class="form-control">
                  <label class="label">
                    <span class="label-text">附件系统</span>
                    <span class="label-text-alt">{{ manualCommand.to_aux }}W</span>
                  </label>
                  <input type="range" min="0" :max="sensorData.pv?.power || 2000" 
                         v-model.number="manualCommand.to_aux"
                         @input="updateManualCommand"
                         class="range range-secondary" />
                </div>
                <div class="form-control">
                  <label class="label">
                    <span class="label-text">电池充电</span>
                    <span class="label-text-alt">{{ manualCommand.to_charge }}W</span>
                  </label>
                  <input type="range" min="0" :max="sensorData.pv?.power || 2000" 
                         v-model.number="manualCommand.to_charge"
                         @input="updateManualCommand"
                         class="range range-success" />
                </div>
                <button class="btn btn-primary w-full m-2" @click="applyManualCommand">应用设置</button>
              </div>
            </div>
          </div>

          <!-- 系统日志 -->
          <div class="card bg-gradient-to-br from-base-100 to-base-200 shadow-2xl hover:shadow-3xl transition-all duration-300 border border-base-300">
            <div class="card-body">
              <h2 class="card-title">
                <span class="text-3xl">📋</span>
                系统事件日志
              </h2>
              <div class="mockup-code max-h-64 overflow-y-auto bg-base-300 shadow-inner rounded-lg">
                <div v-for="(event, index) in events" :key="index" 
                     :class="[
                       'px-4 py-2 transition-all duration-200 hover:bg-base-100 rounded-md mx-2 my-1',
                       getLogClass(event.type)
                     ]">
                  <span class="opacity-60 text-xs">[{{ event.timestamp }}]</span> 
                  <span class="ml-2 font-medium">{{ event.message }}</span>
                </div>
                <div v-if="events.length === 0" class="px-4 py-4 opacity-50 text-center">
                  <span class="text-2xl">📝</span>
                  <div class="mt-2">暂无系统事件</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'App',
  data() {
    return {
      currentMode: 'auto',
      sensorMode: 'auto',
      simulationSpeed: 2,
      isDarkTheme: false,
      modes: [
        { value: 'auto', name: '自动', icon: '🤖' },
        { value: 'eco', name: '节能', icon: '🌱' },
        { value: 'performance', name: '性能', icon: '🚀' },
        { value: 'manual', name: '手动', icon: '🎮' }
      ],
      sensorData: {
        vehicle: {},
        gps: {},
        env: {},
        pv: {},
        road: {}
      },
      manualSensorData: {
        vehicle: {},
        gps: {},
        env: {},
        pv: {}
      },
      predictions: {},
      dispatchCommand: {},
      events: [],
      manualCommand: {
        to_motor: 0,
        to_aux: 0,
        to_charge: 0
      },
      roadSegments: [],
      updateTimer: null,
      canvas: null,
      ctx: null
    }
  },
  computed: {
    modeText() {
      const mode = this.modes.find(m => m.value === this.currentMode)
      return mode ? mode.name : '未知'
    }
  },
  mounted() {
    this.initCanvas()
    this.fetchRoadInfo()
    this.startSimulation()
    this.loadTheme()
  },
  beforeUnmount() {
    if (this.updateTimer) {
      clearInterval(this.updateTimer)
    }
  },
  methods: {
    initCanvas() {
      this.canvas = this.$refs.roadCanvas
      if (this.canvas) {
        this.ctx = this.canvas.getContext('2d')
        const parent = this.canvas.parentElement
        this.canvas.width = parent.offsetWidth
        this.canvas.height = 400
      }
    },
    
    async fetchRoadInfo() {
      try {
        const response = await axios.get('/api/road/info')
        if (response.data.status === 'success') {
          this.roadSegments = response.data.segments
        }
      } catch (error) {
        console.error('获取道路信息失败:', error)
      }
    },
    
    startSimulation() {
      this.simulateStep()
      this.updateTimer = setInterval(() => {
        this.simulateStep()
      }, this.simulationSpeed * 1000)
    },
    
    setSimulationSpeed(speed) {
      this.simulationSpeed = speed
      if (this.updateTimer) {
        clearInterval(this.updateTimer)
      }
      this.startSimulation()
      const labels = { 1: '快速', 2: '正常', 5: '缓慢' }
      this.addEvent('info', `模拟速度已调整为${labels[speed]}模式 (${speed}秒/步)`)
    },
    
    async simulateStep() {
      try {
        const sensorResponse = await axios.post('/api/sensor/simulate', { dt: this.simulationSpeed })
        if (sensorResponse.data.status === 'success') {
          this.sensorData = sensorResponse.data.data
        }
        
        const ingestResponse = await axios.post('/api/ingest', {
          vehicle: this.sensorData.vehicle,
          env: this.sensorData.env,
          pv: this.sensorData.pv
        })
        
        if (ingestResponse.data.status === 'success') {
          this.predictions = ingestResponse.data.predictions
          this.dispatchCommand = ingestResponse.data.dispatch
          this.fetchEvents()
        }
        
        this.drawRoadVisualization()
        
      } catch (error) {
        console.error('模拟步骤失败:', error)
      }
    },
    
    drawRoadVisualization() {
      if (!this.ctx || !this.roadSegments.length) return
      
      const ctx = this.ctx
      const width = this.canvas.width
      const height = this.canvas.height
      
      ctx.fillStyle = '#1a1a2e'
      ctx.fillRect(0, 0, width, height)
      
      const margin = 50
      const roadHeight = 60
      const totalLength = this.sensorData.road?.total_length || 1
      const currentPos = this.sensorData.road?.position || 0
      
      let x = margin
      const y = height / 2 - roadHeight / 2
      
      this.roadSegments.forEach((segment, index) => {
        const segmentWidth = (segment.length / totalLength) * (width - 2 * margin)
        
        ctx.fillStyle = index % 2 === 0 ? '#2d2d44' : '#3d3d5c'
        ctx.fillRect(x, y, segmentWidth, roadHeight)
        
        ctx.strokeStyle = '#4a4a6a'
        ctx.lineWidth = 2
        ctx.strokeRect(x, y, segmentWidth, roadHeight)
        
        ctx.fillStyle = '#ffffff'
        ctx.font = '12px Arial'
        ctx.textAlign = 'center'
        ctx.fillText(segment.name, x + segmentWidth / 2, y - 10)
        
        ctx.fillStyle = '#ffd700'
        ctx.font = '10px Arial'
        ctx.fillText(`${segment.speed_limit}km/h`, x + segmentWidth / 2, y + roadHeight + 15)
        
        ctx.strokeStyle = '#ffff00'
        ctx.setLineDash([10, 5])
        ctx.beginPath()
        ctx.moveTo(x, y + roadHeight / 2)
        ctx.lineTo(x + segmentWidth, y + roadHeight / 2)
        ctx.stroke()
        ctx.setLineDash([])
        
        x += segmentWidth
      })
      
      const carX = margin + (currentPos / totalLength) * (width - 2 * margin)
      const carY = y + roadHeight / 2
      
      ctx.fillStyle = '#ff6b6b'
      ctx.beginPath()
      ctx.arc(carX, carY, 15, 0, Math.PI * 2)
      ctx.fill()
      
      ctx.fillStyle = '#ffffff'
      ctx.beginPath()
      ctx.moveTo(carX + 10, carY)
      ctx.lineTo(carX + 5, carY - 5)
      ctx.lineTo(carX + 5, carY + 5)
      ctx.closePath()
      ctx.fill()
      
      ctx.fillStyle = '#ffffff'
      ctx.font = 'bold 12px Arial'
      ctx.textAlign = 'center'
      ctx.fillText('🚗', carX, carY - 25)
      
      const speed = this.sensorData.vehicle?.speed || 0
      ctx.fillStyle = '#4caf50'
      ctx.font = 'bold 14px Arial'
      ctx.fillText(`${speed.toFixed(1)} km/h`, carX, carY + 40)
      
      const pvPower = this.sensorData.pv?.power || 0
      if (pvPower > 100) {
        ctx.fillStyle = '#ffd700'
        ctx.beginPath()
        ctx.arc(carX, carY - 5, 8, 0, Math.PI * 2)
        ctx.fill()
        ctx.fillStyle = '#000'
        ctx.font = '10px Arial'
        ctx.fillText('☀️', carX, carY - 2)
      }
      
      ctx.fillStyle = 'rgba(76, 175, 80, 0.3)'
      ctx.fillRect(margin, y + roadHeight + 35, (width - 2 * margin) * (currentPos / totalLength), 8)
      ctx.strokeStyle = '#4caf50'
      ctx.strokeRect(margin, y + roadHeight + 35, width - 2 * margin, 8)
      
      ctx.fillStyle = '#4caf50'
      ctx.font = '12px Arial'
      ctx.textAlign = 'right'
      ctx.fillText(`进度: ${((currentPos / totalLength) * 100).toFixed(1)}%`, width - margin, y + roadHeight + 60)
    },
    
    getFlowWidth(target) {
      const pvPower = this.sensorData.pv?.power || 0
      if (pvPower === 0) return 0
      const value = this.dispatchCommand[`to_${target}`] || 0
      return Math.min((value / pvPower) * 100, 100)
    },
    
    async fetchEvents() {
      try {
        const response = await axios.get('/api/state')
        if (response.data.status === 'success') {
          this.events = response.data.state.events || []
        }
      } catch (error) {
        console.error('获取事件失败:', error)
      }
    },
    
    async switchMode(mode) {
      try {
        const response = await axios.post('/api/mode', { mode })
        if (response.data.status === 'success') {
          this.currentMode = mode
          this.fetchEvents()
        }
      } catch (error) {
        console.error('切换模式失败:', error)
      }
    },
    
    updateManualCommand() {
      const total = this.manualCommand.to_motor + this.manualCommand.to_aux + this.manualCommand.to_charge
      const maxPower = this.sensorData.pv?.power || 2000
      if (total > maxPower) {
        const ratio = maxPower / total
        this.manualCommand.to_motor = Math.floor(this.manualCommand.to_motor * ratio)
        this.manualCommand.to_aux = Math.floor(this.manualCommand.to_aux * ratio)
        this.manualCommand.to_charge = Math.floor(this.manualCommand.to_charge * ratio)
      }
    },
    
    async applyManualCommand() {
      try {
        const response = await axios.post('/api/command', this.manualCommand)
        if (response.data.status === 'success') {
          this.fetchEvents()
        }
      } catch (error) {
        console.error('应用手动命令失败:', error)
      }
    },
    
    getSensorLabel(key) {
      const labels = {
        speed: '速度', accel: '加速度', motor_power: '动力功率', soc: 'SOC',
        aux_power: '附件功率', battery_voltage: '电池电压', battery_current: '电池电流',
        battery_temp: '电池温度', odometer: '里程',
        lat: '纬度', lon: '经度', altitude: '海拔', heading: '航向',
        grade: '坡度', hour: '小时', minute: '分钟', temp: '温度', cloud: '云量',
        humidity: '湿度', wind_speed: '风速', weather: '天气',
        power: '功率', voltage: '电压', current: '电流', efficiency: '效率',
        daily_energy: '日发电量'
      }
      return labels[key] || key
    },
    
    formatValue(value, key) {
      if (typeof value === 'number') {
        if (key.includes('temp') || key === 'temperature') return `${value.toFixed(1)}°C`
        if (key === 'speed') return `${value.toFixed(1)} km/h`
        if (key === 'power' || key === 'motor_power' || key === 'aux_power') return `${value.toFixed(0)} W`
        if (key === 'voltage' || key === 'battery_voltage') return `${value.toFixed(1)} V`
        if (key === 'current' || key === 'battery_current') return `${value.toFixed(2)} A`
        if (key === 'soc') return `${(value * 100).toFixed(1)}%`
        if (key === 'cloud' || key === 'humidity' || key === 'efficiency') return `${(value * 100).toFixed(1)}%`
        if (key === 'grade') return `${(value * 100).toFixed(1)}%`
        return value.toFixed(2)
      }
      return value
    },
    
    setSensorMode(mode) {
      this.sensorMode = mode
      if (mode === 'manual') {
        this.manualSensorData = JSON.parse(JSON.stringify(this.sensorData))
        delete this.manualSensorData.road
      }
    },
    
    updateManualSensor(category, key, value) {
      const numValue = parseFloat(value)
      if (!isNaN(numValue)) {
        this.manualSensorData[category][key] = numValue
      } else {
        this.manualSensorData[category][key] = value
      }
    },
    
    getSensorStep(key) {
      const steps = {
        speed: 0.1, accel: 0.01, motor_power: 10, soc: 0.001,
        aux_power: 10, battery_voltage: 0.1, battery_current: 0.01,
        battery_temp: 0.1, odometer: 1,
        lat: 0.0001, lon: 0.0001, altitude: 1, heading: 0.1,
        grade: 0.001, hour: 1, minute: 1, temp: 0.1, cloud: 0.001,
        humidity: 0.001, wind_speed: 0.1,
        power: 1, voltage: 0.1, current: 0.01, efficiency: 0.001,
        daily_energy: 1
      }
      return steps[key] || 0.01
    },
    
    getSensorMin(key) {
      const mins = {
        speed: 0, accel: -5, motor_power: 0, soc: 0,
        aux_power: 0, battery_voltage: 300, battery_current: -50,
        battery_temp: -20, odometer: 0,
        lat: -90, lon: -180, altitude: -100, heading: 0,
        grade: -0.5, hour: 0, minute: 0, temp: -50, cloud: 0,
        humidity: 0, wind_speed: 0,
        power: 0, voltage: 0, current: -50, efficiency: 0,
        daily_energy: 0
      }
      return mins[key] || 0
    },
    
    getSensorMax(key) {
      const maxs = {
        speed: 200, accel: 5, motor_power: 20000, soc: 1,
        aux_power: 2000, battery_voltage: 450, battery_current: 100,
        battery_temp: 80, odometer: 100000,
        lat: 90, lon: 180, altitude: 5000, heading: 360,
        grade: 0.5, hour: 23, minute: 59, temp: 60, cloud: 1,
        humidity: 1, wind_speed: 50,
        power: 5000, voltage: 100, current: 100, efficiency: 1,
        daily_energy: 100
      }
      return maxs[key] || 1000
    },
    
    async applyManualSensors() {
      try {
        const response = await axios.post('/api/sensor/update', {
          position: this.manualSensorData.vehicle.odometer || 0,
          sensor_data: this.manualSensorData
        })
        if (response.data.status === 'success') {
          this.sensorData = { ...this.manualSensorData, road: this.sensorData.road }
          this.addEvent('info', '传感器数据已手动更新')
        }
      } catch (error) {
        console.error('应用手动传感器失败:', error)
        this.addEvent('error', '传感器数据更新失败')
      }
    },
    
    resetManualSensors() {
      this.sensorMode = 'auto'
      this.addEvent('info', '已切换回自动传感器模式')
    },
    
    addEvent(type, message) {
      const event = {
        type,
        message,
        timestamp: new Date().toLocaleTimeString('zh-CN', { 
          hour12: false,
          hour: '2-digit',
          minute: '2-digit',
          second: '2-digit'
        })
      }
      this.events.unshift(event)
      if (this.events.length > 20) {
        this.events = this.events.slice(0, 20)
      }
    },
    
    getLogClass(type) {
      const classes = {
        info: 'text-info',
        warning: 'text-warning',
        error: 'text-error',
        success: 'text-success'
      }
      return classes[type] || 'text-info'
    },
    
    toggleTheme() {
      this.isDarkTheme = !this.isDarkTheme
      const html = document.documentElement
      if (this.isDarkTheme) {
        html.setAttribute('data-theme', 'dark')
      } else {
        html.setAttribute('data-theme', 'light')
      }
      // 保存主题设置到本地存储
      localStorage.setItem('theme', this.isDarkTheme ? 'dark' : 'light')
    },
    
    loadTheme() {
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme === 'dark') {
        this.isDarkTheme = true
        document.documentElement.setAttribute('data-theme', 'dark')
      } else {
        this.isDarkTheme = false
        document.documentElement.setAttribute('data-theme', 'light')
      }
    }
  }
}
</script>

<style scoped>
/* DaisyUI会处理大部分样式，只需要少量自定义 */
.radial-progress {
  --size: 6rem;
  --thickness: 6px;
}

/* 自定义动画和效果 */
@keyframes glow {
  0%, 100% { box-shadow: 0 0 5px rgba(59, 130, 246, 0.5); }
  50% { box-shadow: 0 0 20px rgba(59, 130, 246, 0.8); }
}

.btn-primary {
  animation: glow 2s ease-in-out infinite;
}

.card:hover {
  transform: translateY(-2px);
}

.stats .stat:hover {
  transform: scale(1.02);
}

/* 渐变文本效果 */
.gradient-text {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 滚动条美化 */
.overflow-y-auto::-webkit-scrollbar {
  width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
  background: rgba(0, 0, 0, 0.3);
  border-radius: 3px;
}

.overflow-y-auto::-webkit-scrollbar-thumb:hover {
  background: rgba(0, 0, 0, 0.5);
}
</style>
