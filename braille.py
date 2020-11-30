from gtts import gtts
import vlc
import sys
import time
import gpiozero
from gpiozero.pins.mock import mockfactory
from gpiozero import button

#gpiozero.device.pin_factory = mockfactory()

prev_button = button(2)  #pin 5 = gpio 2
next_button = button(3)

pin1 = gpiozero.outputdevice(17, active_high=true, initial_value=false)
pin2 = gpiozero.outputdevice(23, active_high=true, initial_value=false)
pin3 = gpiozero.outputdevice(27, active_high=true, initial_value=false)
pin4 = gpiozero.outputdevice(24, active_high=true, initial_value=false)
pin5 = gpiozero.outputdevice(22, active_high=true, initial_value=false)
pin6 = gpiozero.outputdevice(25, active_high=true, initial_value=false)

pins = {
	1: pin1,
	2: pin2,
	3: pin3,
	4: pin4,
	5: pin5,
	6: pin6
	}

braille_chars = {
		"a": list("100000"),
		"b": list("101000"),
		"c": list("110000"),
		"d": list("110100"),
		"e": list("100100"),
		"f": list("111000"),
		"g": list("111100"),
		"h": list("101100"),
		"i": list("011000"),
		"j": list("011100"),
		"k": list("100010"),
		"l": list("101010"),
		"m": list("110010"),
		"n": list("110110"),
		"o": list("100110"),
		"p": list("111010"),
		"q": list("111110"),
		"r": list("101110"),
		"s": list("011010"),
		"t": list("011110"),
		"u": list("100011"),
		"v": list("101011"),
		"w": list("011101"),
		"x": list("110011"),
		"y": list("110111"),
		"z": list("100111"),
		" ": list("000000"),
		".": list("010001"),
		"!": list("011011"),
		"?": list("110101"),
		",": list("000001"),
		"0": list("000111"),
		"1": list("001000"),
		"2": list("001010"),
		"3": list("001100"),
		"4": list("001101"),
		"5": list("001001"),
		"6": list("001110"),
		"7": list("001111"),
		"8": list("001011"),
		"9": list("000110")
		}

keys = list(braille_chars)
last = len(keys) - 1

current = 0

def print_list():
	for i in braille_chars:
		print(i + " - " + str(braille_chars[i]))

def get_values():
	print(" -> " + keys[current] + " - ", end="")
	for i in range(1, 7):
		print(pins[i].value, end="")
	print(" ")

def reset():
	for i in range(1, 7):
		pins[i].off()
	time.sleep(0.2)

def display(key):
	reset()
	values = braille_chars[key]
	for i in range(1, 6):
		if(values[i] == "1"):
			pins[i].on()
	get_values()
	time.sleep(1)

def show_prev():
	global current
	if(current == 0):
		current = last
	else:
		current -= 1
	display(keys[current])

def show_next():
	global current
	if(current == last):
		current = 0
	else:
		current += 1
	display(keys[current])

def text_to_speech():
	speech = gtts(text = text, lang = 'en', slow = false)
	speech.save("test.mp3")
	p = vlc.mediaplayer("./test.mp3")
	p.play()

def start():
	#text_to_speech()
	display(keys[current])
	while(1):
		show_next()
		if prev_button.is_pressed:
			show_prev()

		if next_button.is_pressed:
			show_next()

if __name__ == "__main__":
	try:
		start()
	except keyboardinterrupt:
		# turn the relay off
		reset()
		print("\nexiting application\n")
		# exit the application
		sys.exit(0)
