set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

sudo apt update && sudo apt install -y git python3-colcon-common-extensions ros-jazzy-navigation2 ros-jazzy-nav2-bringup ros-jazzy-ros-gz ros-jazzy-slam-toolbox ros-jazzy-teleop-twist-keyboard ros-jazzy-dynamixel-sdk

cd "$SCRIPT_DIR"
colcon build --symlink-install

grep -qxF 'source /opt/ros/jazzy/setup.bash' ~/.bashrc || echo 'source /opt/ros/jazzy/setup.bash' >> ~/.bashrc
grep -qxF "source $SCRIPT_DIR/install/setup.bash" ~/.bashrc || echo "source $SCRIPT_DIR/install/setup.bash" >> ~/.bashrc
grep -qxF 'export TURTLEBOT3_MODEL=burger' ~/.bashrc || echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc

echo "Setup complete! Open a new terminal and run: ros2 launch turtlebot3_gazebo turtlebot3_house.launch.py"
