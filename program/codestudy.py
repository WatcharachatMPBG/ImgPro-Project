import numpy as np
import argparse
import cv2

def image_deskew(image):
    # convert the image to grayscale and flip the foreground
    # and background to ensure foreground is now "white" and
    # the background is "black"
    #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(image)
    # threshold the image, setting all foreground pixels to
    # 255 and all background pixels to 0
    thresh = cv2.threshold(gray, 0, 255,
        cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # grab the (x, y) coordinates of all pixel values that
    # are greater than zero, then use these coordinates to
    # compute a rotated bounding box that contains all
    # coordinates
    coords = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coords)[-1]
    # the `cv2.minAreaRect` function returns values in the
    # range [-90, 0); as the rectangle rotates clockwise the
    # returned angle trends to 0 -- in this special case we
    # need to add 90 degrees to the angle
    if angle < -45:
        angle = -(90 + angle)
    # otherwise, just take the inverse of the angle to make
    # it positive
    else:
        angle = -angle
    # rotate the image to deskew it
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h),
        flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    '''
    # draw the correction angle on the image so we can validate it
    cv2.putText(rotated, "Angle: {:.2f} degrees".format(angle),
        (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    '''
    # show the output image
    print("[INFO] angle: {:.3f}".format(angle))
    return rotated

def color_cut(img):
    kernel = np.ones((2,2),np.uint8)
    # Convert BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # define range of black color in HSV
    lower_val = np.array([0,0,0])
    upper_val = np.array([179,100,130])

    # Threshold the HSV image to get only black colors
    mask = cv2.inRange(hsv, lower_val, upper_val)

    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(img,img, mask= mask)
    # invert the mask to get black letters on white background
    res2 = cv2.bitwise_not(mask)
    '''
    # display image
    cv2.imshow("img", res)
    cv2.imshow("img2", res2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    return res2

def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
        help="path to input image file")
    args = vars(ap.parse_args())
    # load the image from disk
    image = cv2.imread(args["image"])
    image = cv2.resize(image, (1240,1754), interpolation = cv2.INTER_AREA)
    colorgut = color_cut(image)
    rotated = image_deskew(colorgut)
    cv2.imshow("Input", image)
    cv2.imshow("Rotated", rotated)
    cv2.imshow("cut", colorgut)
    cv2.waitKey(0)

if __name__ == "__main__":
    main()