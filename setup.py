from setuptools import find_packages, setup

package_name = 'pygame_mechanism_ros2_practice'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='matthew',
    maintainer_email='matt.robinson10.28.98@gmail.com',
    description='Render planar mechanisms of ROS2 nodes using pygame library',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'test1 = pygame_mechanism_ros2_practice.main_test:main'
        ],
    },
)
