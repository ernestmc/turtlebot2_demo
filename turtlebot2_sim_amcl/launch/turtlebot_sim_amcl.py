# Copyright 2017 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import sys

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescriptor
from launch.exit_handler import restart_exit_handler
from launch.launcher import DefaultLauncher
from launch.output_handler import ConsoleOutput
from ros2run.api import get_executable_path


def launch(launch_descriptor, argv):
    parser = argparse.ArgumentParser(description='launch amcl turtlebot sim demo')
    parser.add_argument(
        '--map',
        help='path to map (will be passed to map_server)')
    args = parser.parse_args(argv)

    ld = launch_descriptor

    package = 'ros1_bridge'
    ld.add_process(
        cmd=[get_executable_path(package_name=package, executable_name='dynamic_bridge')],
        name='dynamic_bridge',
        exit_handler=restart_exit_handler,
        output_handlers=[ConsoleOutput()],
    )
    
    package = 'depthimage_to_laserscan'
    ld.add_process(
        cmd=[
            get_executable_path(
                package_name=package, executable_name='depthimage_to_laserscan_node'),
                '/depth:=/camera/depth/image_raw',
                '/depth_camera_info:=/camera/depth/camera_info'
                ],
        name='depthimage_to_laserscan_node',
        exit_handler=restart_exit_handler,
    )
    
    package = 'joy'
    ld.add_process(
        cmd=[get_executable_path(package_name=package, executable_name='joy_node')],
        name='joy_node',
        exit_handler=restart_exit_handler,
    )
    
    package = 'teleop_twist_joy'
    ld.add_process(
        cmd=[get_executable_path(package_name=package, executable_name='teleop_node'),
        '/cmd_vel:=/cmd_vel_mux/input/teleop'],
        name='teleop_node',
        exit_handler=restart_exit_handler,
    )
    
    turtlebot2_sim_amcl_share = get_package_share_directory('turtlebot2_sim_amcl')
    map_path = os.path.join(turtlebot2_sim_amcl_share, 'examples', 'playground.yaml')
    if args.map:
        map_path = args.map
    package = 'map_server'
    ld.add_process(
        cmd=[get_executable_path(package_name=package, executable_name='map_server'), map_path],
        name='map_server',
    )
    
    package = 'amcl'
    ld.add_process(
        cmd=[get_executable_path(package_name=package, executable_name='amcl')],
        name='amcl',
        exit_handler=restart_exit_handler,
        output_handlers=[ConsoleOutput()],
    )

    return ld


def main(argv=sys.argv[1:]):
    launcher = DefaultLauncher()
    launch_descriptor = launch(LaunchDescriptor(), argv)
    launcher.add_launch_descriptor(launch_descriptor)
    rc = launcher.launch()
    return rc


if __name__ == '__main__':
    sys.exit(main())
