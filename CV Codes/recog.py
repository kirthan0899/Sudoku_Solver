import pytesseract
import cv2
from PIL import Image
from statistics import mean

# create a textfile to store the recognized digits from the each slice
f = open('data.txt','w')
# create an empty list to store the accuracy values
l=[]
print
print("Digit	Accuracy")
for i in range(1,10):
	for j in range(1,10):
		# read each slice one by one
		im = Image.open('slice_img_'+str(i)+'_'+str(j)+'.png')
		# get the width and height of the slice
		width, height = im.size

		x1=10
		y1=10
		x2=width-10
		y2=height-10
		img=cv2.imread('slice_img_'+str(i)+'_'+str(j)+'.png')
		crop_img = img[y1:y2, x1:x2]
		# blur the image so it is easy to identify
		blur_img=cv2.blur(crop_img,(3, 3))
		# pass the blurred image to pytesseract which will recognize the digits in the image using OCR
		data = pytesseract.image_to_string(blur_img, lang='eng', config='--psm 6 -c tessedit_char_whitelist=0123456789')
		if data=='':
			# if there are no digits in the image, print 0
			print("0	"),
			# write the recognized digit i.e., '0' to the file
			f.write('0')
		else:
			print("{}	".format(data)),
			# write the recognized digit to the file
			f.write(str(data))
		# get the output from pytesseract as a dataframe and store it in text
		text = pytesseract.image_to_data(blur_img, lang='eng', config='--psm 6 -c tessedit_char_whitelist=0123456789', output_type='data.frame')

		# filter out the row which contains the accuracy value
		text = text[text.conf != -1]
		if(text.empty==True):
			# append the accuracy value to the list
			l.append(98)
			print([98])
		else:
			# append the accuracy value to the list
			l.append(int(text['conf'].values))
			print(text['conf'].values)
print
print "The Minimum Accuracy of the recognized digits = ", min(l)
print "The Avearge Accuracy of the recognized digits = ", mean(l)
print "The Maximum Accuracy of the recognized digits = ", max(l)
print
