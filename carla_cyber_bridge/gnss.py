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

from .sensor import Sensor

from modules.drivers.gnss.proto.gnss_best_pose_pb2 import GnssBestPose
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

        self.gnss_navsatfix_writer = node.new_writer("/apollo/sensor/gnss/fix",
                                           GnssBestPose,
                                           qos_depth=10)
        self.gnss_odometry_writer = node.new_writer("/apollo/sensor/gnss/odometry",
                                           Gps,
                                           qos_depth=10)
        self.listen()

    def destroy(self):
        super(Gnss, self).destroy()
        self.node.destroy_writer(self.gnss_status_writer)
        self.node.destroy_writer(self.gnss_odometry_writer)

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
