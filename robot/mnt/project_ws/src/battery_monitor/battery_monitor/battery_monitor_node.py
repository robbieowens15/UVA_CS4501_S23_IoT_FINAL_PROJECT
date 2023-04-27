import rclpy
import rclpy.node

class MinimalParam(rclpy.node.Node):
    battery_percentage = 100.0
    battery_tick_rate = 1.0

    def __init__(self):
        super().__init__('battery_monitor_node')

        from rcl_interfaces.msg import ParameterDescriptor
        battery_time_descriptor = ParameterDescriptor(description='Number of seconds for battery to deplete')

        self.declare_parameter('battery_time', '100', battery_time_descriptor)

        battery_time_input = None
        try:
            battery_time_input = int(self.get_parameter('battery_time').get_parameter_value().string_value)
            self.get_logger().info(f'input: {battery_time_input}')
        except ValueError:
            self.get_logger().error('The parameter value for battery_time: "%s" is not an integer.' % self.get_parameter('battery_time').get_parameter_value().string_value)

        if battery_time_input is None: 
            #use default settings 
            self.battery_percentage = 100.0
            self.battery_tick_rate = 1.0
        else:
            self.battery_percentage = 100.0
            self.battery_tick_rate = 100.0 / battery_time_input

        self.get_logger().info(f'tick rate: {self.battery_tick_rate}')

        self.get_logger().info(f'Battery Level: { str(self.battery_percentage)}%')
        self.timer = self.create_timer(1, self.timer_callback) #timer callback executes every second

    def timer_callback(self):
        self.battery_percentage = self.battery_percentage - self.battery_tick_rate
        if self.battery_percentage <= 0.01:
            self.battery_percentage = 0.0

        self.get_logger().info(f'Battery Level: { str(self.battery_percentage)}%')

def main():
    rclpy.init()
    node = MinimalParam()
    rclpy.spin(node)

if __name__ == '__main__':
    main()