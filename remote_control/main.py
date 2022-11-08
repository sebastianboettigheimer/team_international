import time
from jetracer.nvidia_racecar import NvidiaRacecar

if __name__ == "__main__":
    car = NvidiaRacecar()
    car.throttle = 0
    car.steering = 0

    if True:
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

    if True:
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

