import csv
import os
'''
    This parser was made in order to make image-text labeling easier. 
'''

file_name_list = os.listdir('./s3')
file_name_list.sort()
'''
for i in range(len(file_name_list)):
	print(file_name_list[i])
	if i == 10:
		break
'''
#file_name_list.remove('parser.py')
#file_name_list.remove('1.txt')
#file_name_list.remove('2.txt')
#file_name_list.remove('3.txt')
#print(file_name_list)
'''
if os.path.exists('1.txt'):
    print(len('1.txt'))
else:
    print('nn')
'''
#exit(1)

f1 = open('3.txt', 'wt')
#f2 = open('2.txt', 'wt')
#f3 = open('3.txt', 'wt')


for i, file_name in enumerate(file_name_list):
#    if i < 100:
	f1.write(file_name + '/' + '\n') 

