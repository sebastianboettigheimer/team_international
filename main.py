import sys
import time

import ecal.core.core as ecal_core
from ecal.core.subscriber import StringSubscriber

def callback(topic_name, msg, time):
  print(f'{time} {topic_name}')
  print(type(msg))

if __name__ == "__main__":
  ecal_core.initialize(sys.argv, "BCX")
  sub = StringSubscriber("HmiCanKeyboardStatePb")
  sub.set_callback(callback)
  
  while ecal_core.ok():
    time.sleep(0.005) 
  
  ecal_core.finalize()
