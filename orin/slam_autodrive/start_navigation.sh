#!/bin/bash

# ROS 환경 설정
source /opt/ros/noetic/setup.bash  # ROS 버전에 맞춰 경로를 변경해주세요.
source ~/catkin_ws/devel/setup.bash  # catkin workspace 경로를 정확히 설정하세요.

# 프로세스 ID를 저장할 배열
declare -a pids

# ROS core 실행
echo "Starting ROS core..."
roscore &
pids+=($!)
sleep 5  # roscore가 완전히 실행될 시간을 기다립니다.

# TF2 Web Republisher 실행
echo "Starting TF2 Web Republisher..."
rosrun tf2_web_republisher tf2_web_republisher &
pids+=($!)
sleep 2

# ROSBridge WebSocket 서버 실행
echo "Starting ROSBridge WebSocket server..."
roslaunch rosbridge_server rosbridge_websocket.launch &
pids+=($!)
sleep 2

# Apache 서버 실행
echo "Starting Apache server..."
/usr/bin/expect <<EOF
set timeout 5
spawn sudo service apache2 start
expect "password for *:"
send "1\r"
epxect eof
EOF

sudo service apache2 start

# Python 스크립트 (uart.py) 실행
echo "Starting uart.py script..."
python3 /home/c102/test/uart.py &
pids+=($!)

# imu_ros.py 파일 실행
echo "Starting imu_ros.py script..."
python3 /home/c102/catkin_ws/src/my_robot_navigation/src/imu_ros.py &
pids+=($!)

# RPLIDAR와 함께 Navigation 실행
echo "Starting Navigation..."
roslaunch my_robot_navigation my_navigation.launch &
pids+=($!)

# Python 스크립트 (motor_controller.py) 실행
echo "Starting motor controller..."
rosrun my_robot_controller motor_controller.py &
pids+=($!)

echo "All systems are up and running!"

# 스크립트 종료 시 모든 프로세스 종료
trap "echo 'Stopping all processes...'; kill ${pids[@]}" EXIT

# 스크립트가 종료될 때까지 대기
wait

