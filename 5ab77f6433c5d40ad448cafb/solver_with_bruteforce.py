import sys
import itertools


def ground(num):
	t0 = (num & 0x0F) >> 0
	t1 = (num & 0x0F00) >> 0x8
	t2 = (num & 0x0F0000) >> 0x10
	t3 = (num & 0x0F000000) >> 0x18
	t4 = (num & 0xF0) >> 4
	t5 = (num & 0xF000) >> 0xC
	t6 = (num & 0xF00000) >> 0x14
	t7 = (num & 0xF0000000) >> 0x1C
	return (t7 << 0x1c) | (t6 << 0x18) | (t5 << 0x14) | (t4 << 0x10) | (t3 << 0x0C) | (t2 << 0x08) | (t1 << 0x04) | t0

def get_serial(name):
	value = 0x3892DEBA
	checksum = 0
	for c in name:
		checksum = (checksum + ground(ord(c) * value)) & 0xFFFFFFFF
		value = (value + 0x13371337) & 0xFFFFFFFF
	return checksum

def check_serial(name, word):
	a = b = False
	serial_ = "{0:#X}".format(get_serial(sys.argv[1]))[2:]
	serial_a, serial_b = serial_[0:4], serial_[4:8]
	if word == serial_a:
		a = True
	if word == serial_b:
		b = True
	return a, b

if __name__ == "__main__":
	if len(sys.argv) == 2:
		charset = "0123456789ABCDEF"
		serial_a =  serial_b = ""
		for x in itertools.product(charset, charset, charset, charset):
			word = ''.join(x)
			#print("Try: {0}".format(word))
			result = check_serial(sys.argv[1], word)
			if result[0] == True:
				serial_a = word
				print("Success: first = {0}".format(word))
			if result[1] == True:
				serial_b = word
				print("Success: second = {0}".format(word))
		print("Serial: xD-{0}-{1}".format(serial_a, serial_b))
	else:
		print("usage: {0} <name>".format(sys.argv[0]))