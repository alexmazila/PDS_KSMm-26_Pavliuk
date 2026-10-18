#!/usr/bin/env python3
import sys
import threading
import tkinter as tk

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String


class RobotGuiNode(Node):
    def __init__(self):
        super().__init__('robot_gui_node')
        
        # Publisher на /cmd_vel для керування
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # ДОДАНО: Publisher на /motion_status для публікації статусу кнопок
        self.status_publisher = self.create_publisher(String, '/motion_status', 10)
        
        # Підписка на топік статусу (для відображення у власному вікні)
        self.subscription = self.create_subscription(
            String,
            '/motion_status',
            self.status_callback,
            10
        )
        
        # Налаштування швидкостей для кнопок
        self.linear_speed = 0.3
        self.angular_speed = 0.6

    def handle_button_press(self, linear_x, angular_z, button_name):
        # 1. Публікуємо швидкість у /cmd_vel
        twist_msg = Twist()
        twist_msg.linear.x = float(linear_x)
        twist_msg.angular.z = float(angular_z)
        self.publisher_.publish(twist_msg)
        
        # 2. Публікуємо назву кнопки у /motion_status
        status_msg = String()
        status_msg.data = f"Натиснуто: {button_name}"
        self.status_publisher.publish(status_msg)
        
        self.get_logger().info(f'Дія: {button_name} -> linear.x: {linear_x}, angular.z: {angular_z}')

    def status_callback(self, msg: String):
        # Метод для передачі статусу у головне вікно GUI
        if hasattr(self, 'update_status_gui'):
            self.update_status_gui(msg.data)


class GuiApp:
    def __init__(self, root, ros_node: RobotGuiNode):
        self.root = root
        self.ros_node = ros_node
        self.root.title("ROS2 Robot GUI Control")
        self.root.geometry("350x400")
        self.root.config(bg="#f0f0f0")

        # Зв'язуємо колбек ROS-ноди з оновленням інтерфейсу
        self.ros_node.update_status_gui = self.display_status

        self.create_widgets()

    def create_widgets(self):
        # Заголовок
        title_label = tk.Label(self.root, text="Керування роботом", font=("Arial", 14, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        # Кнопки керування із прив'язкою назв до /motion_status
        btn_frame = tk.Frame(self.root, bg="#f0f0f0")
        btn_frame.pack(pady=10)

        self.btn_forward = tk.Button(btn_frame, text="▲ Вперед", width=12, height=2, bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                                     command=lambda: self.ros_node.handle_button_press(self.ros_node.linear_speed, 0.0, "Вперед"))
        self.btn_forward.grid(row=0, column=1, padx=5, pady=5)

        self.btn_left = tk.Button(btn_frame, text="◄ Ліворуч", width=12, height=2, bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                                  command=lambda: self.ros_node.handle_button_press(0.0, self.ros_node.angular_speed, "Ліворуч"))
        self.btn_left.grid(row=1, column=0, padx=5, pady=5)

        self.btn_stop = tk.Button(btn_frame, text="⏹ Стоп", width=12, height=2, bg="#f44336", fg="white", font=("Arial", 10, "bold"),
                                  command=lambda: self.ros_node.handle_button_press(0.0, 0.0, "Стоп"))
        self.btn_stop.grid(row=1, column=1, padx=5, pady=5)

        self.btn_right = tk.Button(btn_frame, text="Праворуч ►", width=12, height=2, bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
                                   command=lambda: self.ros_node.handle_button_press(0.0, -self.ros_node.angular_speed, "Праворуч"))
        self.btn_right.grid(row=1, column=2, padx=5, pady=5)

        self.btn_backward = tk.Button(btn_frame, text="▼ Назад", width=12, height=2, bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                                      command=lambda: self.ros_node.handle_button_press(-self.ros_node.linear_speed, 0.0, "Назад"))
        self.btn_backward.grid(row=2, column=1, padx=5, pady=5)

        # Текстове поле для відображення статусу
        status_label = tk.Label(self.root, text="Статус системи:", font=("Arial", 10, "bold"), bg="#f0f0f0")
        status_label.pack(anchor="w", padx=20, pady=(10, 0))

        self.status_text = tk.Text(self.root, height=5, width=38, state=tk.DISABLED, font=("Courier", 9))
        self.status_text.pack(padx=20, pady=5)

    def display_status(self, message):
        self.status_text.config(state=tk.NORMAL)
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.status_text.config(state=tk.DISABLED)


def main(args=None):
    rclpy.init(args=args)
    node = RobotGuiNode()

    # Запуск ROS2 спінінга у фоновому потоці
    ros_thread = threading.Thread(target=rclpy.spin, args=(node,), daemon=True)
    ros_thread.start()

    # Запуск графічного інтерфейсу
    root = tk.Tk()
    app = GuiApp(root, node)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()