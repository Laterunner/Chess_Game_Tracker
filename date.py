# date.py V 1.0
# Oct 19th 2023, Dr. Mariu Bartsch
#show and print SCORESHEET


import cv2
import tee
from cv2 import blur    

import numpy as np
import threading
import time
from datetime import datetime
import subprocess
import os
import sys
from detect_points import get_points
from read_warp_img import get_warp_img
import cvzone
import pickle
import chess
import chess.engine
from engine import legal_moves_2
from engine import move_pair_in_list
from engine import update_FEN
from enginefunctions import eval
from enginefunctions import get_field_no
# from text_helper import text_function
import cairosvg
import chess.svg
from IPython.display import SVG
import webbrowser

from datetime import datetime
import time
import fentoboardimage
#print(time.time())
#print(datetime.today().strftime("%Y-%rm-%d, %H:%M"))
print(datetime.today().strftime("%A, %B %d, %Y %H:%M:%S"))

time0=time.time()

Imagefile = cv2.imread("/home/marius/fen-to-png/output/result.png")
'''
while True:
	cv2.imshow("imagefile",Imagefile)
	
	k = cv2.waitKey(1)
	if k == ord('q')or k ==27 :
		cv2.destroyAllWindows()	
		break
	
	time1=time.time()
	print(time1-time0)

'''
 
# subprocess.call("clear")

##########################################
### V1 data as given
##########################################
	# test Data:

san_move_list1 = "1.  Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,10. Qb3 Nxc3 "
san_move_list2 = "11. Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,20. Qb3 Nxc3 "
san_move_list3 = "21. Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,30. Qb3 Nxc3 "
san_move_list4 = "31. Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,40. Qb3 Nxc3 "
san_move_list5 = "41. Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,50. Qb3 Nxc3 "
san_move_list6 = "51. Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,60. Qb3 Nxc3 "
san_move_list7 = "61. Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,70. Qb3 Nxc3 "
san_move_list8 = "71. Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,80. Qb3 Nxc3 "
san_move_list9 = "81. Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,90. Qb3 Nxc3 "
san_move_list10 = "91. Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,10. Qb3 Nxc3 "
san_move_list11 = "101. Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,110. Qb3 Nxc3 "
san_move_list12 = "111. Nf3 Nf6 ,2. c4 g6 ,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O ,6. Nf3 Re8 ,7. d3 d5 ,8. cxd5 Nxd5 ,9. Bd2 Bg4 ,120. Qb3 Nxc3 "
san_move_list13 = "1. Nf3 Nf6 ,2. c4 g6 "#,3. Nc3 Bg7 ,4. e4 e5 ,5. Nxe5 O-O "

san_move_list = (

					str(san_move_list1)  + " ," +  str(san_move_list2) 
					 + " ," + str(san_move_list3)+ " ," + str(san_move_list4) + " ," + str(san_move_list5)
					+ " ," + str(san_move_list6) + " ," + str(san_move_list7) + " ," + str(san_move_list8) + " ," + str(san_move_list9) + " ," + str(san_move_list10)
					+ " ,"+ str(san_move_list11) + " ," + str(san_move_list12) + " ," + str(san_move_list13)
				)
# make list x, use correct separator
x = san_move_list.split(" ,")

subprocess.run("clear")
#print("yx = ",yx)


