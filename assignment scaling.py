import numpy as np
import cv2
global mouseX, mouseY

###################################################
###################################################


def trycatch(img):  # function checking whether image is empty or not
    try:
        if img == None:
            return True
    except:
        return False
#######################################################
#######################################################


def mouse_handler(event, x, y, flags, param):
    global mouseX, mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        mouseX, mouseY = x, y

###################################################
##################################################


# code for zooming out pixels
# deleting alternative row and columns
# zoomed_out_image-->> output image
def zoom_out_replication(image):
    height = image.shape[0]
    width = image.shape[1]
    # declaring a blank image
    zoomed_out_image = 255 * np.ones((height//2, width//2), np.uint8)
    # taking alternative values from original image and saving it to output image
    for row in range(zoomed_out_image.shape[0]):
        for column in range(zoomed_out_image.shape[1]):
            zoomed_out_image[row][column] = image[row*2][column*2]

    # showing output image
    return zoomed_out_image
###################################################
###################################################


def show(image, x, y, size):
    height = min(y+size//2, image.shape[0])-max(0, y-size//2)
    width = min(x + size//2, image.shape[1]) - max(0, x - size//2)
    output_image = 255 * np.ones((height, width), np.uint8)
    xcordi = 0
    ycordi = 0
    for i in range(max(0, y-size//2), min(y+size//2, image.shape[0])):
        xcordi = 0
        for j in range(max(0, x - size//2), min(x + size//2, image.shape[1])):
            output_image[ycordi][xcordi] = image[i][j]
            xcordi = xcordi+1
        ycordi = ycordi+1
    cv2.namedWindow('image2')
    cv2.imshow('image2', output_image)
    cv2.waitKey(0) & 0xFF


####################################################
###################################################


def zoom_out_interpolation(image):
    height = image.shape[0]
    width = image.shape[1]
    # declaring a blank image
    zoomed_out_image = 255 * np.ones((height//2, width//2), np.uint8)
    # taking average of four neighbours of alternate pixels and saving them to output image
    for row in range(zoomed_out_image.shape[0]-zoomed_out_image.shape[0] % 4):
        for column in range(zoomed_out_image.shape[1]-zoomed_out_image.shape[1] % 4):
            zoomed_out_image[row][column] = image[row*2][column*2]//4+image[row*2 +
                                                                            1][column*2]//4+image[row*2][column*2+1]//4+image[row*2+1][column*2+1]//4

    # showing output image
    return zoomed_out_image

###################################################
###################################################
# code for zooming in pixels


def zoom_in_replication(image):
    height = image.shape[0]
    width = image.shape[1]
    # declaring a blank image
    zoomed_in_image = 255 * np.ones((height * 2, width*2), np.uint8)
    row = 0
    # taking values from original image and placing alternatively in output image
    while row < 2*height:
        column = 0
        while column < 2*width:
            zoomed_in_image[row][column] = image[row//2][column//2]
            column = column+2
        row = row+2

    row = 0
    # replicating pixels row wise
    while row < 2 * height:
        column = 1
        while column < 2 * width:
            zoomed_in_image[row][column] = zoomed_in_image[row][column-1]
            column = column + 2
        row = row + 2

    row = 1
    # replicating pixels column wise
    while row < 2 * height:
        column = 0
        while column < 2 * width:
            zoomed_in_image[row][column] = zoomed_in_image[row-1][column]
            column = column + 1
        row = row + 2

    return zoomed_in_image
###################################################
###################################################


def zoom_in_interpolation(image):
    height = image.shape[0]
    width = image.shape[1]
    # declaring a blank image
    zoomed_in_image = 255 * np.ones((height * 2, width*2), np.uint8)
    row = 0
    # taking values from original image and placing alternatively in output image
    while row < 2*height:
        column = 0
        while column < 2*width:
            zoomed_in_image[row][column] = image[row//2][column//2]
            column = column+2
        row = row+2

    row = 0
    # averaging pixels row wise
    while row < 2 * height-2:
        column = 1
        while column < 2 * width-2:
            zoomed_in_image[row][column] = (
                zoomed_in_image[row][column-1]//2 + zoomed_in_image[row][column+1]//2)
            column = column + 2
        row = row + 2

    row = 1
    # averaging pixels column wise
    while row < 2 * height-2:
        column = 0
        while column < 2 * width-2:
            zoomed_in_image[row][column] = (
                zoomed_in_image[row-1][column]//2+zoomed_in_image[row+1][column]//2)
            column = column + 1
        row = row + 2

    return zoomed_in_image

###################################################
###################################################
###################################################


# code for taking image as input
def input_image():
    while (True):
        url_input1 = input(
            "Enter URL/address/path Of original image with extention of image in format shown\nExample:-'/home/user/image.png'\n")
        original_image = cv2.imread(url_input1, 0)
        if trycatch(original_image):
            print("not a valid address\n")
            continue
        else:
            return original_image

###################################################
###################################################
###################################################
###################################################


# taking image as input
original_image = input_image()
print("Click on region of intrest and press any key for functions")
# selecting region of intrest
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_handler)


cv2.imshow('image', original_image)
k = cv2.waitKey(0)
cv2.destroyAllWindows()
print("zoom out image using press '1' for interpolation and '2' for replication")
option2 = int(input())
if option2 == 1:
    image = zoom_out_interpolation(original_image)
elif option2 == 2:
    image = zoom_out_replication(original_image)
else:
    print("Wrong option selected")

print("zoom in image using press '1' for interpolation and '2' for replication")
option2 = int(input())
if option2 == 1:
    image = zoom_in_interpolation(image)
elif option2 == 2:
    image = zoom_in_replication(image)
else:
    print("Wrong option selected")

print("Enter size of output frame ")
x = int(input())


show(image, mouseX, mouseY, x)
