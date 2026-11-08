from setuptools import find_packages, setup

package_name = 'motion_recorder'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={'': ['py.typed']},
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='alexmazila',
    maintainer_email='alexpavluk10@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'recorder_node = motion_recorder.recorder_node:main',
        'player_node = motion_recorder.player_node:main',
        'gui_node = motion_recorder.gui_node:main',
        'motion_node = motion_recorder.motion_node:main',
    ],
    },
)
