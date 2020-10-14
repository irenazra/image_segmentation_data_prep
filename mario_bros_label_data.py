#A simple python program that identifies UI elements in Super Mario Bros NES (1985)
#UI elements that are text are labelled with white.
#The gold icon at the top of the screen is a different type of UI element (not text), so
#it is labelled with magenta
#Author: Iren Azra Coskun 
import os
import cv2 
from matplotlib import pyplot
import numpy as np
import glob, os

def identify_ui (file_name):
    
    #load the image
    myimage = cv2.imread(file_name)
    
    #convert the BGR image to RGB
    rgbimage = cv2.cvtColor(myimage,cv2.COLOR_BGR2RGB )

    #height and width of the image
    h = rgbimage.shape[0]
    w = rgbimage.shape[1]

    #initially set to false
    gold_present = False

    #go through each pixel in the image
    for row in range(0,h) : 
        for col in range(0,w) :
            #if the pixel is white, label it white 
            if (rgbimage[row,col,0] == 255  and rgbimage[row,col,1] == 255 and rgbimage[row,col,2] == 255) :
                    #if there are white pixels in this area, the gold icon is present 
                    #this makes sure that we are indeed looking at a game screen shot
                    #that contains these UI elements. Let's us avoid mislabelling loading screens etc. 
                    
                    if (row > 15 and row < 25 and col > 70 and col < 130):
                        gold_present = True
                    rgbimage[row,col] = 255

            #label the pixel black
            else:
                rgbimage[row,col] = 0

            #Avoid accidentally labelling white things like clouds
            if (row > 23):
                rgbimage[row,col] = 0
     
    #if the gold icon is present in the image, label those pixels with magenta
    if (gold_present): 
        for row in range(16,24) : 
            for col in range(89,94) :
                rgbimage[row,col,0] = 255
                rgbimage[row,col,1] = 0
                rgbimage[row,col,2] = 255
            

    #reload the image 
    image_gray = cv2.cvtColor(myimage, cv2.COLOR_BGR2GRAY)
    
    
    #Getting the template (an example of how score is printed on the screen when an enemy is killed)
    template_image= cv2.imread("images/template.png")
    template_image_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

    #cut the area where "100" points is displayed
    template = template_image_gray[143:153,108:121]

    #shape of template
    template_height = template.shape[0]
    template_width = template.shape[1]
    
    #perform template matching, returns a numpy array
    match_result = cv2.matchTemplate(image_gray,template,cv2.TM_CCOEFF_NORMED)
    

    #returns all the values that are greater than 0.7
    #0.7 is selected as threshold to allow for other points such as "200" to be recognized
    activated = np.where( match_result >= 0.7)

    rectangle_color = (255,255,255)
    result = rgbimage

    #around each area that was identified through template matching, draw a rectangle
    for point in zip(*activated[::-1]):
        result = cv2.rectangle(rgbimage, point, (point[0] + template_width, point[1] + template_height), rectangle_color, -1)

    pyplot.imshow(result)
    pyplot.show()

   
if __name__ == "__main__":
    
    for fileName in glob.glob("images/*.png"):
        identify_ui(fileName)