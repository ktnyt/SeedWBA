from environment import Environment

import cv2
from minidora import Minidora
from minidora.dc_motor import DcMotorData
from minidora.servo_motor import ServoMotorData


class MinidoraEnv(Environment):
    def __init__(self, localhost, remotehost):
        super(MinidoraEnv, self).__init__(10)
        self.client = Minidora(self_host=localhost, minidora_host=remotehost)

        self.image = None
        self.pose = None

        def update_camera(image):
            self.image = image

        def update_pose(pose):
            self.pose = pose

        self.image_thread = self.client.listen_to_camera(update_camera)
        self.pose_thread = self.client.listen_to_pose(update_pose)

        #while self.pose is None or self.image is None:
        #    continue

    def step(self, action):
        servo = ServoMotorData()
        if "armleft" in action: servo.arm.left = (action["armleft"] / 2 + 0.5)
        if "armright" in action: servo.arm.right = (action["armright"] / 2 + 0.5)
        if "headroll" in action: servo.head.roll = action["headroll"]
        if "headpitch" in action: servo.head.pitch = action["headpitch"]
        if "headyaw" in action: servo.head.yaw = action["headyaw"]
        self.client.move_servo_motor(servo)

        dc = DcMotorData()
        if "wheelleft" in action: dc.wheel.left = action["wheelleft"] * 100
        if "wheelright" in action: dc.wheel.right = action["wheelright"] * 100
        self.client.move_dc_motor(dc)

        observation = {
            'image': self.image,
            'pose': self.pose,
        }
        reward = 1
        done = None
        info = None

        return observation, reward, done, info

    def render(self):
        pass

    def reset(self):
        pass
