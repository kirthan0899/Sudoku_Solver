
from __future__ import division
from PIL import Image
import math
import os

# Load the image
init = Image.open("test.png")
# calculate the width and height of the image
width, height = init.size
ss = int(math.ceil(height/9))
print

def long_slice(out_name, outdir, slice_size):
    # slice an image into parts slice_size tall
	img = Image.open("test.png")
	width, height = img.size
	upper = 0
	slices_height = int(math.ceil(height/slice_size))
	slices_width = int(math.ceil(width/slice_size))

	count1 = 1
	for slice_height in range(slices_height):
		left = 0
		#if we are at the end, set the lower bound to be the bottom of the image
		if count1 == slices_height:
			lower = height
		else:
			lower = int(count1 * slice_size) 
		count2 = 1
		for slice_width in range(slices_width):
			#if we are at the end, set the lower bound to be the bottom of the image
			if count2 == slices_width:
				right = width
			else:
				right = int(count2 * slice_size)  
			#set the bounding box     
			bbox = (left, upper, right, lower)
			working_slice = img.crop(bbox)
            
			#save the slice
			working_slice.save(os.path.join(outdir, "slice_" + out_name + "_" + str(count1)+ "_" + str(count2)+".png"))
			print(left, upper, right, lower)
			print(outdir, "slice_" + out_name + "_" + str(count1)+ "_" + str(count2)+".png")
			left += slice_size
			count2 +=1 
		upper += slice_size
		count1 +=1

if __name__ == '__main__':
	#slice_size is the max height of the slices in pixels
	long_slice("img", os.getcwd(), ss)
