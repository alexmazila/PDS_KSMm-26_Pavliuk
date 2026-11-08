#!/usr/bin/env python3
import csv
import time
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MotionRecorderNode(Node):
    def __init__(self):
        super().__init__('motion_recorder_node')
        
        # 2.2 & 2.3: Підписка на /cmd_vel з типом geometry_msgs/msg/Twist
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )
        
        self.filename = 'motion_scenario.csv'
        self.file = open(self.filename, mode='w', newline='')
        self.writer = csv.writer(self.file)
        
        # Запис заголовка CSV файлу
        self.writer.writerow(['timestamp', 'linear_x', 'angular_z'])
        
        self.start_time = time.time()
        self.get_logger().info(f'Запис розпочато. Дані зберігаються у файл: {self.filename}')

    def cmd_vel_callback(self, msg: Twist):
        # 3.1: Фіксація часу від початку запису та значень швидкостей
        current_time = time.time() - self.start_time
        linear_x = msg.linear.x
        angular_z = msg.angular.z
        
        # 3.2: Збереження у файл
        self.writer.writerow([round(current_time, 4), linear_x, angular_z])
        self.file.flush()
        
        self.get_logger().info(f'Записано -> Час: {current_time:.2f}s | lin.x: {linear_x} | ang.z: {angular_z}')

    def destroy_node(self):
        self.file.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = MotionRecorderNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Запис зупинено користувачем.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()