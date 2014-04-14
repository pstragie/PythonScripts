#!/usr/bin/python
import os
var = os.getcwd()
for dirpath, dirnames, filenames in os.walk(var):
	for file in filenames:
		if len(file) > 20:
			name = file.split("_")[1].lstrip("sample")
			os.rename(dirpath + '/' + file, dirpath + '/' + name + '.fa')