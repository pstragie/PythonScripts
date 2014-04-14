#!/usr/bin/python
import os
var = os.getcwd()
dct = {}
for dirpath, dirnames, filenames in os.walk(var):
	for file in filenames:
		if file.endswith("ani_output.txt"):
			invoer = open(dirpath+'/'+file, 'r')
			regel = invoer.readline().rstrip()
			if len(regel) > 1:
				
				A, B, C, D, E, F, G, H, I, J = regel.split("\t")
				orgA = A.split("/")[-1].rstrip(".fa")
				orgB = B.split("/")[-1].rstrip(".fa")
				aniF = F
				aniR = H
				aniDual = J
				combo = orgA + "_" + orgB
				dct[combo] = [aniF, aniR, aniDual]
for k, v in dct.items():
	print("{0:30}: {1:30}".format(k, v))
print("____________________________")
teller = 0
for k, v in dct.items():
	if float(v[2]) >= 95:
		teller += 1
		print("{0:30}: {1:30}".format(k, v))
print(teller)