# carlson 136 moves
carlson_pgn = (\
	"1. d4 Nf6 2. Nf3 d5 3. g3 e6 4. Bg2 Be7 5. O-O O-O 6. b3 c5 7. dxc5 Bxc5 8. c4 dxc4 9. Qc2 Qe7 10. Nbd2 Nc6 11. Nxc4 b5 12. Nce5 Nb4 13. Qb2 Bb7 14. a3 Nc6 15. Nd3 Bb6 16. Bg5 Rfd8 17. Bxf6 gxf6 18. Rac1 Nd4 19. Nxd4 Bxd4 \
	20. Qa2 Bxg2 21. Kxg2 Qb7+ 22. Kg1 Qe4 23. Qc2 a5 24. Rfd1 Kg7 25. Rd2 Rac8 26. Qxc8 Rxc8 27. Rxc8 Qd5 28. b4 a4 29. e3 Be5 30. h4 h5 31. Kh2 Bb2 32. Rc5 Qd6 33. Rd1 Bxa3 34. Rxb5 Qd7 35. Rc5 e5 36. Rc2 Qd5 37. Rdd2 Qb3 38. Ra2 e4 39. Nc5 Qxb4 \
	40. Nxe4 Qb3 41. Rac2 Bf8 42. Nc5 Qb5 43. Nd3 a3 44. Nf4 Qa5 45. Ra2 Bb4 46. Rd3 Kh6 47. Rd1 Qa4 48. Rda1 Bd6 49. Kg1 Qb3 50. Ne2 Qd3 51. Nd4 Kh7 52. Kh2 Qe4 53. Rxa3 Qxh4+ 54. Kg1 Qe4 55. Ra4 Be5 56. Ne2 Qc2 57. R1a2 Qb3 58. Kg2 Qd5+ 59. f3 Qd1 \
	60. f4 Bc7 61. Kf2 Bb6 62. Ra1 Qb3 63. Re4 Kg7 64. Re8 f5 65. Raa8 Qb4 66. Rac8 Ba5 67. Rc1 Bb6 68. Re5 Qb3 69. Re8 Qd5 70. Rcc8 Qh1 71. Rc1 Qd5 72. Rb1 Ba7 73. Re7 Bc5 74. Re5 Qd3 75. Rb7 Qc2 76. Rb5 Ba7 77. Ra5 Bb6 78. Rab5 Ba7 79. Rxf5 Qd3 \
	80. Rxf7+ Kxf7 81. Rb7+ Kg6 82. Rxa7 Qd5 83. Ra6+ Kh7 84. Ra1 Kg6 85. Nd4 Qb7 86. Ra2 Qh1 87. Ra6+ Kf7 88. Nf3 Qb1 89. Rd6 Kg7 90. Rd5 Qa2+ 91. Rd2 Qb1 92. Re2 Qb6 93. Rc2 Qb1 94. Nd4 Qh1 95. Rc7+ Kf6 96. Rc6+ Kf7 97. Nf3 Qb1 98. Ng5+ Kg7 99. Ne6+ Kf7 \
	100. Nd4 Qh1 101. Rc7+ Kf6 102. Nf3 Qb1 103. Rd7 Qb2+ 104. Rd2 Qb1 105. Ng1 Qb4 106. Rd1 Qb3 107. Rd6+ Kg7 108. Rd4 Qb2+ 109. Ne2 Qb1 110. e4 Qh1 111. Rd7+ Kg8 112. Rd4 Qh2+ 113. Ke3 h4 114. gxh4 Qh3+ 115. Kd2 Qxh4 116. Rd3 Kf8 117. Rf3 Qd8+ 118. Ke3 Qa5 119. Kf2 Qa7+ \
	120. Re3 Qd7 121. Ng3 Qd2+ 122. Kf3 Qd1+ 123. Re2 Qb3+ 124. Kg2 Qb7 125. Rd2 Qb3 126. Rd5 Ke7 127. Re5+ Kf7 128. Rf5+ Ke8 129. e5 Qa2+ 130. Kh3 Qe6 131. Kh4 Qh6+ 132. Nh5 Qh7 133. e6 Qg6 134. Rf7 Kd8 135. f5 Qg1 136. Ng7"\
	)

j= ""
carlson_list = carlson_pgn.split(". ")
print("CARLSON ",len(carlson_list))
for i in range(len(carlson_list),):
	uf= carlson_list
	print(uf[i], end = "")
	
	i=i+3



