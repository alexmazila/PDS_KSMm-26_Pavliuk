#!/usr/bin/env python3
import random
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class SensorNode(Node):
    def __init__(self):
        super().__init__('sensor_node')
        
        # Publisher на /sensor_data з типом std_msgs/msg/Float32
        self.publisher_ = self.create_publisher(Float32, '/sensor_data', 10)
        
        # Періодичність 10 Гц (інтервал 0.1 секунди)
        self.timer_period = 0.1 
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        
        # Буфер для усереднення (фільтрації) даних (наприклад, останні 5 вимірювань)
        self.window_size = 5
        self.readings_buffer = []
        
        # Порогове значення (наприклад, дистанція до перешкоди < 0.5 м)
        self.threshold = 0.5
        
        self.get_logger().info('Sensor Node успішно запущено. Публікація у /sensor_data на частоті 10 Гц.')

    def timer_callback(self):
        # Генерація тестових даних (імітація сенсора в діапазоні від 0.1 до 2.0)
        raw_value = round(random.uniform(0.1, 2.0), 2)
        
        # Реалізація усереднення значень (рухоме середнє)
        self.readings_buffer.append(raw_value)
        if len(self.readings_buffer) > self.window_size:
            self.readings_buffer.pop(0)
        
        filtered_value = sum(self.readings_buffer) / len(self.readings_buffer)
        filtered_value = round(filtered_value, 2)
        
        # Перевірка порогового значення та виведення WARN у разі перевищення
        if filtered_value < self.threshold:
            self.get_logger().warning(
                f'УВАГА! Критичне значення сенсора! Сире: {raw_value}, Усереднене: {filtered_value} (Поріг: {self.threshold})'
            )
        else:
            self.get_logger().info(f'Сире значення: {raw_value} | Усереднене (фільтроване): {filtered_value}')

        # Публікація відфільтрованого значення у топік /sensor_data
        msg = Float32()
        msg.data = float(filtered_value)
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = SensorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()