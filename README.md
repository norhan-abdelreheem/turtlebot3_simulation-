 # TurtleBot3 Gazebo Simulation: SLAM & Autonomous Navigation

[![ROS](https://img.shields.io/badge/ROS-jazzy-blue.svg)](http://wiki.ros.org/)
[![Gazebo](https://img.shields.io/badge/Simulator-Gazebo-orange.svg)](http://gazebosim.org/)
[![Robot](https://img.shields.io/badge/Robot-TurtleBot3-green.svg)](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)

##  Project Overview
This repository contains a robotics simulation project demonstrating **Simultaneous Localization and Mapping (SLAM)** and **Autonomous Navigation** using a **TurtleBot3** robot inside a **Gazebo** environment. 

The project is divided into two main phases:
1. **Mapping (SLAM):** Spawning the TurtleBot3 in a custom/standard Gazebo world, teleoperating it around the environment, and generating an occupancy grid map using SLAM (e.g., Gmapping / Cartographer).
2. **Autonomous Navigation:** Loading the saved map into the ROS Navigation Stack (`move_base` / `Nav2`), localizing the robot using Adaptive Monte Carlo Localization (AMCL), and commanding the robot to autonomously navigate to a target goal pose while avoiding obstacles.

---

##  Prerequisites & Dependencies
Before running this project, ensure you have the following installed on your system (Ubuntu 20.04 with ROS Noetic or Ubuntu 22.04 with ROS 2 Humble):

* **ROS** (Noetic / Humble)
* **Gazebo Simulator**
* **RViz**
* **TurtleBot3 Packages:**
  * `turtlebot3`
  * `turtlebot3_msgs`
  * `turtlebot3_simulations`
* **SLAM & Navigation Packages:**
  * `gmapping` / `slam_gmapping` (or `slam_toolbox` for ROS 2)
  * `navigation` (`move_base`, `amcl`, `map_server`) or `navigation2`

### Quick Dependency Installation (ROS Noetic Example)
```bash
sudo apt update
sudo apt install ros-noetic-turtlebot3 ros-noetic-turtlebot3-msgs ros-noetic-turtlebot3-simulations
sudo apt install ros-noetic-gmapping ros-noetic-navigation ros-noetic-map-server
```

---

##  Installation & Setup

1. **Create and initialize a catkin workspace** (skip if you already have one):
   ```bash
   mkdir -p ~/catkin_ws/src
   cd ~/catkin_ws/src
   ```

2. **Clone this repository:**
   ```bash
   git clone https://github.com/norhan-abdelreheem/turtlebot3_simulation-.git
   ```

3. **Build the workspace:**
   ```bash
   cd ~/catkin_ws
   catkin_make
   source devel/setup.bash
   ```

4. **Set the TurtleBot3 model environment variable** (`burger`, `waffle`, or `waffle_pi`):
   ```bash
   echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc
   source ~/.bashrc
   ```

---

##  Usage Instructions

### Phase 1: Environment Mapping (SLAM)

1. **Launch the Gazebo Simulation Environment:**
   ```bash
   roslaunch turtlebot3_gazebo turtlebot3_world.launch
   ```
   *(Note: Replace `turtlebot3_world.launch` with your custom launch file name if you used a custom world in this repository).*

2. **Start the SLAM Node & RViz:**
   Open a new terminal and run:
   ```bash
   roslaunch turtlebot3_slam turtlebot3_slam.launch slam_methods:=gmapping
   ```

3. **Teleoperate the Robot to Explore the Map:**
   Open another terminal and use the keyboard to drive the robot around all corners of the environment until the map is fully built in RViz:
   ```bash
   roslaunch turtlebot3_teleop turtlebot3_teleop_key.launch
   ```
   *Controls: `W` (Forward), `X` (Backward), `A` (Turn Left), `D` (Turn Right), `S` (Stop).*

4. **Save the Generated Map:**
   Once the map is complete, save it to your `maps` directory:
   ```bash
   rosrun map_server map_saver -f ~/map
   ```
   This generates two files: `map.pgm` (the occupancy grid image) and `map.yaml` (the map metadata).

5. **Close all running nodes** (`Ctrl + C` in all terminals) before proceeding to Phase 2.

---

### Phase 2: Autonomous Navigation

1. **Launch the Gazebo Environment:**
   ```bash
   roslaunch turtlebot3_gazebo turtlebot3_world.launch
   ```

2. **Launch the Navigation Stack with Your Saved Map:**
   Open a new terminal and load the map into `move_base` and `AMCL`:
   ```bash
   roslaunch turtlebot3_navigation turtlebot3_navigation.launch map_file:=$HOME/map.yaml
   ```

3. **Set Initial Pose (Localization):**
   * In **RViz**, click the **`2D Pose Estimate`** button on the top toolbar.
   * Click on the map where the robot is currently located in Gazebo and drag the arrow in the direction the robot is facing.

4. **Send an Autonomous Navigation Goal:**
   * In **RViz**, click the **`2D Nav Goal`** button on the top toolbar.
   * Click on your desired target destination on the map and drag to specify the final orientation.
   * The global planner will compute a path, and the local planner will drive the TurtleBot3 autonomously to the goal while avoiding obstacles!

---

##  Repository Structure
```text
turtlebot3_simulation-/
├── launch/          # Custom Gazebo, SLAM, and Navigation launch files
├── maps/            # Saved occupancy grid maps (.pgm and .yaml)
├── worlds/          # Custom Gazebo environment world files (.world)
├── rviz/            # RViz configuration files
├── CMakeLists.txt   # Build configuration
├── package.xml      # Package dependencies and metadata
└── README.md        # Project documentation
```

---

##  Demo & Results


* **Gazebo Environment:** Shows the robot spawned in the simulated world.
* **SLAM Mapping:** Real-time occupancy grid generation using LiDAR scan data (`/scan`).
* **Navigation Stack:** Costmaps (global & local), AMCL particle cloud convergence, and dynamic obstacle avoidance.

---
