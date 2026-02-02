ARG ROS_DISTRO=humble
FROM ros:${ROS_DISTRO}-ros-base AS base

ARG ROS_DISTRO

ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive
ENV TERM=xterm-256color

RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    terminator \
    iputils-ping \
    openssh-server \
    iproute2 \
    python3-pip \
    nano \
    build-essential \
    cmake \
    git \
    python3-colcon-common-extensions \
    python3-colcon-mixin \
    python3-flake8 \
    python3-setuptools \
    python3-vcstool \
    freeglut3-dev \
    lsb-release \
    gnupg \
    libglew-dev \
    libqt5opengl5-dev \
    python3-rosdep \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir --upgrade pip \
    argcomplete \
    flake8-blind-except \
    flake8-builtins \
    flake8-comprehensions \
    flake8-deprecated \
    flake8-return \
    flake8-length \
    flake8-todo \
    flake8-quotes \
    black \
    mypy \
    prospector \
    pylint \
    numpy \
    opencv-python \
    panda \
    matplotlib \
    rosbags

RUN sh -c 'echo "deb http://packages.osrfoundation.org/gazebo/ubuntu-stable `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list' \
    && wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add - \
    && apt-get update && apt-get install -y ignition-fortress \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Pin ros2_control stack packages so they don't drift across layers / rebuilds
RUN mkdir -p /etc/apt/preferences.d && \
    printf "Package: ros-%s-ros2-control\nPin: release *\nPin-Priority: 1001\n\nPackage: ros-%s-ros2-controllers\nPin: release *\nPin-Priority: 1001\n\nPackage: ros-%s-realtime-tools\nPin: release *\nPin-Priority: 1001\n" \
      "${ROS_DISTRO}" "${ROS_DISTRO}" "${ROS_DISTRO}" \
      > /etc/apt/preferences.d/pin-ros2-control

RUN apt-get update && apt-get install -y --no-install-recommends \
    ros-$ROS_DISTRO-rqt \
    ros-$ROS_DISTRO-rqt-common-plugins \
    ros-$ROS_DISTRO-rqt-robot-dashboard \
    ros-$ROS_DISTRO-rqt-robot-steering \
    ros-$ROS_DISTRO-rqt-tf-tree \
    ros-$ROS_DISTRO-image-transport-plugins \
    ros-$ROS_DISTRO-compressed-image-transport \
    ros-$ROS_DISTRO-clearpath-desktop \
    ros-$ROS_DISTRO-cv-bridge \
    ros-$ROS_DISTRO-ros2-control \
    ros-$ROS_DISTRO-ros2-controllers \
    ros-$ROS_DISTRO-kinematics-interface \
    ros-$ROS_DISTRO-control-msgs \
    ros-$ROS_DISTRO-realtime-tools \
    ros-$ROS_DISTRO-rosbag2-py \
    ros-$ROS_DISTRO-usb-cam \
    ros-$ROS_DISTRO-rviz2 \
    ros-$ROS_DISTRO-rmw-cyclonedds-cpp \
    ros-$ROS_DISTRO-ros-testing \
    ros-$ROS_DISTRO-ros2bag \
    ros-$ROS_DISTRO-ign-ros2-control \
    ros-$ROS_DISTRO-moveit \
    ros-$ROS_DISTRO-moveit-servo \
    ros-$ROS_DISTRO-moveit-visual-tools \
    ros-$ROS_DISTRO-pilz-industrial-motion-planner \
    ros-$ROS_DISTRO-ros-ign-bridge \
    ros-$ROS_DISTRO-ros-ign-gazebo \
    ros-$ROS_DISTRO-ament-clang-format \
    ros-$ROS_DISTRO-clearpath-simulator \
    ros-$ROS_DISTRO-clearpath-nav2-demos \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /dev_ws/src
WORKDIR /dev_ws/src

RUN wget https://packages.clearpathrobotics.com/public.key -O - | apt-key add - \
    && sh -c 'echo "deb https://packages.clearpathrobotics.com/stable/ubuntu $(lsb_release -cs) main" > /etc/apt/sources.list.d/clearpath-latest.list' \
    && apt-get update && apt-get install -y ros-$ROS_DISTRO-clearpath-sensors \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /dev_ws
COPY . /dev_ws/src

# Re-enable rosdep install for workspace dependencies
RUN apt-get update && rosdep update && \
    rosdep install --ignore-src --from-paths src -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Patch UR driver in this repo to compile with Humble's current deps:
# std::atomic<bool> doesn't have readFromRT()/writeFromNonRT()
RUN set -eux; \
    F=/dev_ws/src/Universal_Robots_ROS2_Driver/ur_controllers/src/scaled_joint_trajectory_controller.cpp; \
    test -f "$F"; \
    sed -i \
      -e 's/rt_has_pending_goal_\.readFromRT()/rt_has_pending_goal_\.load()/g' \
      -e 's/rt_is_holding_\.readFromRT()/rt_is_holding_\.load()/g' \
      -e 's/rt_has_pending_goal_\.writeFromNonRT(/rt_has_pending_goal_\.store(/g' \
      "$F"; \
    # Fix leftover pointer-dereference patterns like *(rt_is_holding_.load())
    sed -i \
      -e 's/\*\s*(\s*rt_is_holding_\.load()\s*)/rt_is_holding_.load()/g' \
      -e 's/\*\s*(\s*rt_has_pending_goal_\.load()\s*)/rt_has_pending_goal_.load()/g' \
      "$F"

RUN ["/bin/bash", "-c", "source /opt/ros/$ROS_DISTRO/setup.bash && \
     colcon build --merge-install --symlink-install --cmake-args '-DCMAKE_BUILD_TYPE=Release'"]

RUN ["/bin/bash", "-c", "cp /dev_ws/src/.docker/setup.bash /dev_ws/setup.bash && chmod 777 /dev_ws/setup.bash"]
RUN ["/bin/bash", "-c", "cp /dev_ws/src/.docker/entrypoint.bash / && chmod 777 /entrypoint.bash"]

ENTRYPOINT ["bash", "/entrypoint.bash"]
CMD ["bash"]