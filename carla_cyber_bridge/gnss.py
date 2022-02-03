#!/usr/bin/env python

#
# Copyright (c) 2018-2019 Intel Corporation
#
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.
#
"""
Classes to handle Carla gnsss
"""

import carla_common.transforms as trans

from carla_cyber_bridge.sensor import Sensor

from modules.drivers.gnss.proto.gnss_best_pose_pb2 import GnssBestPose
from modules.drivers.gnss.proto.gnss_status_pb2 import GnssStatus
from modules.drivers.gnss.proto.heading_pb2 import Heading
from modules.localization.proto.gps_pb2 import Gps


class Gnss(Sensor):

    """
    Actor implementation details for gnss sensor
    """

    def __init__(self, uid, name, parent, relative_spawn_pose, node, carla_actor, synchronous_mode):
        """
        Constructor

        :param uid: unique identifier for this object
        :type uid: int
        :param name: name identiying this object
        :type name: string
        :param parent: the parent of this
        :type parent: carla_cyber_bridge.Parent
        :param relative_spawn_pose: the relative spawn pose of this
        :type relative_spawn_pose: geometry_msgs.Pose
        :param node: node-handle
        :type node: CompatibleNode
        :param carla_actor: carla actor object
        :type carla_actor: carla.Actor
        :param synchronous_mode: use in synchronous mode?
        :type synchronous_mode: bool
        """
        super(Gnss, self).__init__(uid=uid,
                                   name=name,
                                   parent=parent,
                                   relative_spawn_pose=relative_spawn_pose,
                                   node=node,
                                   carla_actor=carla_actor,
                                   synchronous_mode=synchronous_mode)

        self.gnss_navsatfix_writer = node.new_writer(self.get_topic_prefix() + "/best_pose",
                                           GnssBestPose,
                                           qos_depth=10)
        self.gnss_odometry_writer = node.new_writer(self.get_topic_prefix() + "/odometry",
                                           Gps,
                                           qos_depth=10)
        self.gnss_heading_writer = node.new_writer(self.get_topic_prefix() + "/heading",
                                           Heading,
                                           qos_depth=10)
        self.gnss_status_writer = node.new_writer(self.get_topic_prefix() + "/gnss_status",
                                           GnssStatus,
                                           qos_depth=10)
        self.listen()

    def destroy(self):
        super(Gnss, self).destroy()
        self.node.destroy_writer(self.gnss_status_writer)
        self.node.destroy_writer(self.gnss_odometry_writer)

    def get_topic_prefix(self):
        """
        get the topic name of the current entity.

        :return: the final topic name of this object
        :rtype: string
        """
        return "/apollo/sensor/" + self.name

    def sensor_data_updated(self, carla_gnss_measurement):
        """
        Function to transform a received gnss event into a ROS NavSatFix message

        :param carla_gnss_measurement: carla gnss measurement object
        :type carla_gnss_measurement: carla.GnssMeasurement
        """
        gnss_navsatfix_msg = GnssBestPose()
        gnss_navsatfix_msg.header.CopyFrom(self.get_msg_header(timestamp=carla_gnss_measurement.timestamp))
        gnss_navsatfix_msg.latitude = carla_gnss_measurement.latitude
        gnss_navsatfix_msg.longitude = carla_gnss_measurement.longitude
        gnss_navsatfix_msg.height_msl = carla_gnss_measurement.altitude
        self.gnss_navsatfix_writer.write(gnss_navsatfix_msg)

        gnss_odometry_msg = Gps()
        gnss_odometry_msg.header.CopyFrom(self.get_msg_header(timestamp=carla_gnss_measurement.timestamp))
        gnss_odometry_msg.localization.CopyFrom(self.parent.get_current_cyber_pose())
        self.gnss_odometry_writer.write(gnss_odometry_msg)

        gnss_heading_msg = Heading()
        gnss_heading_msg.header.CopyFrom(self.get_msg_header(timestamp=carla_gnss_measurement.timestamp))
        gnss_heading_msg.measurement_time = self.node.get_time()
        roll, pitch, yaw = trans.carla_rotation_to_RPY(self.carla_actor.get_transform().rotation)
        gnss_heading_msg.heading = yaw
        self.gnss_odometry_writer.write(gnss_heading_msg)

        gnss_status_msg = GnssStatus()
        gnss_status_msg.header.timestamp_sec = carla_gnss_measurement.timestamp
        gnss_status_msg.header.module_name = "gnss"
        gnss_status_msg.solution_completed = True
        gnss_status_msg.solution_status = 0
        gnss_status_msg.position_type = 56
        gnss_status_msg.num_sats = 3
        self.gnss_status_writer.write(gnss_status_msg)
