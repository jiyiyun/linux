items =['aaa',111,(4,5),201]
tests =[(4,5),3.14]

for key in tests:
	for item in items:
		print(key,"was found")
		break
	else:
		print(key,"not found!")