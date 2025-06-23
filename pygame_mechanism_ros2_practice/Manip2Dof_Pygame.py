from threading import Thread
import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Pose2D

from manip2dof_interfaces.msg import Manip2DofSolution
from manip2dof_interfaces.srv import Manip2DofProperties

import pygame_ros2_tools.Variables as v
from pygame_ros2_tools.Linkage import Linkage
from pygame_ros2_tools.Point import Point
from pygame_ros2_tools.Screen import Screen

SCREEN_PIXEL_SIZE = 800
SCREEN_INCH_SIZE = 16

class Manip2Dof_SolutionSub(Node):

    def __init__(self, screen):
        super().__init__('Manip2Dof_SolutionSub')
        self.solution_sub = self.create_subscription(
            Manip2DofSolution,
            'Manip2Dof_SolutionTopic',
            self.solutionsub_callback,
            10)
        self.goal_sub = self.create_subscription(
            Pose2D,
            'Manip2Dof_SetGoalTraceCircle_PoseTopic',
            self.goalsub_callback,
            10)
        self.properties_client = self.create_client(Manip2DofProperties, 'request_manip_info')

        while not self.properties_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')


        self.req = Manip2DofProperties.Request()
        self.screen = screen

        future = self.request_manip_properties()
        rclpy.spin_until_future_complete(self, future)

        self.link_lengths = [future.result().l1, future.result().l2]
        self.joint_config = [0, 0]

        # To avoid unused var warnings
        self.solution_sub
        self.goal_sub

    def solutionsub_callback(self, msg):
        self.get_logger().info('I heard a new solution: "%f", "%f"' % (msg.j1, msg.j2))
        self.joint_config = msg.j1, msg.j2

    def goalsub_callback(self, msg):
        self.get_logger().info('I heard a new goal: "%f", "%f"' % (msg.x, msg.y))

        # Create point and add it to the screen
        Point(self.screen, self.screen.inches_to_pixels(msg.x + (SCREEN_INCH_SIZE/2)), 
              self.screen.inches_to_pixels(msg.y + (SCREEN_INCH_SIZE/2)), 0, self.screen.points)

        if len(self.screen.points) > 25:
            self.screen.delete_point()

    def request_manip_properties(self):
        return self.properties_client.call_async(self.req)


def main(args=None):
    rclpy.init(args=args)

    screen = Screen(SCREEN_PIXEL_SIZE, SCREEN_INCH_SIZE)

    solution_sub = Manip2Dof_SolutionSub(screen)

    ros_thread = Thread(target=rclpy.spin, args=(solution_sub,))
    ros_thread.start()

    run = True
    while run:
        screen.initialize()

        link1 = Linkage(solution_sub.screen, solution_sub.link_lengths[0], 
                        SCREEN_INCH_SIZE/2, 
                        SCREEN_INCH_SIZE/2, 
                        solution_sub.joint_config[0], 
                        v.blue)
        
        link2 = Linkage(solution_sub.screen, solution_sub.link_lengths[1], 
                        SCREEN_INCH_SIZE/2 + solution_sub.link_lengths[0] * math.cos(solution_sub.joint_config[0]), 
                        SCREEN_INCH_SIZE/2 + solution_sub.link_lengths[0] * math.sin(solution_sub.joint_config[0]), 
                        solution_sub.joint_config[1], 
                        v.blue)
        screen.linkages = [link1, link2]
        screen.draw()

    solution_sub.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
    py.quit()