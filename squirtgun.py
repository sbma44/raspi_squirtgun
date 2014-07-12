#!/home/pi/.virtualenvs/raspi_squirtgun/bin/python
import time

class Squirtgun(object):
    """Controls custom-built Raspberry Pi-controlled supersoaker"""
    
    OUT_PIN = 1

    def __init__(self, debug=False):
        super(Squirtgun, self).__init__()
        self.debug = debug

        if not self.debug:
            import wiringpi
            self.wiringpi = wiringpi
            self.wiringpi.wiringPiSetup()
            self.wiringpi.pinMode(self.OUT_PIN, self.wiringpi.OUTPUT)

    def _on(self):
        if not self.debug:
            self.wiringpi.digitalWrite(self.OUT_PIN, self.wiringpi.HIGH)

    def _off(self):
        if not self.debug:
            self.wiringpi.digitalWrite(self.OUT_PIN, self.wiringpi.LOW)

    def pulse(self, delay=0.5):
        if self.debug:
            print 'firing squirtgun for %0.1f seconds' % delay
        self._on()
        time.sleep(delay)
        self._off()
        if self.debug:
            print 'done.'

if __name__ == '__main__':
    sg = Squirtgun()
    sg.pulse()
