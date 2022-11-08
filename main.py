import sys
import time

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber

from protobuf import VehicleDynamics_pb2, SurroundViewImage_pb2, Brake_pb2, HMICanKeyboard_pb2

# steering wheel
def steering_callback(topic_name, msg, time):
    dynamics = VehicleDynamics_pb2.VehicleDynamics()
    dynamics.ParseFromString(msg)
    steering_angle = float(dynamics.signals.steering_wheel_angle)

    print(f'steering angle: {steering_angle}')

# brake
def brake_callback(topic_name, msg, time):
    brake = Brake_pb2.Brake()
    brake.ParseFromString(msg)
    brake_applied = bool(brake.signals.is_brake_applied)

    print(f'brake: {brake_applied}')

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

    print(f'buttons: {buttons_str}')

# image
#def image_callback(topic_name, msg, time):
#    image = SurroundViewImage_pb2.SurroundViewImage()
#    image.ParseFromString(msg)

#    image_bytes = image.data.imageData
#    width = image.data.width
#    height = image.data.height

#    print(f'image: {width}x{height}')

if __name__ == "__main__":
    ecal_core.initialize(sys.argv, "BCX")
    dyn_sub = StringSubscriber("VehicleDynamicsInPb")
    dyn_sub.set_callback(steering_callback)
    brake_sub = StringSubscriber("BrakeInPb")
    brake_sub.set_callback(brake_callback)
    button_sub = StringSubscriber("HmiCanKeyboardStatePb")
    button_sub.set_callback(buttons_callback)
    
    #img_sub = StringSubscriber("SvcImageFrontRgbPb")
    #img_sub.set_callback(image_callback)
    
    try:
        while ecal_core.ok():
            time.sleep(0.005)
    except BaseException as ex:
        ecal_core.finalize()
        raise ex
    
    ecal_core.finalize()
