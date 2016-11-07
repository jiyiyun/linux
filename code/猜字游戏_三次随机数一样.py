import random

i = 0

xnum =random.randint(0,9)

while  i < 5:
	print('****************')
	num = int(input("Please in put a number between 1 to 10\n"))

	x = 3 - i

	if num == xnum:
		print("Yes Guess Right")
		break
	elif num > xnum:
		print("Bigger than Random,chance Only %d " %x)
	elif num < xnum:
		print("Small than Randon ,chance Only %d " %x)

	i +=1