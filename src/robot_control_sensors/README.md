# Robot Control and Sensors

## Project Overview

This ROS 2 package implements the Robot Control and Sensors module for the TurtleBot3 autonomous navigation project.

- Team Role: Member 2 – Robot Control and Sensors
- Robot: TurtleBot3 Burger
- Operating System: Ubuntu 24.04 (WSL2)
- ROS Distribution: ROS 2 Jazzy
- Simulator: Gazebo Harmonic
- Programming Language: Python

## Package Features

- Manual robot control using keyboard teleoperation.
- LiDAR, Odometry, and IMU data monitoring.
- Obstacle detection in four directions.
- Automatic forward movement.
- Automatic stopping when a front obstacle is detected.
- Fail-safe behavior when LiDAR data is missing or invalid.
- Obstacle stop latching to prevent repeated movement near obstacles.

## Package Structure

```text
robot_control_sensors/
├── robot_control_sensors/
│   ├── __init__.py
│   ├── sensor_monitor.py
│   ├── obstacle_detector.py
│   └── auto_controller.py
├── resource/
├── test/
├── package.xml
├── setup.py
├── setup.cfg
└── README.md
```

## ROS 2 Topics

| Topic | Message Type | Purpose |
|---|---|---|
| /scan | LaserScan | LiDAR measurements |
| /odom | Odometry | Robot position and velocity |
| /imu | Imu | Inertial measurements |
| /cmd_vel | TwistStamped | Robot movement commands |
| /tf | TFMessage | Dynamic transformations |
| /tf_static | TFMessage | Static transformations |

## Build Instructions

From the project workspace:

```bash
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select robot_control_sensors
source install/setup.bash
export TURTLEBOT3_MODEL=burger
```

## Launch Simulation

```bash
ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py
```

Run the following nodes in separate terminals after sourcing the workspace.

## 1. Sensor Monitor

```bash
ros2 run robot_control_sensors sensor_monitor
```

Displays:

- Nearest valid LiDAR obstacle distance.
- Robot X and Y coordinates.
- Linear and angular velocities.
- IMU acceleration values.

## 2. Obstacle Detector

```bash
ros2 run robot_control_sensors obstacle_detector
```

Monitors four directions:

- Front
- Left
- Right
- Rear

An obstacle warning is generated when a valid measured distance is below 0.30 meters.

## 3. Manual Control

```bash
ros2 run turtlebot3_teleop teleop_keyboard
```

Use the keyboard to control robot movement.

## 4. Automatic Controller

Stop manual teleoperation and other velocity publishers before running this node.

```bash
ros2 run robot_control_sensors auto_controller
```

Automatic movement is disabled by default.

Enable movement:

```bash
ros2 param set /auto_controller enable_motion true
```

Disable movement:

```bash
ros2 param set /auto_controller enable_motion false
```

### Controller Configuration

| Parameter | Value |
|---|---|
| Forward speed | 0.05 m/s |
| Front stopping threshold | 0.30 m |
| Front detection angle | -30 to +30 degrees |
| LiDAR timeout | 2 seconds |
| Control timer period | 0.1 seconds |
| Default movement state | Disabled |

Once a front obstacle reaches the stopping threshold, the controller latches the stop state. Movement must be disabled and enabled again to reset the latch.

## Testing Results

| Test | Result |
|---|---|
| Package compilation | Passed |
| Manual robot movement | Passed |
| LiDAR data reception | Passed |
| Odometry data reception | Passed |
| IMU data reception | Passed |
| Odometry to LiDAR TF | Passed |
| Sensor monitoring | Passed |
| Directional obstacle detection | Passed |
| Automatic forward movement | Passed |
| Automatic front obstacle stopping | Passed |
| Obstacle stop latching | Passed |
| Zero velocity after disabling movement | Passed |
| Missing LiDAR data at startup | Passed |

### Experimental Observations

- Automatic forward displacement: approximately 0.473 meters.
- Front obstacle distance before the stopping test: approximately 0.41 meters.
- Automatic stop was reported after approximately 7.1 seconds of wall-clock time.
- No movement resumption was reported during the following 10.9 seconds before disabling movement.
- All measured linear and angular velocities were zero after disabling movement.

## Fail-Safe Test

With other velocity publishers stopped:

```bash
ros2 run robot_control_sensors auto_controller --ros-args -r /scan:=/missing_scan -p enable_motion:=true
```

Expected status:

```text
STOP: LiDAR data missing
```

Verify the velocity command in another terminal:

```bash
ros2 topic echo /cmd_vel --once
```

The observed velocity command contained zero linear and angular velocities.

## Integration with SLAM and Nav2

The sensor monitor and obstacle detector are monitoring nodes and do not publish movement commands.

The automatic controller publishes directly to /cmd_vel. It must be stopped before using Nav2 or manual teleoperation to prevent conflicting velocity commands.

SLAM and Nav2 integration testing is outside the scope of this package's completed tests.

## Known Issues and Limitations

- The IMU message frame ID differs from the available IMU TF frame.
- Gazebo simulation performance may be reduced under WSL2.
- Some environment textures may be missing.
- The automatic controller checks front obstacles only and does not guarantee collision avoidance in every direction.
- Positive infinite LiDAR readings are treated as clear up to the sensor's maximum range.
- The sensor monitor displays the latest received data without a freshness check.
- Missing LiDAR data at startup was tested. Sensor interruption during active movement has not been experimentally verified.
- Automated lint and copyright tests have not yet been verified.
- The automatic controller is intended for simulation testing, not safety-critical physical robot operation.

## Development Branch

```text
member2-control-sensors
```

This package was developed separately without modifying the original simulation source files.

## References

- ROS 2 Jazzy: https://docs.ros.org/en/jazzy/
- TurtleBot3 Documentation: https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/
- Gazebo Harmonic: https://gazebosim.org/docs/harmonic/
- Navigation2: https://docs.nav2.org/
