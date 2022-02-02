load("//tools:cpplint.bzl", "cpplint")

package(default_visibility = ["//visibility:public"])

proto_library(
    name = "carla_proto_lib",
    srcs = [
        "carla_bounding_box.proto",
        "carla_clock.proto",
        "carla_spawn_object.proto",
        "carla_status.proto",
        "carla_world_info.proto",
        "carla_traffic_light_status.proto",
    ],
    deps = [
        "//modules/localization/proto:pose_proto_lib",
    ],
)
