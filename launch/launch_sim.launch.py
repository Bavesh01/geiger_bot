import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare
from launch_ros.actions import Node



def generate_launch_description():


    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name='geiger_bot' #<--- CHANGE ME

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # default_world = os.path.join(
    # get_package_share_directory(package_name),
    # 'worlds',
    # 'empty.world'
    # )    

    # default_world = '/home/bavesh/geigerbot_project/dev_ws/src/geiger_bot/worlds/empty.world'
    
    default_world = os.path.join(
        FindPackageShare(package_name).find(package_name),
        'worlds',
        'empty.world'
    )

    # default_world = '/home/bavesh/geigerbot_project/dev_ws/src/geiger_bot/worlds/empty.world'

    print(f"Testing world file path: {default_world}")  # Debugging output

    world = LaunchConfiguration('world')

    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='World to load'
        )
    

    print(f"Resolved default world: {default_world}")
    print(world_arg)

    # Include the Gazebo launch file, provided by the ros_gz_sim package
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(
                FindPackageShare('ros_gz_sim').find('ros_gz_sim'), 'launch', 'gz_sim.launch.py')]
        ),
        launch_arguments={
            'gz_args': ['-r -v4 ', world],
            'on_exit_shutdown': 'true'
        }.items()
    )


    print(f"FindPackageShare resolved path: {FindPackageShare(package_name).find(package_name)}")
    print(f"Default world path: {default_world}")
    
    # Run the spawner node from the ros_gz_sim package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='ros_gz_sim', executable='create',
                        arguments=['-topic', 'robot_description',
                                   '-name', 'my_bot',
                                   '-z', '0.1'],
                        output='screen')


    print(f"Resolved world file: {world.describe()}")


    # Launch them all!
    return LaunchDescription([
        rsp,
        world_arg,
        gazebo,
        spawn_entity,
    ])