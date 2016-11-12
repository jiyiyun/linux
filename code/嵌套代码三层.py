while  True:
	reply = input("输入一个数字")
	if reply == "stop":
		break
	elif not reply.isdigit():
		print("bad" * 8)
	else:
		num = int(reply)
		if num <20:
			print("low")
		else:
			print(num ** 2)
print("再见")