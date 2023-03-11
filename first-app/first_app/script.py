import cv2
import numpy as np
import skimage.exposure
import matplotlib.pyplot as plt
import math
'''
This function detects the black circles, and draws the interior rectangles of each experimental condition. 
Returns a list of coordinates of the rectangles
'''
def draw(img):
    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # blur
    blur = cv2.GaussianBlur(gray, (0,0), sigmaX=99, sigmaY=99)
    # do division normalization
    normal = cv2.divide(gray, blur, scale=255)
    # stretch to full dynamic range
    stretch = skimage.exposure.rescale_intensity(normal, in_range='image', out_range=(0,255)).astype(np.uint8)
    # adaptive threshold - decrease C constant - original 6 (last command)
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 25, 6)
    # apply morphology close (need better way to close structure) increase morphology close size - original 11, 11
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (6,6))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # get external contours
    contours = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    # draw contour on copy of image and also draw ellipse
    result1 = img.copy()
    result2 = img.copy()
    i = 1
    count = 0
    total_coords = []
    for cntr in contours:
        area = cv2.contourArea(cntr)
        if area > 5000:
            ellipse = cv2.fitEllipse(cntr)
            (xc,yc),(d1,d2),angle = ellipse
            cv2.drawContours(result1, [cntr], 0, (0,0,255), 1)
            #cv2.ellipse(result2, (int(xc),int(yc)), (int(d1/2),int(d2/2)), angle, 0, 360, (0,0,255), 1)
            radius_frac = 0.18
            radius = int(d2 * radius_frac)
            # get rectangle
            x1, y1 = int(xc) - radius, int(yc) - radius
            x2, y2 = int(xc) + radius, int(yc) + radius
            cv2.rectangle(result2, (x1, y1), (x2, y2), (255, 0, 0), 2)
            ind_coords = (x1, y1, x2, y2)
            total_coords.append(ind_coords)
            i += 1
            count += 1

    return total_coords

'''
This function takes in the list from draw function and crops out the rectangles. 
Returns the pics list.
'''
def process_rects(img, coord_list):
    # Makes sure the images are displayed in chronological order: NC, PC, NT, T, NG
    coord_list = sorted(coord_list, key=lambda c: c[0])
    pics = []
    for coord in coord_list:
        cropped = img[coord[1]:coord[3], coord[0]:coord[2]]
        pics.append(cropped)
    return pics

'''
This function takes in the pics list generated from cropping out the rectangles and 
conducts rgb analysis on each of the image. 
Output is the corresponding rgb values from the 5 images 
'''
def rgb_analysis(images):
    total_rgb = []
    for i, img in enumerate(images):
        ind_rgb = []
        # Split the image into its Red, Green, and Blue channels
        b, g, r = cv2.split(img)
        # Calculate the mean or median RGB values for each channel and add to list
        r_mean = np.mean(r)
        ind_rgb.append(r_mean)
        g_mean = np.mean(g)
        ind_rgb.append(g_mean)
        b_mean = np.mean(b)
        ind_rgb.append(b_mean)
        total_rgb.append(ind_rgb)
        print(f"Image {i + 1} RGB values: R={r_mean}, G={g_mean}, B={b_mean}")
    return total_rgb

'''
This function takes in the raw rgb values and computes the relative expression levels. 
Output is a list with the 5 relative expression values 
'''
def relative_expression(conditions):
    r_nc = conditions[0][0]
    g_nc = conditions[0][1]
    y_nc = conditions[0][2]
    for condition in conditions:
        condition[0] -= r_nc
        condition[1] -= g_nc
        condition[2] -= y_nc
    # dimensional reduction
    reductions = []
    r_pc = conditions[1][0]
    g_pc = conditions[1][1]
    y_pc = conditions[1][2]
    denom = math.sqrt(r_pc ** 2 + g_pc ** 2 + y_pc ** 2)
    for new in conditions:
        reductions.append((new[0] * r_pc + new[1] * g_pc + new[2] * y_pc) / denom)
    express_vals = []
    pc_val = reductions[1]
    for reduction in reductions:
        express_vals.append(reduction / pc_val)

    return express_vals

def main(image) -> list:
    img = cv2.imread(image[1:])

    rect_cord_list = draw(img)
    images = process_rects(img, rect_cord_list)
    values = rgb_analysis(images)
    return relative_expression(values)

if __name__ == "__main__":
    main()
