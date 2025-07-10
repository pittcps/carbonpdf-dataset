# 
# Dell Device Carbon Emission Parser
# Modify imports as needed. I used a lot of imports during testing so feel free to remove or modify any here

import PyPDF2 as pdf
from numpy import NaN
import tabula as tab
from pathlib import Path
import pandas as pd
import os
import glob
import fitz
import cv2
import pytesseract as tess
import numpy as np
from sklearn.cluster import KMeans


# This is one of the parsers used for Carbon information collection for Dell Devices. The device carbon files come in many formats, so this is simply one of those formats it works best with
# It can be adjusted to work with most formats, but naming conventions would need to be changed and order of information varies across files.
#
# This parser in particular takes all of the carbon files and extracts the pie chart images from the file. It then grabs as much of the information it can from those pie charts to 
# compile the data. This works decently for most files, but the pie chart order varies heavily across files and the placement of the information. As such, this file acts as a good
# building point to work off of since it has the basic rundown of things but only works on some of the files 100%

def get_carbon_data():
    # Create initial DataFrame with column names. These names work for some of the dataset but other files have different naming conventions
    df = pd.DataFrame(columns=["Model","Chassis & Assembly","Hard Drive","Power Supply","Battery","Mainboard and other boards","Display","Packaging"])

    # Starts a search for all of the .pdf files in a file location
    pdf_search = Path("Dell_Laptop_Carbon/")


    # runs through all of the pdf files individually
    for x in pdf_search.glob("*.pdf"):
            pdf = fitz.open(x)
            page = pdf[0]

            # gets list of images within the file
            image_list = page.get_images(full=True)
            for image_index, img in enumerate(image_list):

                # for every file I personally tested this result gave the pie chart image. Modify this in the case of varying image placement within the document.
                xref = img[0]
                pix = fitz.Pixmap(pdf, xref)
                if pix.n < 5:
                    # Saves pie chart image as its own file, can modify if desired. 
                    pix.save(pdf.name.removesuffix(".pdf") + ".png",'png')
                pix = None
                try:

                    # Starts the image processing. Reads the image using CV2 and creates cropped versions of the legend and pie chart as well as a greyscale version of them. 
                    # Greyscale works best for thresholding in the next step of the process.
                    image_path = pdf.name.removesuffix(".pdf") + ".png"
                    image = cv2.imread(image_path)
                    cropped_legend = image[int(image.shape[0] - 120):int(image.shape[0]),int(image.shape[1] / 2 - 400):int(image.shape[1] / 2 + 400)]
                    cropped_pie = image[int(30):int(image.shape[0] - 120),int(image.shape[1] / 2 + 200):int(image.shape[1])]
                    gray_pie = cv2.cvtColor(cropped_pie, cv2.COLOR_BGR2GRAY)
                    gray_legend = cv2.cvtColor(cropped_legend, cv2.COLOR_BGR2GRAY)


                    # Sets up pytesseract. modify this line if you have pytesseract in a different file location or using something like a vim.
                    tess.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

                    # Starts the thresholding process. The specific values below is just what gave me the best results from my testing
                    # Feel free to modify as fit for the cases where it does not accurately get the information
                    _, thresholded_img = cv2.threshold(gray_pie, 41, 255, cv2.THRESH_BINARY)
                    _, thresholded_legend = cv2.threshold(gray_legend, 50, 255, cv2.THRESH_BINARY_INV)

                    # Splits the pie chart in 2. This allows for a more streamlined process with comparing it to the legend. 
                    # In this case, the information for the pie chart of this variance of the document is clockwise ending on packaging
                    # Because of this, I get the information into each respective half and then take the packaging value and place it at the end.
                    pie_left = thresholded_img[int(0):int(thresholded_img.shape[0]),int(0):int(thresholded_img.shape[1] / 2.7)]
                    pie_right = thresholded_img[int(0):int(thresholded_img.shape[0]),int(thresholded_img.shape[1] / 2.7):int(thresholded_img.shape[1])]

                    # Basic pytesseract usage to extract the text. print if results are inconsistent
                    left_text: str = tess.image_to_string(pie_left,config='--psm 11')
                    right_text: str = tess.image_to_string(pie_right,config='--psm 11')
                    legend_text: str = tess.image_to_string(thresholded_legend,config='--psm 11')

                    # This is a basic filter to double check that the % sign is present within the pytesseract words. 
                    # This is useful for if it tries to see a line somewhere as a character and attempt to add it to the data
                    # Adjust if you use any files that dont have percentage signs next to the data (all the ones I tested did)
                    left_new = ""
                    right_new = ""
                    for word in left_text.split():
                        if word.find("%") != -1:
                            left_new += word + "\n"
                    for word in right_text.split():
                        if word.find("%") != -1:
                            right_new += word + "\n"
                    
                    # Splits up the pytesseract output and turns it into a list
                    # This is where I remove the packaging percentage and add it to the end
                    # 
                    # Up to this point most files should be able to get here with maybe the occasional need to modify crop placement or adjust thresholding
                    # After this point is where the specific variance of this file comes into play
                    # So stuff after this point is where would need the most modifications for different types
                    # The main issue is linking up the values, not getting the values themselves usually
                    # Some files do have a harder time being read though.
                    left_split: list = left_new.split("\n")
                    left_split.remove('')
                    right_split: list = right_new.split("\n")
                    right_split.remove('')
                    if len(left_split) > 0:
                        end = left_split[-1]
                        left_split.remove(end)
                    left_split.reverse()
                    in_order = []
                    for word in left_split:
                        in_order.append(word)
                    for word in right_split:
                        in_order.append(word)
                    in_order.append(end)

                    # Same process as before but this time with the legend text
                    legend_labels = legend_text.split("\n")

                    for word in legend_labels[:]:
                        if not df.columns.__contains__(word):
                            legend_labels.remove(word)

                    # This part starts adding the information to the dataframe
                    # Adjust this part as needed
                    # Currently it uses the names in the legend as column names and matches it with the percentage data
                    # This part will give you most information but in the wrong spots if the format is wrong
                    if len(in_order) == len(legend_labels):
                        final = {}

                        for i in range(len(legend_labels)):
                            final[legend_labels[i]] = in_order[i]

                        df.loc[-1] = final
                        df["Model"].loc[-1] = x.name

                        df = df.reset_index(drop=True)

                        # This part makes the relevant images show up on screen so you can verify results.
                        # Press enter to move on to next image
                        # Comment this out if you have finished testing and just want to run the program
                        cv2.imshow("image", gray_pie)
                        cv2.waitKey(0)
                        cv2.imshow("image",pie_left)

                        cv2.waitKey(0)
                        cv2.destroyAllWindows()


                # The above gets most of the values for the files I started the testing with. It does not work on all files, so some manual work needed to get done.
                # Usually the main issues you will run into with this are:
                    # Data being right in the middle of the cutoff. Can be fixed by adjusting the placement of the cut and threshold values
                    # Thresholding still not making text clear enough. Can be fixed by adjusting that on an individual level, or potentially trying a new
                        # Strategy. This is just the method I used as I found it simple and quick to use. 
                    # The Dell dataset is made up of multiple formats of pie chart. The data collection itself is usually easy, but linking it up
                        # with the desired legend tags is the issue. I counted about 5 different formats within the dataset I was working with, so
                        # with some modifications this should work with all 5, the main difference being just changing how the code links the legend
                        # text with the specific pie chart configuration.
                except:
                    pass
    print(df)


if __name__=="__main__":
    get_carbon_data()
    pass