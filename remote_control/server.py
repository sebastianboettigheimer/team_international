import time
from jetracer.nvidia_racecar import NvidiaRacecar
import eventlet
import socketio

car = None

sio = socketio.Server()
app = socketio.WSGIApp(sio, static_files={
    '/': {'content_type': 'text/html', 'filename': 'index.html'}
})

@sio.event
def connect(sid, environ):
    car.throttle = 0
    car.steering = 0
    print('connect ', sid)

@sio.event
def steering(sid, data):
    value = data["value"]
    car.steering = value*1.5
    print('message ', data)

@sio.event
def throttle(sid, data):
    value = data["value"]
    car.throttle = value
    print('message ', data)

@sio.event
def disconnect(sid):
    car.throttle = 0
    car.steering = 0

    print('disconnect ', sid)

if __name__ == '__main__':
    car = NvidiaRacecar()
    time.sleep(1)
    car.throttle = 0
    car.steering = 0

    # if False:
    #     print('steering test ', end='', flush=True)
    #     car.steering = -1.0
    #     while car.steering < 1.0:
    #         car.steering += 0.05
    #         time.sleep(0.1)
    #     for i in range(10):
    #         car.steering = 1.0
    #         time.sleep(0.5)
    #         car.steering = -1.0
    #         time.sleep(0.5)
    #     car.steering = 0
    #     print('completed')

    eventlet.wsgi.server(eventlet.listen(('', 8001)), app)