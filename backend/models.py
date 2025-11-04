# -*- coding: utf-8 -*-
"""
模拟的机器学习模型
使用简单的规则和随机值模拟预测
"""

import random
import math


class EnergyDemandPredictor:
    """能耗预测模型（模拟）"""
    
    def predict(self, vehicle_data, env_data):
        """
        预测未来30秒的功率需求
        
        参数:
            vehicle_data: 车辆数据字典
            env_data: 环境数据字典
            
        返回:
            预测的动力功率和附件功率（单位：W）
        """
        speed = vehicle_data.get('speed', 0)
        accel = vehicle_data.get('accel', 0)
        grade = env_data.get('grade', 0)
        
        # 基础功率 + 速度相关 + 加速度相关 + 坡度相关
        base_power = 5000
        speed_factor = speed * 100
        accel_factor = max(0, accel) * 15000
        grade_factor = max(0, grade) * 30000
        
        # 添加随机波动
        noise = random.uniform(-500, 500)
        
        motor_power = base_power + speed_factor + accel_factor + grade_factor + noise
        motor_power = max(0, min(50000, motor_power))  # 限制在0-50kW
        
        # 附件功率相对稳定
        aux_power = random.uniform(600, 1200)
        
        return {
            'predicted_motor_power': round(motor_power, 2),
            'predicted_aux_power': round(aux_power, 2),
            'confidence': random.uniform(0.75, 0.95)
        }


class SolarPowerPredictor:
    """光伏发电预测模型（模拟）"""
    
    def predict(self, env_data, pv_data):
        """
        预测未来5-15分钟的光伏功率
        
        参数:
            env_data: 环境数据字典
            pv_data: 光伏数据字典
            
        返回:
            预测的光伏功率（单位：W）
        """
        hour = env_data.get('hour', 12)
        cloud = env_data.get('cloud', 0.5)
        temp = env_data.get('temp', 25)
        historical_mean = pv_data.get('historical_mean', 1000)
        
        # 基于时间的太阳辐射强度（简化的正弦曲线）
        # 假设太阳在6:00升起，18:00落下，12:00最强
        if hour < 6 or hour > 18:
            solar_intensity = 0
        else:
            # 正弦曲线模拟
            solar_angle = (hour - 6) / 12 * math.pi
            solar_intensity = math.sin(solar_angle)
        
        # 云量影响
        cloud_factor = 1 - cloud * 0.7
        
        # 温度影响（温度越高，效率略微下降）
        temp_factor = 1 - (temp - 25) * 0.002
        
        # 历史平均值作为基准
        max_power = 2000  # 假设最大功率2kW
        predicted_power = max_power * solar_intensity * cloud_factor * temp_factor
        
        # 添加随机波动
        noise = random.uniform(-50, 50)
        predicted_power = max(0, predicted_power + noise)
        
        return {
            'predicted_pv_power': round(predicted_power, 2),
            'confidence': random.uniform(0.70, 0.90)
        }


class DispatchStrategy:
    """能量调度策略"""
    
    def __init__(self):
        self.mode = 'auto'  # auto, manual, eco, performance
        self.manual_command = None
        
    def set_mode(self, mode):
        """设置调度模式"""
        if mode in ['auto', 'manual', 'eco', 'performance']:
            self.mode = mode
            return True
        return False
    
    def set_manual_command(self, command):
        """设置手动控制指令"""
        self.manual_command = command
        
    def dispatch(self, predicted_motor_power, predicted_aux_power, predicted_pv_power, 
                 vehicle_data, env_data):
        """
        执行能量调度
        
        返回:
            调度指令字典
        """
        if self.mode == 'manual' and self.manual_command:
            return self._manual_dispatch()
        
        available_pv_power = predicted_pv_power
        soc = vehicle_data.get('soc', 0.5)
        
        if self.mode == 'eco':
            return self._eco_dispatch(available_pv_power, predicted_motor_power, 
                                     predicted_aux_power, soc)
        elif self.mode == 'performance':
            return self._performance_dispatch(available_pv_power, predicted_motor_power, 
                                             predicted_aux_power, soc)
        else:  # auto
            return self._auto_dispatch(available_pv_power, predicted_motor_power, 
                                      predicted_aux_power, soc, vehicle_data)
    
    def _auto_dispatch(self, pv_power, motor_power, aux_power, soc, vehicle_data):
        """自动模式：根据场景智能分配"""
        accel = vehicle_data.get('accel', 0)
        speed = vehicle_data.get('speed', 0)
        
        to_motor = 0
        to_aux = 0
        to_charge = 0
        
        # 场景1：高能耗场景（加速或高速）
        if accel > 0.5 or speed > 80:
            # 太阳能优先辅助动力
            to_motor = min(pv_power * 0.7, motor_power * 0.3)
            remaining = pv_power - to_motor
            to_aux = min(remaining, aux_power)
            to_charge = max(0, remaining - to_aux)
            reason = "高能耗场景：太阳能优先辅助动力系统"
            
        # 场景2：低速巡航
        elif speed < 30:
            # 太阳能优先供给附件
            to_aux = min(pv_power, aux_power)
            remaining = pv_power - to_aux
            to_charge = remaining
            reason = "低速巡航：太阳能优先供给附件并充电"
            
        # 场景3：正常行驶
        else:
            # 平衡分配
            to_aux = min(pv_power * 0.5, aux_power)
            remaining = pv_power - to_aux
            to_motor = min(remaining * 0.3, motor_power * 0.2)
            to_charge = remaining - to_motor
            reason = "正常行驶：平衡分配太阳能"
        
        return {
            'to_motor': round(to_motor, 2),
            'to_aux': round(to_aux, 2),
            'to_charge': round(to_charge, 2),
            'mode': 'auto',
            'reason': reason
        }
    
    def _eco_dispatch(self, pv_power, motor_power, aux_power, soc):
        """节能模式：最大化太阳能利用，优先充电"""
        to_aux = min(pv_power * 0.4, aux_power)
        remaining = pv_power - to_aux
        
        if soc < 0.8:
            # SOC较低时优先充电
            to_charge = remaining * 0.8
            to_motor = remaining * 0.2
        else:
            to_charge = remaining * 0.6
            to_motor = remaining * 0.4
            
        return {
            'to_motor': round(to_motor, 2),
            'to_aux': round(to_aux, 2),
            'to_charge': round(to_charge, 2),
            'mode': 'eco',
            'reason': '节能模式：优先充电和附件供电'
        }
    
    def _performance_dispatch(self, pv_power, motor_power, aux_power, soc):
        """性能模式：优先动力系统"""
        to_motor = pv_power * 0.6
        to_aux = min(pv_power * 0.3, aux_power)
        to_charge = pv_power - to_motor - to_aux
        
        return {
            'to_motor': round(to_motor, 2),
            'to_aux': round(to_aux, 2),
            'to_charge': round(to_charge, 2),
            'mode': 'performance',
            'reason': '性能模式：太阳能优先辅助动力'
        }
    
    def _manual_dispatch(self):
        """手动模式：使用用户指定的分配"""
        cmd = self.manual_command
        return {
            'to_motor': cmd.get('to_motor', 0),
            'to_aux': cmd.get('to_aux', 0),
            'to_charge': cmd.get('to_charge', 0),
            'mode': 'manual',
            'reason': '手动模式：用户自定义分配'
        }