##########################################
### V2 data as generated by xptestx.py
##########################################
# list xxx
# xxx = [' 1. e4', ' e5', ' 2. Nf3', ' d5', ' 3. exd5', ' Qxd5',  ' 4. Nc3', ' Qa5', ' 5. d4', ' Bg4', ' 6. Bc4', ' Nc6', ' 7. Bxf7+', ' Kxf7', ' 8. d5', ' Nf6', ' 9. dxc6', ' bxc6', ' 10. h3', ' Bxf3', ' 11. Qxf3', ' e4', '12. Qe2', ' Bb4', ' 13. Bd2', ' Rhd8', ' 14. Qc4+', ' Rd5', ' 15. O-O-O', ' Rb8', ' 16. Rhe1', ' Ba3', ' 17. Na4', ' Qxa4', ' 18. Qxa4', ' Bxb2+', ' 19. Kb1', ' Bc3+', ' 20. Kc1', ' Bb2+', ' 21. Kb1', ' Bc3+']

data1 = [' 1. e4', ' e5', ' 2. Nf3', ' d5', ' 3. exd5', ' Qxd5',  ' 4. Nc3', ' Qa5', ' 5. d4', ' Bg4', ' 6. Bc4', ' Nc6', ' 7. Bxf7+', ' Kxf7', ' 8. d5', ' Nf6', ' 9. dxc6', ' bxc6', ' 10. h3', ' Bxf3', ' 11. Qxf3', ' e4', ' 12. Qe2', ' Bb4', ' 13. Bd2', ' Rhd8', ' 14. Qc4+', ' Rd5', ' 15. O-O-O', ' Rb8', ' 16. Rhe1', ' Ba3', ' 17. Na4', ' Qxa4', ' 18. Qxa4', ' Bxb2+', ' 19. Kb1', ' Bc3+', ' 20. Kc1', ' Bb2+', ' 21. Kb1', ' Bc3+']
#data1 = ['1. f4', ' f5', ' 2. Nf3', ' g6', ' 3. g3', ' Bg7', ' 4. Bg2']
# preprocess x
data1 = uf

# data1 = ['1. f4', ' f5', ' 2. Nf3' ] #, ' g6'
# data1 = [' 1. f4' , ' f5', ' 2. Nf3']#  , ' g6']
print(data1)
print()

joined= ( " , ").join(data1[0:]) # jetzt ein str
print("joined : ",  joined) 
### remove ", " :
new = joined.replace(" , ", ". ")
print("new", new)


# print("split: ", data1.split(" , "))
print(3*"\n")



'''
print(len(data1))
i=0
k=[]
while i < (len(data1)):
	if i < len(data1)-1:
		z1 = str(data1[i]).ljust(11)  + str(data1[i+1]).ljust(11)
		# print(z1)
		k.append(z1)
	else: 
		k.append(str(data1[i]))
	i= i +2

# print(k)
x= k
'''

# x= ""
###


###



'''
if len(data1) %2 ==0:
	for i in range(0,len(data1),2):
		j= (data1)[i] + (data1)[i+1]
		k.append(j)
		i = i+1

'''

