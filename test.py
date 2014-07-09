#!/home/pi/.virtualenvs/raspi_squirtgun/bin/python

import time
import wiringpi

OUT_PIN = 1

def on():
	wiringpi.digitalWrite(OUT_PIN, wiringpi.HIGH)

def off():
	wiringpi.digitalWrite(OUT_PIN, wiringpi.LOW)

def pulse(delay=0.5):
	on()
	time.sleep(delay)
	off()

def setup():
	wiringpi.wiringPiSetup()
        wiringpi.pinMode(OUT_PIN, wiringpi.OUTPUT)

def main():
	time.sleep(1)
	pulse(0.25)

if __name__ == '__main__':
	setup()
	main()
