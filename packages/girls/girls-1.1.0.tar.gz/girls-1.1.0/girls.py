def queen(girls, level):
	for each_girl in girls:
		if isinstance(each_girl,list):
			queen(each_girl,level)
		else:
			for tab_stop in range(level):
				print("\t", end='')
			print(each_girl)
