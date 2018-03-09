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

        self.image_thread = self.client.listen_to_camera(
            update_camera, block=False)
        self.pose_thread = self.client.listen_to_pose(update_pose, block=False)

        while self.pose is None or self.image is None:
            continue

    def step(self, action):
        larm = action[0]
        rarm = action[1]
        lleg = action[2]
        rleg = action[3]

        servo = ServoMotorData()
        servo.arm.left = (larm / 2 + 0.5)
        servo.arm.right = (rarm / 2 + 0.5)
        self.client.move_servo_motor(servo)

        dc = DcMotorData()
        dc.wheel.left = lleg * 100
        dc.wheel.right = rleg * 100
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
