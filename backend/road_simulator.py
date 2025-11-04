# -*- coding: utf-8 -*-
"""
路段数据模拟系统
基于真实道路场景生成传感器数据
"""

import math
import random


class RoadSegmentSimulator:
    """道路路段模拟器"""
    
    def __init__(self):
        # 定义一条真实的路段（例如：城市主干道 -> 高速公路 -> 山路）
        self.segments = [
            {
                'name': '城市主干道',
                'length': 3000,  # 米
                'speed_limit': 60,  # km/h
                'grade': 0.0,  # 坡度
                'traffic_density': 0.7,  # 交通密度
                'weather': 'sunny'
            },
            {
                'name': '高速公路',
                'length': 5000,
                'speed_limit': 120,
                'grade': 0.02,
                'traffic_density': 0.3,
                'weather': 'sunny'
            },
            {
                'name': '上坡路段',
                'length': 2000,
                'speed_limit': 80,
                'grade': 0.08,
                'traffic_density': 0.2,
                'weather': 'cloudy'
            },
            {
                'name': '下坡路段',
                'length': 2000,
                'speed_limit': 80,
                'grade': -0.05,
                'traffic_density': 0.2,
                'weather': 'cloudy'
            },
            {
                'name': '城市道路',
                'length': 1500,
                'speed_limit': 50,
                'grade': 0.0,
                'traffic_density': 0.8,
                'weather': 'rainy'
            }
        ]
        
        self.total_length = sum(seg['length'] for seg in self.segments)
        self.current_position = 0  # 当前位置（米）
        self.current_segment_index = 0
        self.trip_time = 0  # 行程时间（秒）
    
    def get_current_segment(self):
        """获取当前所在路段"""
        cumulative_length = 0
        for i, segment in enumerate(self.segments):
            cumulative_length += segment['length']
            if self.current_position < cumulative_length:
                return i, segment
        return len(self.segments) - 1, self.segments[-1]
    
    def get_road_position(self):
        """获取道路位置信息（用于可视化）"""
        segment_idx, segment = self.get_current_segment()
        
        # 计算在当前路段的位置
        cumulative_length = sum(seg['length'] for seg in self.segments[:segment_idx])
        position_in_segment = self.current_position - cumulative_length
        progress_in_segment = position_in_segment / segment['length']
        
        return {
            'segment_index': segment_idx,
            'segment_name': segment['name'],
            'position_in_segment': position_in_segment,
            'progress_in_segment': progress_in_segment,
            'total_progress': self.current_position / self.total_length
        }
    
    def simulate_step(self, dt=2.0):
        """
        模拟一步（dt秒）
        返回传感器数据
        """
        segment_idx, segment = self.get_current_segment()
        
        # 基于路段特性生成速度
        target_speed = segment['speed_limit']
        traffic_factor = 1 - segment['traffic_density'] * 0.5
        actual_speed = target_speed * traffic_factor + random.uniform(-5, 5)
        actual_speed = max(0, min(actual_speed, segment['speed_limit']))
        
        # 计算加速度（基于速度变化）
        if hasattr(self, 'last_speed'):
            acceleration = (actual_speed - self.last_speed) / dt
        else:
            acceleration = 0
        self.last_speed = actual_speed
        
        # 更新位置
        distance = actual_speed * 1000 / 3600 * dt  # 转换为米
        self.current_position += distance
        
        # 如果到达终点，重新开始
        if self.current_position >= self.total_length:
            self.current_position = 0
            self.trip_time = 0
        
        self.trip_time += dt
        
        # 生成完整的传感器数据
        return self.generate_sensor_data(segment, actual_speed, acceleration, dt)
    
    def generate_sensor_data(self, segment, speed, acceleration, dt=2.0):
        """生成所有传感器数据"""
        
        # GPS数据（模拟坐标）
        lat = 30.5728 + self.current_position / 111320.0  # 纬度（约）
        lon = 114.2668 + self.current_position / 111320.0 / math.cos(math.radians(lat))
        
        # 环境传感器
        weather_map = {
            'sunny': {'cloud': 0.1, 'temp_base': 28},
            'cloudy': {'cloud': 0.5, 'temp_base': 25},
            'rainy': {'cloud': 0.8, 'temp_base': 22}
        }
        weather_data = weather_map.get(segment['weather'], weather_map['sunny'])
        
        # 动力系统
        motor_power = self._calculate_motor_power(speed, acceleration, segment['grade'])
        battery_consumption = motor_power * 2 / 3600  # Wh per second
        
        # 辅件功率（空调、车机等）
        aux_power = 800 + random.uniform(-100, 100)
        if weather_data['temp_base'] > 26:
            aux_power += 400  # 空调额外功耗
        
        # 太阳能板数据
        hour = int(self.trip_time / 60) % 24 + 8  # 从8点开始
        pv_power = self._calculate_solar_power(hour, weather_data['cloud'], weather_data['temp_base'])
        pv_voltage = 48.0 + random.uniform(-2, 2)
        pv_current = pv_power / pv_voltage if pv_voltage > 0 else 0
        pv_temp = weather_data['temp_base'] + 10 + random.uniform(-2, 2)
        
        # 电池数据 - 基于真实电动车电池 (75kWh容量)
        if not hasattr(self, 'soc'):
            self.soc = 0.85  # 初始SOC 85%
        
        # 计算电池消耗 (考虑电机效率和电池效率)
        battery_efficiency = 0.95  # 电池充放电效率
        energy_consumed_wh = (motor_power / 3600) * dt  # Wh
        battery_energy_used = energy_consumed_wh / battery_efficiency
        
        battery_capacity_wh = 75000  # 75kWh电池
        soc_change = battery_energy_used / battery_capacity_wh
        self.soc = max(0.05, min(1.0, self.soc - soc_change))  # 限制SOC在5%-100%
        
        return {
            'vehicle': {
                'speed': round(speed, 2),
                'accel': round(acceleration, 3),
                'motor_power': round(motor_power, 1),
                'soc': round(self.soc, 3),
                'aux_power': round(aux_power, 1),
                'battery_voltage': round(400 + random.uniform(-5, 5), 2),
                'battery_current': round(motor_power / 400, 2),
                'battery_temp': round(30 + random.uniform(-2, 2), 1),
                'odometer': round(self.current_position, 1)
            },
            'gps': {
                'lat': round(lat, 6),
                'lon': round(lon, 6),
                'altitude': round(100 + self.current_position * segment['grade'], 1),
                'speed': round(speed, 2),
                'heading': round((self.current_position / 100) % 360, 1)
            },
            'env': {
                'grade': segment['grade'],
                'hour': hour,
                'minute': int((self.trip_time % 60)),
                'temp': round(weather_data['temp_base'] + random.uniform(-1, 1), 1),
                'cloud': round(weather_data['cloud'] + random.uniform(-0.05, 0.05), 2),
                'humidity': round(0.5 + random.uniform(-0.1, 0.1), 2),
                'wind_speed': round(random.uniform(0, 5), 1),
                'weather': segment['weather']
            },
            'pv': {
                'power': round(pv_power, 1),
                'voltage': round(pv_voltage, 2),
                'current': round(pv_current, 2),
                'temp': round(pv_temp, 1),
                'efficiency': round(0.18 + random.uniform(-0.02, 0.02), 3),
                'daily_energy': round(pv_power * self.trip_time / 3600, 2)
            },
            'road': {
                'segment_name': segment['name'],
                'segment_index': self.get_current_segment()[0],
                'speed_limit': segment['speed_limit'],
                'traffic_density': segment['traffic_density'],
                'position': round(self.current_position, 1),
                'total_length': self.total_length,
                'progress': round(self.current_position / self.total_length * 100, 1)
            },
            'timestamp': self.trip_time
        }
    
    def _calculate_motor_power(self, speed_kmh, accel, grade):
        """计算电机功率 - 基于真实电动车参数"""
        speed_ms = speed_kmh / 3.6

        # 真实电动车参数 (以Tesla Model 3为例)
        mass = 1800  # 车重1800kg
        frontal_area = 2.2  # 迎风面积 m²
        drag_coeff = 0.23  # 空气阻力系数
        rolling_resistance = 0.012  # 滚动阻力系数

        # 空气阻力功率 (P_air = 0.5 * ρ * Cd * A * v³)
        air_density = 1.225  # kg/m³
        air_power = 0.5 * air_density * drag_coeff * frontal_area * (speed_ms ** 3)

        # 滚动阻力功率 (P_roll = m * g * Cr * v)
        gravity = 9.81
        roll_power = mass * gravity * rolling_resistance * speed_ms

        # 加速功率 (P_accel = m * a * v) - 限制加速功率，避免过高
        accel_power = mass * accel * speed_ms if accel > 0 else 0
        accel_power = min(accel_power, 50000)  # 限制加速功率在50kW以内

        # 爬坡功率 (P_grade = m * g * grade * v) - 坡度通常不会超过10%
        grade_power = mass * gravity * grade * speed_ms

        # 辅助系统功率 (空调、电子系统等)
        aux_base_power = 500  # 基础辅助功率

        total_power = air_power + roll_power + accel_power + grade_power + aux_base_power

        # 考虑电机效率 (约85-90%)
        motor_efficiency = 0.87
        electrical_power = total_power / motor_efficiency

        # 限制在合理范围内 (0-100kW)，避免过高功率
        return max(0, min(electrical_power, 100000))
    
    def _calculate_solar_power(self, hour, cloud_cover, env_temp=25):
        """计算太阳能功率 - 基于真实太阳能板参数"""
        if hour < 6 or hour > 18:
            return 0
        
        # 太阳辐射强度（简化的正弦曲线）
        solar_angle = (hour - 6) / 12 * math.pi
        base_intensity = math.sin(solar_angle)
        
        # 云量影响
        cloud_factor = 1 - cloud_cover * 0.8
        
        # 温度影响 (太阳能板温度约为环境温度+15°C)
        pv_temp = env_temp + 15
        temp_factor = 1 - (pv_temp - 25) / 100
        
        # 太阳能板参数 (假设2m²太阳能板，效率18%)
        panel_area = 2.0  # m²
        panel_efficiency = 0.18
        max_power = 1000 * panel_area * panel_efficiency  # ~360W峰值功率
        
        power = max_power * base_intensity * cloud_factor * temp_factor
        
        # 添加随机波动 (±10%)
        power *= (1 + random.uniform(-0.1, 0.1))
        
        return max(0, power)
    
    def set_position(self, position):
        """手动设置位置（用于控制面板）"""
        self.current_position = max(0, min(position, self.total_length))
    
    def reset(self):
        """重置模拟"""
        self.current_position = 0
        self.trip_time = 0
        self.soc = 0.85
        if hasattr(self, 'last_speed'):
            delattr(self, 'last_speed')
