from threading import Thread

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose2D
from geometry_msgs.msg import Vector3

from pygame_ros2_tools.Point import Point
from pygame_ros2_tools.Screen import Screen

def run_pygame(screen):
    run = True

    while run:
        screen.initialize()
        screen.draw()

class Manip2Dof_SolutionSub(Node):

    def __init__(self, screen):
        super().__init__('Manip2Dof_SolutionSub')
        self.solution_sub = self.create_subscription(
            Vector3,
            'Manip2Dof_SolutionTopic',
            self.solutionsub_callback,
            10)
        self.goal_sub = self.create_subscription(
            Pose2D,
            'Manip2Dof_SetGoalTraceCircle_PoseTopic',
            self.goalsub_callback,
            10)
        self.solution_sub
        self.goal_sub
        self.screen = screen

    def solutionsub_callback(self, msg):
        self.get_logger().info('I heard a new solution: "%f", "%f"' % (msg.x, msg.y))

    def goalsub_callback(self, msg):
        self.get_logger().info('I heard a new goal: "%f", "%f"' % (msg.x, msg.y))

        # Create point and add it to the screen
        Point(self.screen, self.screen.inches_to_pixels(msg.x), self.screen.inches_to_pixels(msg.y), 0, self.screen.points)



def main(args=None):
    rclpy.init(args=args)

    screen = Screen(800, 8)

    solution_sub = Manip2Dof_SolutionSub(screen)

    ros_thread = Thread(target=rclpy.spin, args=(solution_sub,))
    ros_thread.start()
    # ros_thread.join()

    run_pygame(screen)

    # rclpy.spin(solution_sub)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    solution_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    py.quit()