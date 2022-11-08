import time
from jetracer.nvidia_racecar import NvidiaRacecar
from flask import Flask, request
import json

if __name__ == "__main__":
    car = NvidiaRacecar()
    car.throttle = 0
    car.steering = 0

    if False:
        print('steering test ', end='', flush=True)
        car.steering = -1.0
        while car.steering < 1.0:
            car.steering += 0.05
            time.sleep(0.1)
        for i in range(10):
            car.steering = 1.0
            time.sleep(0.5)
            car.steering = -1.0
            time.sleep(0.5)
        car.steering = 0
        print('completed')

    if False:
        print('throttle test ', end='', flush=True)
        car.throttle = 0
        while car.throttle > -1.0:
            car.throttle -= 0.1
            time.sleep(0.2)
        car.throttle = 0

        time.sleep(1)
        while car.throttle < 1.0:
            car.throttle += 0.1
            time.sleep(0.2)
        car.throttle = 0
        print('completed')
 
    app = Flask(__name__)
    print('initialized')

    @app.route('/steering', methods=['POST'])
    def index():
        record = json.loads(request.data)
        if 'value' in record:
            car.steering = record.get('value')
        return dict()
    app.run(debug=True, host='0.0.0.0')

