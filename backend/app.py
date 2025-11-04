# -*- coding: utf-8 -*-
"""
SolarBoost Flask 后端服务
提供能量预测和调度API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import random

from models import EnergyDemandPredictor, SolarPowerPredictor, DispatchStrategy
from road_simulator import RoadSegmentSimulator

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 初始化模型和策略
energy_predictor = EnergyDemandPredictor()
solar_predictor = SolarPowerPredictor()
dispatch_strategy = DispatchStrategy()
road_simulator = RoadSegmentSimulator()

# 系统状态
system_state = {
    'mode': 'auto',
    'last_command': None,
    'last_update': None,
    'events': []
}


def add_event(event_type, message):
    """添加事件日志"""
    event = {
        'type': event_type,  # info, warning, error
        'message': message,
        'timestamp': datetime.now().strftime('%H:%M:%S')
    }
    system_state['events'].insert(0, event)
    # 只保留最近50条
    if len(system_state['events']) > 50:
        system_state['events'] = system_state['events'][:50]


@app.route('/api/ingest', methods=['POST'])
def ingest():
    """
    接收车辆、环境、光伏数据，返回预测和调度指令
    
    请求体示例:
    {
        "vehicle": {"speed": 50, "accel": 0.4, "motor_power": 12000, "soc": 0.65, "aux_power": 800},
        "env": {"grade": 0.03, "hour": 14, "temp": 23, "cloud": 0.2, "lat": 29.87, "lon": 121.55},
        "pv": {"temp": 35, "historical_mean": 1200}
    }
    """
    try:
        data = request.get_json()
        
        vehicle_data = data.get('vehicle', {})
        env_data = data.get('env', {})
        pv_data = data.get('pv', {})
        
        # 1. 能耗预测
        energy_prediction = energy_predictor.predict(vehicle_data, env_data)
        
        # 2. 光伏预测
        solar_prediction = solar_predictor.predict(env_data, pv_data)
        
        # 3. 能量调度
        dispatch_command = dispatch_strategy.dispatch(
            energy_prediction['predicted_motor_power'],
            energy_prediction['predicted_aux_power'],
            solar_prediction['predicted_pv_power'],
            vehicle_data,
            env_data
        )
        
        # 更新系统状态
        system_state['last_command'] = dispatch_command
        system_state['last_update'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # 记录事件
        add_event('info', f"调度指令: {dispatch_command['reason']}")
        
        # 检查异常情况
        if solar_prediction['predicted_pv_power'] < 100:
            add_event('warning', '太阳能功率较低，主要依靠电池供电')
        
        if vehicle_data.get('soc', 1.0) < 0.2:
            add_event('warning', 'SOC低于20%，建议尽快充电')
        
        response = {
            'status': 'success',
            'predictions': {
                'energy': energy_prediction,
                'solar': solar_prediction
            },
            'dispatch': dispatch_command,
            'timestamp': system_state['last_update']
        }
        
        return jsonify(response)
        
    except Exception as e:
        add_event('error', f'数据处理错误: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/mode', methods=['POST'])
def set_mode():
    """
    切换系统模式
    
    请求体示例:
    {
        "mode": "auto"  // auto, manual, eco, performance
    }
    """
    try:
        data = request.get_json()
        mode = data.get('mode')
        
        if not mode:
            return jsonify({'status': 'error', 'message': '缺少mode参数'}), 400
        
        if dispatch_strategy.set_mode(mode):
            system_state['mode'] = mode
            add_event('info', f'切换到{mode}模式')
            return jsonify({'status': 'success', 'mode': mode})
        else:
            return jsonify({'status': 'error', 'message': '无效的模式'}), 400
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/command', methods=['POST'])
def manual_command():
    """
    手动模式下发送自定义功率分配指令
    
    请求体示例:
    {
        "to_motor": 500,
        "to_aux": 300,
        "to_charge": 200
    }
    """
    try:
        data = request.get_json()
        
        # 验证参数
        to_motor = data.get('to_motor', 0)
        to_aux = data.get('to_aux', 0)
        to_charge = data.get('to_charge', 0)
        
        if any(v < 0 for v in [to_motor, to_aux, to_charge]):
            return jsonify({'status': 'error', 'message': '功率值不能为负'}), 400
        
        dispatch_strategy.set_manual_command(data)
        add_event('info', f'手动指令: 动力{to_motor}W, 附件{to_aux}W, 充电{to_charge}W')
        
        return jsonify({'status': 'success', 'command': data})
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/state', methods=['GET'])
def get_state():
    """
    获取当前系统状态
    """
    try:
        return jsonify({
            'status': 'success',
            'state': system_state
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查"""
    return jsonify({'status': 'ok', 'service': 'SolarBoost API'})


@app.route('/api/sensor/simulate', methods=['POST'])
def simulate_sensor():
    """
    模拟传感器数据（基于路段）
    """
    try:
        data = request.get_json() or {}
        dt = data.get('dt', 2.0)
        
        # 生成传感器数据
        sensor_data = road_simulator.simulate_step(dt)
        
        return jsonify({
            'status': 'success',
            'data': sensor_data
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/sensor/update', methods=['POST'])
def update_sensor():
    """
    手动更新传感器数据
    
    请求体示例:
    {
        "position": 5000,
        "sensor_data": {
            "vehicle": {...},
            "gps": {...},
            "env": {...},
            "pv": {...}
        }
    }
    """
    try:
        data = request.get_json()
        
        # 处理位置更新
        if 'position' in data:
            road_simulator.set_position(data['position'])
        
        # 处理手动传感器数据
        if 'sensor_data' in data:
            manual_data = data['sensor_data']
            
            # 更新路段模拟器的状态
            if 'vehicle' in manual_data:
                vehicle_data = manual_data['vehicle']
                if 'speed' in vehicle_data:
                    road_simulator.last_speed = vehicle_data['speed']
                if 'odometer' in vehicle_data:
                    road_simulator.current_position = vehicle_data['odometer']
            
            # 可以在这里添加更多手动数据处理逻辑
            add_event('info', '传感器数据已手动更新')
        
        # 生成并返回当前传感器数据
        current_segment = road_simulator.get_current_segment()
        sensor_data = road_simulator.generate_sensor_data(
            current_segment[1],
            road_simulator.last_speed if hasattr(road_simulator, 'last_speed') else 0,
            0,
            2.0
        )
        
        return jsonify({
            'status': 'success',
            'data': sensor_data
        })
    except Exception as e:
        add_event('error', f'传感器更新失败: {str(e)}')
        return jsonify({'status': 'error', 'message': str(e)}), 400


@app.route('/api/road/info', methods=['GET'])
def get_road_info():
    """
    获取道路信息
    """
    try:
        return jsonify({
            'status': 'success',
            'segments': road_simulator.segments,
            'total_length': road_simulator.total_length,
            'current_position': road_simulator.current_position
        })
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400


if __name__ == '__main__':
    add_event('info', 'SolarBoost 系统启动')
    print('=' * 60)
    print('🌞 SolarBoost 智能太阳能调度系统')
    print('=' * 60)
    print('后端服务启动在: http://localhost:5000')
    print('API 端点:')
    print('  - POST /api/ingest   : 数据采集与调度')
    print('  - POST /api/mode     : 切换模式')
    print('  - POST /api/command  : 手动控制')
    print('  - GET  /api/state    : 获取状态')
    print('=' * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
