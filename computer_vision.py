import cv2

img = cv2.imread("image.jpg")

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Convert image to CMYK
cmyk = cv2.cvtColor(img, cv2.COLOR_BGR2CMYK)

# Convert image to YUV
yuv = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)

# Convert image to HLS
hls = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
