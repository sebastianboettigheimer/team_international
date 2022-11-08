import sys
import time

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber
from ecal.core.publisher import StringPublisher
import socketio

from protobuf import VehicleDynamics_pb2, SurroundViewImage_pb2, Brake_pb2, HMICanKeyboard_pb2, W3Lightbar_pb2

light_pub: StringPublisher
sio: socketio.Client
multiplier: float = 0.1
direction: int = -1

RC_IP = "172.20.10.6"
RC_PORT = 8001
MAX_SPEED = 0.5

def remote_steering(value: float):
    sio.emit('steering', dict(value=value))

def remote_throttle(value: float):
    sio.emit('throttle', dict(value=value))

# steering wheel
def steering_callback(topic_name, msg, time):
    dynamics = VehicleDynamics_pb2.VehicleDynamics()
    dynamics.ParseFromString(msg)
    steering_angle = float(dynamics.signals.steering_wheel_angle)

    #print(f'steering angle: {steering_angle}')
    remote_steering(steering_angle)

# brake
def brake_callback(topic_name, msg, time):
    brake = Brake_pb2.Brake()
    brake.ParseFromString(msg)
    brake_applied = bool(brake.signals.is_brake_applied)

    #print(f'brake: {brake_applied}')
    if brake_applied:
        remote_throttle(direction*multiplier*MAX_SPEED)
    else:
        remote_throttle(0.0)
        #print(f'braking')

# buttons
def buttons_callback(topic_name, msg, time):
    buttons = HMICanKeyboard_pb2.HmiCanKeyboardState()
    buttons.ParseFromString(msg)

    button_list = [
        int(buttons.CanKeyboard_Button_01) == 2,
        int(buttons.CanKeyboard_Button_02) == 2,
        int(buttons.CanKeyboard_Button_03) == 2,
        int(buttons.CanKeyboard_Button_04) == 2,
        int(buttons.CanKeyboard_Button_05) == 2,
        int(buttons.CanKeyboard_Button_06) == 2,
        int(buttons.CanKeyboard_Button_07) == 2,
        int(buttons.CanKeyboard_Button_08) == 2,
        int(buttons.CanKeyboard_Button_09) == 2,
        int(buttons.CanKeyboard_Button_10) == 2,
        int(buttons.CanKeyboard_Button_11) == 2,
        int(buttons.CanKeyboard_Button_12) == 2
    ]
    buttons_str = ",".join([str(e) for e in button_list])

    #print(f'buttons: {buttons_str}')

    light = W3Lightbar_pb2.W3LightbarRequest()
    if button_list[0]:
        light.take_down = False
        light.alley_light_left = True
        light.alley_light_right = True
        light.red_warning_light = True
        light.three_sixty_degree_colour_2 = True
        light.front_colour_2 = True
        light.turn_signal_left = True
        light.turn_signal_right = True
        light_pub.send(light.SerializeToString())
        #print('light on')
    else:
        light.take_down = True
        light.alley_light_left = False
        light.alley_light_right = False
        light.red_warning_light = False
        light.three_sixty_degree_colour_2 = False
        light.front_colour_2 = False
        light.turn_signal_left = False
        light.turn_signal_right = False
        light_pub.send(light.SerializeToString())
        #print('light off')

    if button_list[1]:
        global multiplier
        multiplier = multiplier + 0.1
        if multiplier >= MAX_SPEED:
            multiplier = 0.1
        print(f'speed: {multiplier*MAX_SPEED}')

    if button_list[4]:
        global direction
        direction = -direction
        print(f'reversing')

# image
#def image_callback(topic_name, msg, time):
#    image = SurroundViewImage_pb2.SurroundViewImage()
#    image.ParseFromString(msg)
#
#    image_bytes = image.data.imageData
#    width = image.data.width
#    height = image.data.height
#
#    print(f'image: {width}x{height}')

if __name__ == "__main__":
    sio = socketio.Client()
    sio.connect(f'http://{RC_IP}:{RC_PORT}')

    ecal_core.initialize(sys.argv, "BCX")
    dyn_sub = StringSubscriber("VehicleDynamicsInPb")
    dyn_sub.set_callback(steering_callback)
    brake_sub = StringSubscriber("BrakeInPb")
    brake_sub.set_callback(brake_callback)
    button_sub = StringSubscriber("HmiCanKeyboardStatePb")
    button_sub.set_callback(buttons_callback)
    #img_sub = StringSubscriber("SvcImageFrontRgbPb")
    #img_sub.set_callback(image_callback)
    light_pub = StringPublisher("W3LightbarRequestPb")
    
    try:
        while ecal_core.ok():
            time.sleep(0.005)
    except BaseException as ex:
        ecal_core.finalize()
        sio.disconnect()
        raise ex
    
    ecal_core.finalize()
    sio.disconnect()


@sio.event
def connect():
    print("socket connected")

@sio.event
def connect_error(data):
    print("docket connection failed")

@sio.event
def disconnect():
    print("socket disconnected")

