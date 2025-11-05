<template>
    <div class="min-h-screen bg-base-100">
    <!-- 顶部导航栏 -->
    <div class="bg-base-100 border-b border-base-300 shadow-sm">
      <div class="max-w-[1920px] mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-8">
            <!-- Logo -->
            <div class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                <span class="text-white font-bold text-sm">SB</span>
              </div>
              <div>
                <h1 class="text-xl font-semibold text-base-content">SolarBoost</h1>
                <p class="text-xs text-base-content/60">智能太阳能调度系统</p>
              </div>
            </div>

            <!-- 模拟速度控制 -->
            <div class="flex items-center space-x-3">
              <span class="text-sm font-medium text-base-content">模拟速度</span>
              <div class="flex bg-base-200 rounded-lg p-1">
                <button
                  :class="[
                    'px-3 py-1 text-sm font-medium rounded-md transition-all duration-200',
                    simulationSpeed === 1
                      ? 'bg-primary text-primary-content shadow-sm'
                      : 'text-base-content/70 hover:text-base-content hover:bg-base-300'
                  ]"
                  @click="setSimulationSpeed(1)"
                >
                  快速
                </button>
                <button
                  :class="[
                    'px-3 py-1 text-sm font-medium rounded-md transition-all duration-200',
                    simulationSpeed === 2
                      ? 'bg-primary text-primary-content shadow-sm'
                      : 'text-base-content/70 hover:text-base-content hover:bg-base-300'
                  ]"
                  @click="setSimulationSpeed(2)"
                >
                  正常
                </button>
                <button
                  :class="[
                    'px-3 py-1 text-sm font-medium rounded-md transition-all duration-200',
                    simulationSpeed === 5
                      ? 'bg-primary text-primary-content shadow-sm'
                      : 'text-base-content/70 hover:text-base-content hover:bg-base-300'
                  ]"
                  @click="setSimulationSpeed(5)"
                >
                  缓慢
                </button>
              </div>
            </div>

            <!-- 驱动模式选择 -->
            <div class="flex items-center space-x-3">
              <span class="text-sm font-medium text-base-content">驱动模式</span>
              <div class="flex bg-base-200 rounded-lg p-1">
                <button
                  v-for="mode in modes"
                  :key="mode.value"
                  :class="[
                    'px-4 py-2 text-sm font-medium rounded-md transition-all duration-200 flex items-center space-x-2',
                    currentMode === mode.value
                      ? 'bg-primary text-primary-content shadow-sm'
                      : 'text-base-content/70 hover:text-base-content hover:bg-base-300'
                  ]"
                  @click="switchMode(mode.value)"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path v-if="mode.icon === 'brain'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
                    <path v-else-if="mode.icon === 'leaf'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z"></path>
                    <path v-else-if="mode.icon === 'zap'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
                    <path v-else-if="mode.icon === 'settings'" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"></path>
                    <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  <span>{{ mode.name }}</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 右侧状态栏 -->
          <div class="flex items-center space-x-6">
            <!-- 主题切换 -->
            <button
              class="p-2 text-base-content/70 hover:text-base-content hover:bg-base-300 rounded-lg transition-colors duration-200"
              @click="toggleTheme"
              :title="isDarkTheme ? '切换到亮色主题' : '切换到暗色主题'"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path v-if="isDarkTheme" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"></path>
                <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"></path>
              </svg>
            </button>

            <!-- 状态卡片 -->
            <div class="flex space-x-4">
              <div class="bg-base-100 border border-base-300 rounded-lg px-4 py-2 shadow-sm">
                <div class="text-sm text-base-content/60 uppercase tracking-wide">电池SOC</div>
                <div class="text-xl font-semibold text-base-content">
                  {{ (sensorData.vehicle?.soc * 100 || 0).toFixed(1) }}%
                </div>
              </div>
              <div class="bg-base-100 border border-base-300 rounded-lg px-4 py-2 shadow-sm">
                <div class="text-sm text-base-content/60 uppercase tracking-wide">光伏功率</div>
                <div class="text-xl font-semibold text-warning">
                  {{ sensorData.pv?.power || 0 }}W
                </div>
              </div>
              <div class="bg-base-100 border border-base-300 rounded-lg px-4 py-2 shadow-sm">
                <div class="text-sm text-base-content/60 uppercase tracking-wide">当前模式</div>
                <div class="text-xl font-semibold text-primary">
                  {{ modeText }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="flex-1 overflow-y-auto bg-base-100">
      <div class="max-w-[1920px] mx-auto p-6">
        <!-- 第一行：路网和能量流动图 -->
        <div class="grid grid-cols-3 gap-6 mb-6">
          <!-- 路网与车辆位置 (占2列) -->
          <div class="col-span-2 bg-base-100 rounded-xl shadow-sm border border-base-300 overflow-hidden">
            <div class="p-6">
              <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-semibold text-base-content">路网与车辆位置</h2>
                <div class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium">
                  {{ sensorData.road?.segment_name || '-' }}
                </div>
              </div>
              <div class="w-full overflow-hidden rounded-lg bg-gray-900" style="height: 280px;">
                <canvas ref="roadCanvas" style="width: 100%; height: 100%;"></canvas>
              </div>
              <div class="flex justify-between items-center mt-4 text-base text-base-content/70">
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 bg-red-500 rounded-full"></div>
                  <span>速度: {{ sensorData.vehicle?.speed?.toFixed(1) || 0 }} km/h</span>
                </div>
                <div class="flex items-center space-x-2">
                  <div class="w-2 h-2 bg-green-500 rounded-full"></div>
                  <span>进度: {{ ((sensorData.road?.position / sensorData.road?.total_length * 100) || 0).toFixed(1) }}%</span>
                </div>
              </div>
            </div>
          </div>

          <!-- 能量流动可视化 (占1列) -->
          <div class="card bg-base-100 shadow-xl">
            <div class="card-body">
              <h2 class="card-title">
                能量流动可视化
              </h2>
              <div class="flex gap-6 py-4">
                <!-- 左侧：太阳能输入和能量平衡 -->
                <div class="flex flex-col items-center justify-center space-y-4 flex-1">
                  <!-- 太阳能源输入 -->
                  <div class="flex flex-col items-center">
                    <div class="text-center">
                      <div class="font-bold text-xl text-primary">{{ sensorData.pv?.power || 0 }}W</div>
                      <div class="text-sm opacity-70">太阳能输入</div>
                    </div>
                  </div>

                  <!-- 总能量平衡 -->
                  <div class="w-full bg-base-200 p-4 rounded-lg">
                    <div class="text-center">
                      <div class="text-base font-medium mb-3">能量平衡</div>
                      <div class="grid grid-cols-1 gap-3 text-base">
                        <div class="flex justify-between">
                          <span>输入:</span>
                          <span class="font-mono text-success">{{ sensorData.pv?.power?.toFixed(0) || 0 }}W</span>
                        </div>
                        <div class="flex justify-between">
                          <span>输出:</span>
                          <span class="font-mono text-info">{{ (dispatchCommand.to_motor + dispatchCommand.to_aux + dispatchCommand.to_charge || 0).toFixed(0) }}W</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 右侧：能量分配详情 -->
                <div class="flex-1 space-y-3">
                  <!-- 动力系统 -->
                  <div class="bg-base-200 p-4 rounded-lg border-l-4 border-primary">
                    <div class="flex justify-between items-center mb-2">
                      <span class="text-base font-medium">动力系统</span>
                      <span class="text-base font-mono text-primary">{{ dispatchCommand.to_motor?.toFixed(0) || 0 }}W</span>
                    </div>
                    <div class="w-full h-4 bg-base-300 rounded-full overflow-hidden mb-2">
                      <div class="h-full bg-primary transition-all duration-300"
                           :style="`width: ${getFlowWidth('motor')}%`"></div>
                    </div>
                    <div class="text-sm opacity-70">实际需求: {{ predictions.energy?.predicted_motor_power?.toFixed(0) || 0 }}W</div>
                  </div>

                  <!-- 附件系统 -->
                  <div class="bg-base-200 p-4 rounded-lg border-l-4 border-secondary">
                    <div class="flex justify-between items-center mb-2">
                      <span class="text-base font-medium">附件系统</span>
                      <span class="text-base font-mono text-secondary">{{ dispatchCommand.to_aux?.toFixed(0) || 0 }}W</span>
                    </div>
                    <div class="w-full h-4 bg-base-300 rounded-full overflow-hidden mb-2">
                      <div class="h-full bg-secondary transition-all duration-300"
                           :style="`width: ${getFlowWidth('aux')}%`"></div>
                    </div>
                    <div class="text-sm opacity-70">实际需求: {{ predictions.energy?.predicted_aux_power?.toFixed(0) || 0 }}W</div>
                  </div>

                  <!-- 电池充电 -->
                  <div class="bg-base-200 p-4 rounded-lg border-l-4 border-accent">
                    <div class="flex justify-between items-center mb-2">
                      <span class="text-base font-medium">电池充电</span>
                      <span class="text-base font-mono text-accent">{{ dispatchCommand.to_charge?.toFixed(0) || 0 }}W</span>
                    </div>
                    <div class="w-full h-4 bg-base-300 rounded-full overflow-hidden mb-2">
                      <div class="h-full bg-accent transition-all duration-300"
                           :style="`width: ${getFlowWidth('charge')}%`"></div>
                    </div>
                    <div class="text-sm opacity-70">SOC: {{ (sensorData.vehicle?.soc * 100 || 0).toFixed(1) }}%</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 第二行：学习过程，传感器数据和日志 -->
        <div class="grid grid-cols-3 gap-6">
          <!-- 机器学习驱动过程 (占1列) -->
          <div class="bg-base-100 rounded-xl shadow-sm border border-base-300 overflow-hidden">
            <div class="p-6">
              <h2 class="text-xl font-semibold text-base-content mb-4">机器学习驱动过程</h2>
              <div class="space-y-4">
                <!-- 能耗预测 -->
                <div class="bg-base-200 p-4 rounded-lg border border-base-300">
                  <h4 class="font-medium text-base text-base-content mb-3">能耗预测</h4>
                  <div class="space-y-3 text-base">
                    <div class="flex justify-between">
                      <span class="text-base-content/70">动力:</span>
                      <span class="font-mono text-primary">{{ predictions.energy?.predicted_motor_power?.toFixed(0) || 0 }}W</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-base-content/70">附件:</span>
                      <span class="font-mono text-secondary">{{ predictions.energy?.predicted_aux_power?.toFixed(0) || 0 }}W</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-base-content/70">信心:</span>
                      <span class="font-mono text-success">{{ ((predictions.energy?.confidence || 0) * 100).toFixed(1) }}%</span>
                    </div>
                  </div>
                </div>

                <!-- 光伏预测 -->
                <div class="bg-base-200 p-4 rounded-lg border border-base-300">
                  <h4 class="font-medium text-base text-base-content mb-3">光伏预测</h4>
                  <div class="space-y-3 text-base">
                    <div class="flex justify-between">
                      <span class="text-base-content/70">功率:</span>
                      <span class="font-mono text-warning">{{ predictions.solar?.predicted_pv_power?.toFixed(0) || 0 }}W</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-base-content/70">信心:</span>
                      <span class="font-mono text-success">{{ ((predictions.solar?.confidence || 0) * 100).toFixed(1) }}%</span>
                    </div>
                    <div class="flex justify-between">
                      <span class="text-base-content/70">效率:</span>
                      <span class="font-mono text-base-content">{{ sensorData.pv?.efficiency ? (sensorData.pv.efficiency * 100).toFixed(1) : 0 }}%</span>
                    </div>
                  </div>
                </div>

                <!-- 决策解释 -->
                <div class="bg-base-200 p-4 rounded-lg border border-base-300">
                  <h4 class="font-medium text-base text-base-content mb-3">决策理由</h4>
                  <div class="text-base">
                    <div class="font-medium text-base-content mb-2">{{ getCurrentScenario() }}</div>
                    <div class="bg-info/10 p-3 rounded-lg text-sm text-base-content border border-info/20">
                      {{ getDecisionExplanation() }}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 传感器数据 (占1列) -->
          <div class="bg-base-100 rounded-xl shadow-sm border border-base-300 overflow-hidden">
            <div class="p-6 max-h-[500px] overflow-y-auto">
              <div class="flex items-center justify-between mb-4">
                <h2 class="text-xl font-semibold text-base-content">传感器数据</h2>
                <div class="flex bg-base-200 rounded-lg p-1">
                  <button
                    :class="[
                      'px-3 py-1 text-sm font-medium rounded-md transition-all duration-200',
                      sensorMode === 'auto'
                        ? 'bg-success text-success-content shadow-sm'
                        : 'text-base-content/70 hover:text-base-content hover:bg-base-300'
                    ]"
                    @click="setSensorMode('auto')"
                  >
                    自动
                  </button>
                  <button
                    :class="[
                      'px-3 py-1 text-sm font-medium rounded-md transition-all duration-200',
                      sensorMode === 'manual'
                        ? 'bg-warning text-warning-content shadow-sm'
                        : 'text-base-content/70 hover:text-base-content hover:bg-base-300'
                    ]"
                    @click="setSensorMode('manual')"
                  >
                    手动
                  </button>
                </div>
              </div>

              <div class="space-y-4">
                <!-- 车辆数据 -->
                <div>
                  <h3 class="text-base font-medium text-base-content mb-3 uppercase tracking-wide">车辆数据</h3>
                  <div class="space-y-3">
                    <div v-for="(value, key) in sensorData.vehicle" :key="key" class="flex items-center justify-between py-2 border-b border-base-300 last:border-b-0">
                      <span class="text-base text-base-content/70">{{ getSensorLabel(key) }}</span>
                      <div class="flex items-center space-x-2">
                        <span class="font-mono text-base text-base-content">{{ formatValue(sensorMode === 'manual' ? manualSensorData.vehicle[key] : value, key) }}</span>
                        <input v-if="sensorMode === 'manual'"
                               type="range"
                               :value="manualSensorData.vehicle[key]"
                               @input="updateManualSensor('vehicle', key, $event.target.value)"
                               :min="getSensorMin(key)"
                               :max="getSensorMax(key)"
                               :step="getSensorStep(key)"
                               class="w-16 h-1 bg-base-300 rounded-lg appearance-none cursor-pointer slider" />
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 环境数据 -->
                <div>
                  <h3 class="text-base font-medium text-base-content mb-3 uppercase tracking-wide">环境数据</h3>
                  <div class="space-y-3">
                    <div v-for="(value, key) in sensorData.env" :key="key" class="flex items-center justify-between py-2 border-b border-base-300 last:border-b-0">
                      <span class="text-base text-base-content/70">{{ getSensorLabel(key) }}</span>
                      <div class="flex items-center space-x-2">
                        <span class="font-mono text-base text-base-content">{{ formatValue(sensorMode === 'manual' ? manualSensorData.env[key] : value, key) }}</span>
                        <input v-if="sensorMode === 'manual' && key !== 'weather'"
                               type="range"
                               :value="manualSensorData.env[key]"
                               @input="updateManualSensor('env', key, $event.target.value)"
                               :min="getSensorMin(key)"
                               :max="getSensorMax(key)"
                               :step="getSensorStep(key)"
                               class="w-16 h-1 bg-base-300 rounded-lg appearance-none cursor-pointer slider" />
                        <select v-if="sensorMode === 'manual' && key === 'weather'"
                                :value="manualSensorData.env[key]"
                                @change="updateManualSensor('env', key, $event.target.value)"
                                class="text-base border border-gray-300 rounded px-2 py-1">
                          <option value="sunny">晴天</option>
                          <option value="cloudy">多云</option>
                          <option value="rainy">雨天</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>

                <div v-if="sensorMode === 'manual'" class="flex justify-end space-x-2 pt-4 border-t border-gray-200">
                  <button class="px-4 py-2 bg-green-500 text-white text-base font-medium rounded-lg hover:bg-green-600 transition-colors duration-200" @click="applyManualSensors">
                    应用
                  </button>
                  <button class="px-4 py-2 bg-base-300 text-base-content text-base font-medium rounded-lg hover:bg-base-content/10 transition-colors duration-200" @click="resetManualSensors">
                    重置
                  </button>
                </div>
              </div>
            </div>
          </div>          <!-- 系统事件日志 (占1列) -->
          <div class="bg-base-100 rounded-xl shadow-sm border border-base-300 overflow-hidden">
            <div class="p-6">
              <h2 class="text-xl font-semibold text-base-content mb-4">系统事件日志</h2>
              <div class="terminal-window max-h-64 overflow-y-auto bg-black text-green-400 font-mono text-base rounded-lg border border-gray-600 shadow-inner">
                <div class="terminal-header bg-gray-800 px-3 py-2 rounded-t-lg flex items-center justify-between">
                  <div class="flex items-center space-x-2">
                    <div class="w-3 h-3 bg-red-500 rounded-full"></div>
                    <div class="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <div class="w-3 h-3 bg-green-500 rounded-full"></div>
                  </div>
                  <div class="text-sm text-base-content/50">SolarBoost Terminal</div>
                  <div class="w-16"></div>
                </div>
                <div class="terminal-content p-3 space-y-1">
                  <div v-for="(event, index) in events" :key="index"
                       :class="[
                         'terminal-line transition-all duration-200 hover:bg-gray-900 px-2 py-1 rounded',
                         getLogClass(event.type)
                       ]">
                    <span class="terminal-prompt text-green-300">$</span>
                    <span class="terminal-timestamp text-base-content/60 ml-2">[{{ event.timestamp }}]</span>
                    <span class="terminal-message ml-2">{{ event.message }}</span>
                  </div>
                  <div v-if="events.length === 0" class="terminal-line text-center py-4 opacity-50">
                    <span class="terminal-prompt text-green-300">$</span>
                    <span class="terminal-message ml-2">No system events recorded...</span>
                  </div>
                  <div class="terminal-line">
                    <span class="terminal-prompt text-green-300">$</span>
                    <span class="terminal-cursor ml-2 animate-pulse">_</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 手动控制面板 (条件显示) -->
        <div v-if="currentMode === 'manual'" class="mt-6">
          <div class="bg-base-100 rounded-xl shadow-sm border border-base-300 overflow-hidden">
            <div class="p-6">
              <h2 class="text-xl font-semibold text-base-content mb-4">手动控制</h2>
              <div class="grid grid-cols-3 gap-6">
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="text-base font-medium text-base-content">动力系统</span>
                    <span class="text-base font-mono text-blue-600">{{ manualCommand.to_motor }}W</span>
                  </div>
                  <input type="range" min="0" :max="sensorData.pv?.power || 2000"
                         v-model.number="manualCommand.to_motor"
                         @input="updateManualCommand"
                         class="w-full h-2 bg-base-300 rounded-lg appearance-none cursor-pointer slider" />
                </div>
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="text-base font-medium text-base-content">附件系统</span>
                    <span class="text-base font-mono text-purple-600">{{ manualCommand.to_aux }}W</span>
                  </div>
                  <input type="range" min="0" :max="sensorData.pv?.power || 2000"
                         v-model.number="manualCommand.to_aux"
                         @input="updateManualCommand"
                         class="w-full h-2 bg-base-300 rounded-lg appearance-none cursor-pointer slider" />
                </div>
                <div class="space-y-3">
                  <div class="flex items-center justify-between">
                    <span class="text-base font-medium text-base-content">电池充电</span>
                    <span class="text-base font-mono text-green-600">{{ manualCommand.to_charge }}W</span>
                  </div>
                  <input type="range" min="0" :max="sensorData.pv?.power || 2000"
                         v-model.number="manualCommand.to_charge"
                         @input="updateManualCommand"
                         class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider" />
                </div>
              </div>
              <div class="mt-6 flex justify-center">
                <button class="px-6 py-3 bg-blue-500 text-white font-medium rounded-lg hover:bg-blue-600 transition-colors duration-200 shadow-sm" @click="applyManualCommand">
                  应用设置
                </button>
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
        { value: 'auto', name: '自动', icon: 'brain' },
        { value: 'eco', name: '节能', icon: 'leaf' },
        { value: 'performance', name: '性能', icon: 'zap' },
        { value: 'manual', name: '手动', icon: 'settings' }
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
    // 设置默认主题为solarboost
    document.documentElement.setAttribute('data-theme', 'solarboost')
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
        this.canvas.height = 300
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
        ctx.font = '20px Arial'
        ctx.textAlign = 'center'
        ctx.fillText(segment.name, x + segmentWidth / 2, y - 10)
        
        ctx.fillStyle = '#ffd700'
        ctx.font = '18px Arial'
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
      
      // 绘制车为方块
      ctx.fillStyle = '#ff6b6b'
      ctx.fillRect(carX - 12, carY - 8, 24, 16)
      
      // 车轮
      ctx.fillStyle = '#333'
      ctx.fillRect(carX - 10, carY + 8, 4, 3)
      ctx.fillRect(carX + 6, carY + 8, 4, 3)
      
      ctx.fillStyle = '#ffffff'
      ctx.font = 'bold 16px Arial'
      ctx.textAlign = 'center'
      ctx.fillText('🚗', carX, carY - 25)
      
      const speed = this.sensorData.vehicle?.speed || 0
      ctx.fillStyle = '#4caf50'
      ctx.font = 'bold 24px Arial'
      ctx.fillText(`${speed.toFixed(1)} km/h`, carX, carY + 45)
      
      const pvPower = this.sensorData.pv?.power || 0
      if (pvPower > 100) {
        ctx.fillStyle = '#ffd700'
        ctx.beginPath()
        ctx.arc(carX, carY - 5, 10, 0, Math.PI * 2)
        ctx.fill()
        ctx.fillStyle = '#000'
        ctx.font = '14px Arial'
        ctx.fillText('☀️', carX, carY - 2)
      }
      
      ctx.fillStyle = 'rgba(76, 175, 80, 0.3)'
      ctx.fillRect(margin, y + roadHeight + 35, (width - 2 * margin) * (currentPos / totalLength), 10)
      ctx.strokeStyle = '#4caf50'
      ctx.strokeRect(margin, y + roadHeight + 35, width - 2 * margin, 10)
      
      ctx.fillStyle = '#4caf50'
      ctx.font = '20px Arial'
      ctx.textAlign = 'right'
      ctx.fillText(`进度: ${((currentPos / totalLength) * 100).toFixed(1)}%`, width - margin, y + roadHeight + 65)
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
        html.setAttribute('data-theme', 'solarboost')
      }
      // 保存主题设置到本地存储
      localStorage.setItem('theme', this.isDarkTheme ? 'dark' : 'solarboost')
    },
    
    loadTheme() {
      const savedTheme = localStorage.getItem('theme')
      if (savedTheme === 'dark') {
        this.isDarkTheme = true
        document.documentElement.setAttribute('data-theme', 'dark')
      } else {
        this.isDarkTheme = false
        document.documentElement.setAttribute('data-theme', 'solarboost')
      }
    },
    
    getCurrentScenario() {
      const speed = this.sensorData.vehicle?.speed || 0
      const accel = this.sensorData.vehicle?.accel || 0
      
      if (accel > 0.5 || speed > 80) return '高能耗场景（加速/高速）'
      if (speed < 30) return '低速巡航'
      return '正常行驶'
    },
    
    getOptimizationGoal() {
      const mode = this.dispatchCommand.mode
      if (mode === 'eco') return '最大化太阳能利用，优先充电'
      if (mode === 'performance') return '优先动力系统性能'
      if (mode === 'manual') return '用户自定义控制'
      return '智能平衡分配能源'
    },
    
    getDecisionExplanation() {
      const mode = this.dispatchCommand.mode
      const speed = this.sensorData.vehicle?.speed || 0
      const accel = this.sensorData.vehicle?.accel || 0
      const soc = this.sensorData.vehicle?.soc || 0.5
      
      if (mode === 'auto') {
        if (accel > 0.5 || speed > 80) {
          return '检测到高能耗场景，机器学习模型预测需要大量动力功率。系统优先分配太阳能辅助动力系统，同时保证附件系统基本供电，剩余能源用于电池充电，以维持车辆性能。'
        } else if (speed < 30) {
          return '当前处于低速巡航状态，能耗相对较低。机器学习模型建议优先为附件系统供电并补充电池电量，充分利用太阳能资源，提高整体能源效率。'
        } else {
          return '正常行驶状态下，基于历史数据和实时传感器输入，机器学习模型采用平衡策略：适度辅助动力系统、保证附件供电、适量充电，实现能源的最优分配。'
        }
      } else if (mode === 'eco') {
        return '节能模式激活。机器学习优化算法优先考虑长期能源效率，根据电池SOC状态智能分配太阳能：SOC较低时优先充电，SOC充足时平衡各系统需求。'
      } else if (mode === 'performance') {
        return '性能模式激活。机器学习模型分析当前驾驶条件，优先为动力系统分配太阳能资源，确保车辆在各种工况下都能获得最佳性能表现。'
      } else {
        return '手动控制模式。用户根据具体需求自定义能源分配策略，系统将严格按照用户指令执行调度。'
      }
    }
  }
}
</script>

