# Carla Cyber Bridge

For Carla Simulator (0.9.11) and Apollo-5.0.0.

The "Carla Cyber Bridge" is a mimic of ["Carla ROS Bridge"](https://github.com/carla-simulator/ros-bridge.git). Carla ROS Bridge enables two-way communication between Carla Simulator and ROS. In a mimic way, the current package is to build communication between Carla Simulator and CyberRT which is used in Baidu Apollo stack.

CyberRT is a real-time middle-ware which is different from ROS. But other than that, the commonly used message exchanging mechanism is quite similar to that in ROS. For example, the "writer and reader" mechanism in CyberRTmechanism is a counterpart to the "publisher and subscriber" mechanism in ROS. In CyberRT, it also has its version "service and client". Based on those facts, we can mimic the ros bridge.  

## Getting started

### Build docker image / run container for Carla Cyber Bridge

This container will run the bridge and sim clients.

```
# run on local machine, starting from the root of this repo:

cd docker
./build_docker.sh
./run_docker.sh
```

### Run Carla client and bridge

#### Enter carla-cyber docker container

```
# run on local machine:

docker exec -ti carla-cyber bash
```

#### Update /apollo/cyber/setup.bash

Change CYBER_IP in /apollo/cyber/setup.bash to the carla-cyber container IP address

To find out the ip address to use, run this command outside of the container:

```
# run on local machine:

docker inspect carla-cyber | grep IPAddress
```

Then update the file in your preferred editor

```
# run in carla-cyber container:

vim /apollo/cyber/setup.bash
# and so on to edit the text file

# then source your ~/.bashrc file to apply the changes:
source ~/.bashrc
```

#### Run Carla-Cyber-Bridge with an ego vehicle

In Terminal 1:

```
# run in carla-cyber container:
cd /apollo/carla_bridge
python carla_cyber_bridge/bridge.py
```

In Terminal 2:

```
# run in carla-cyber container
cd /apollo/carla_bridge
python carla_spawn_object/carla_spawn_object.py
```

### Run Apollo Dreamview & modules

Now, in the apollo container, run dreamview:

```
# run in apollo_dev_user container:

. /apollo/scripts/dreamview.sh start_fe
```

Then, in a web browser, go to: `localhost:8888`
