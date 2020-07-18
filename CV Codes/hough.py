import numpy as np
import cv2
from PIL import Image
import PIL

# Load the image
img = cv2.imread('output.png')
rows, cols, channels = img.shape

# Convert it to gray scale and detect the edges
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray, threshold1=50, threshold2=150, apertureSize=3)

# Obtain the Hough transform
deltaRho = 1
deltaTheta = np.pi / 180
threshold = 200
lines = cv2.HoughLines(edges, deltaRho, deltaTheta, threshold)

# Paint the lines on the image
maxLength = np.sqrt(rows ** 2 + cols ** 2)

for rho, theta in lines[:, 0]:
	cos = np.cos(theta)
	sin = np.sin(theta)
	x0 = rho * cos
	y0 = rho * sin
	x1 = int(x0 + maxLength * sin)
	y1 = int(y0 - maxLength * cos)
	x2 = int(x0 - maxLength * sin)
	y2 = int(y0 + maxLength * cos)
	cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

# Obtain the probabilistic Hough transform
deltaRho = 1
deltaTheta = np.pi / 180
threshold = 100
minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges, deltaRho, deltaTheta, threshold, minLineLength=minLineLength, maxLineGap=maxLineGap)

# Paint the lines on the image
a=[]
b=[]
c=[]
d=[]
i=0
for x1, y1, x2, y2 in lines[:, 0]:
	i+=1
	a.append(x1)
	b.append(x2)
	c.append(y1)
	d.append(y2)
q = max(a)
w = min(a)
e = max(b)
r = min(b)
t = max(c)
y = min(c)
u = max(d)
i = min(d)

crop = img[y:u,w:e]

cv2.imwrite('test.png',crop)
file = Image.open('test.png')
width, height = file.size
if width < height:
	file = file.resize((width, width), PIL.Image.ANTIALIAS)
else:
	file = file.resize((height, height), PIL.Image.ANTIALIAS)
    
# Save the image
file.save('test.png')
cv2.waitKey(0)
cv2.destroyAllWindows()
