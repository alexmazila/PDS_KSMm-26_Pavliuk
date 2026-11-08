#!/usr/bin/env python3
import csv
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MotionPlayerNode(Node):
    def __init__(self):
        super().__init__('motion_player_node')
        
        # Publisher на /cmd_vel
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.filename = 'motion_scenario.csv'
        
        # Затримка для ініціалізації з'єднання топіків
        time.sleep(1.0)
        self.play_scenario()

    def play_scenario(self):
        try:
            with open(self.filename, mode='r') as file:
                reader = csv.DictReader(file)
                previous_time = 0.0
                
                self.get_logger().info('Початок відтворення сценарію руху...')
                
                for row in reader:
                    timestamp = float(row['timestamp'])
                    linear_x = float(row['linear_x'])
                    angular_z = float(row['angular_z'])
                    
                    # 5.1 & 5.2: Реалізація затримки між командами (синхронізація часу)
                    delay = timestamp - previous_time
                    if delay > 0:
                        time.sleep(delay)
                    
                    # Відправка команди у /cmd_vel
                    msg = Twist()
                    msg.linear.x = linear_x
                    msg.angular.z = angular_z
                    self.publisher_.publish(msg)
                    
                    self.get_logger().info(f'Відтворено -> Час: {timestamp}s | lin.x: {linear_x} | ang.z: {angular_z}')
                    previous_time = timestamp
                    
                # Зупинка робота після завершення сценарію
                stop_msg = Twist()
                self.publisher_.publish(stop_msg)
                self.get_logger().info('Сценарій успішно відтворено. Робот зупинений.')
                
        except FileNotFoundError:
            self.get_logger().error(f'Файл сценарію {self.filename} не знайдено!')

def main(args=None):
    rclpy.init(args=args)
    node = MotionPlayerNode()
    rclpy.shutdown()

if __name__ == '__main__':
    main()