import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MotionControlNode(Node):
    def __init__(self):
        super().__init__('motion_control_node')
        
        #Підписка на топік /cmd_vel з типом geometry_msgs/msg/Twist
        self.subscription = self.create_subscription(
            Twist,
            '/cmd_vel',
            self.cmd_vel_callback,
            10
        )
        
        #Встановлення граничних значень швидкості
        self.max_linear_x = 0.5   # Максимальна лінійна швидкість (м/с)
        self.max_angular_z = 1.0  # Максимальна кутова швидкість (рад/с)
        
        self.get_logger().info('Motion Control Node успішно запущено та підписано на /cmd_vel')

    def cmd_vel_callback(self, msg: Twist):
        #Зберігаємо початкові значення
        linear_x = msg.linear.x
        angular_z = msg.angular.z

        #Перевірка та обмеження linear.x з WARN-повідомленням
        if abs(linear_x) > self.max_linear_x:
            self.get_logger().warning(
                f'Лінійна швидкість перевищує ліміт! Отримано: {linear_x:.2f}, обмежено до: {self.max_linear_x:.2f}'
            )
            linear_x = max(-self.max_linear_x, min(self.max_linear_x, linear_x))

        # Перевірка та обмеження angular.z з WARN-повідомленням
        if abs(angular_z) > self.max_angular_z:
            self.get_logger().warning(
                f'Кутова швидкість перевищує ліміт! Отримано: {angular_z:.2f}, обмежено до: {self.max_angular_z:.2f}'
            )
            angular_z = max(-self.max_angular_z, min(self.max_angular_z, angular_z))

        #Виведення прийнятих (та обмежених) значень через INFO-лог
        self.get_logger().info(f'Отримано команди -> linear.x: {linear_x:.2f}, angular.z: {angular_z:.2f}')

def main(args=None):
    rclpy.init(args=args)
    node = MotionControlNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()