def show_scoresheet(x):
	print()
	print()
	print("x = ",x)

	######################################################
	### for debug insert "#" below
	######################################################
	subprocess.call("clear")

	def san_print(x):
		if len(x) <= 60:
			pages=1
		if len(x) > 60:
			pages=2
		if len(x) > 120:
			pages=3
			print("Page 3 is not yet ready")
		i=0
		tab= 71
		###############################################################################################
		######    Start scoresheet page 1
		###############################################################################################
		#print(3*"\n")

		print(3*"\n")
		print( 2*"\t    ", " - SCORE SHEET V 1.0 -" )
		print("          Game played", datetime.today().strftime("%A, %B %d, %Y %H:%M:%S"))
		print(4*"\n")
		
		print("White Player: " , 16*".", "\t",  "Black Player:", 16*".")
		print(tab*"_", end="")
		print("\n")
		print("moves 1-20", "\t\t", "moves 21-40", "\t\t", "moves 41-60")

		for s in range(tab):
			print("_", end="")
		print("\n")

		### start writing data to table
		while i < 20:
			if len(x) <= 20 and i < len(x):
				print( str(x[i:i+1])[2:-2])

			if len(x) <= 20 and i > len(x): 
				print( (str(i)+ ". ").rjust(5) + ".....   .....")

			if len(x)  <=40 and len(x) >20:
				if i < 20:
					print( str(x[i:i+1])[2:-2], "\t", str(x[i+20:i+21])[2:-2])

			if len(x) <= 60 and len(x) >40:
				if i < 20:
					print(str(x[i:i+1])[2:-2], "\t\t", str(x[i+20:i+21])[2:-2], "\t\t", str(x[i+40:i+41])[2:-2],  )
			
			if (len(x) >60): 	#ok
				if i < 20:
					print(str(x[i:i+1])[2:-2], "\t\t", str(x[i+20:i+21])[2:-2], "\t\t", str(x[i+40:i+41])[2:-2],)
			i=i+1

		for s in range(tab):
			print("_", end="")
		print("\n")
		print("Page 1 of", pages, ", ", "total moves= ",len(x),)
		
		if len(x)  <= 60:
			print("Scoresheet saved to outputfile.log")
		print("\n")

		if len(x) > 60:
			###############################################################################################
			######    Start scoresheet page 2
			######    works for moves 1-119  
			###############################################################################################
			i=0
			# print(3*"\n")
			print( 2*"\t    ", " - SCORE SHEET V 1.0 -" )
			print("          Game played", datetime.today().strftime("%A, %B %d, %Y %H:%M:%S"))
			print(5*"\n")
			print("White Player: " , 16*".", "\t",  "Black Player:", 16*".")
			print(tab*"_", end ="")
			print("\n")
			print("moves 61-80", "\t\t", "moves 81-100", "\t\t", "moves 101-120",)
			print(tab*"_",end="")
			print("\n")

			while i < 20:		#print(i)
			#print("len ",len(x))
		
				if len(x) <= 20 and i < len(x):
					print(str(x[i:i+1])[2:-2],)

				if len(x) <= 20 and i > len(x): 
					print()
				
				if len(x)  <=40 and len(x) >20:
					if i < len(x)%20:
						#pass
						print(str(x[i:i+1])[2:-2], "\t\t", str(x[i+20:i+21])[2:-2], )
					else:
						print(str(x[i:i+1])[2:-2],  )
				
				if len(x) <= 60 and len(x) >40:
					if i < len(x)%20:
						print(str(x[i:i+1])[2:-2], "\t\t", str(x[i+20:i+21])[2:-2], "\t\t", str(x[i+40:i+41])[2:-2],  )
				
				if (len(x) <= 80 and len(x) >60):	#ok
					if i < len(x)%20:		#print(i)
			#print("len ",len(x))
		
						print(str(x[i+60:i+61])[2:-2],)
				
				if len(x) <= 100 and len(x) >80:
					if i < len(x):			
						print( str(x[i+60:i+61])[2:-2],"\t\t", str(x[i+80:i+81])[2:-2],)
					
				if len(x) <= 120 and len(x) >100:
					if i < len(x):			
						print( str(x[i+60:i+61])[2:-2], "\t\t", str(x[i+80:i+81])[2:-2], "\t\t", str(x[i+100:i+101])[2:-2])

				i=i+1
				
			for s in range(tab): # 
				print("_", end="")  # Table format underline
			print("\n")
			print("Page 2 of", pages, ", ", "total moves= ",len(x),)


		if len(x) > 120:
			print("Seite 3 kommt")





	########################################
	# Print to Printer:
	# change  sys.stdout to file
	# save SCORESHEET to file
	# print SCORESHEET as file to screen
	# print SCORESHEET to printer
	########################################
	original_stdout= sys.stdout
	with open("outputfile.log", "w") as f:
		sys.stdout= f 	# change std to file
		san_print(x) # 
		sys.stdout = original_stdout 	#back to normal

	with open('outputfile.log', 'r') as text_file:
		# Read and print the entire file line by line
		for line in text_file:
			print(line, end='') 
		#os.system("lp outputfile.log") 	 # print SCORE SHEET
print("Scoresheet saved to outputfile.log")
if __name__ == "__main__":
	show_scoresheet(x)
### EOF