<style scoped>
/* 自定义滑块样式 */
.slider::-webkit-slider-thumb {
  appearance: none;
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
}

.slider::-webkit-slider-thumb:hover {
  background: #2563eb;
  transform: scale(1.1);
}

.slider::-moz-range-thumb {
  height: 16px;
  width: 16px;
  border-radius: 50%;
  background: #3b82f6;
  cursor: pointer;
  border: 2px solid #ffffff;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.2);
}

.slider::-moz-range-thumb:hover {
  background: #2563eb;
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

/* CLI终端样式 */
.terminal-window {
  font-family: 'Courier New', 'Monaco', 'Menlo', monospace;
  background: #000000;
  color: #00ff00;
  border: 1px solid #333;
  border-radius: 8px;
  overflow: hidden;
}

.terminal-header {
  background: linear-gradient(90deg, #2d2d2d 0%, #3d3d3d 100%);
  border-bottom: 1px solid #555;
}

.terminal-content {
  background: #000000;
  min-height: 150px;
}

.terminal-line {
  display: flex;
  align-items: center;
  font-size: 13px;
  line-height: 1.4;
}

.terminal-prompt {
  color: #00ff00;
  font-weight: bold;
  margin-right: 4px;
}

.terminal-timestamp {
  color: #888;
  font-size: 11px;
}

.terminal-message {
  color: #00ff00;
  flex: 1;
}

.terminal-cursor {
  color: #00ff00;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* 日志类型颜色 */
.terminal-line.info .terminal-message {
  color: #00ff00;
}

.terminal-line.warning .terminal-message {
  color: #ffff00;
}

.terminal-line.error .terminal-message {
  color: #ff4444;
}

.terminal-line.success .terminal-message {
  color: #00ff88;
}

/* 卡片悬停效果 */
.card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

/* 按钮动画 */
.btn:hover {
  transform: translateY(-1px);
}

/* 渐变文本效果 */
.gradient-text {
  background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
</style>
