import re
import os 
import cv2
import pytesseract
import numpy as np
from PIL import Image
from transformers import pipeline
from pdf2image import convert_from_path
from utils import *


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
images = convert_from_path('resume.pdf', poppler_path = r"C:\Users\shakhansho.sabzaliev\Downloads\Release-22.01.0-0\poppler-22.01.0\Library\bin")
ner = pipeline("ner", aggregation_strategy="simple")
pdf = []

for image in images:
    data = pytesseract.image_to_data(image, output_type='dict')

    text = '' 
    for i in data['text']:
        if i == '':
            pass
        else:
            text += i.strip() + ' '

    bert = ner(text)

    bbox, matches = [], []

    find_emails(text, matches)
    find_numbers(text, matches)
    find_months(text, matches)

    # Find names, organizations' names, locations & addresses
    for obj in bert:
        group = obj['entity_group']
        word = obj['word']

        if (group in ['PER', 'ORG', 'LOC']) and (len(word.strip('#')) > 3):
            temp = word.strip('#').split(' ')

            for w in temp:
                if len(w) > 2:
                    matches.append(w)

    find_coordinates_pytesseract(matches, data, bbox)
    draw_black_box_pytesseract(bbox, image)

    pdf.append(image)


img1 = pdf.pop(0)
img1.save('D:\\Git Repos\\open-data-anonymizer\\anonympy\\pdf\\temp_out.pdf', save_all=True, append_images=pdf)
alter_metadata('temp_out.pdf', 'resume_out.pdf')
# os.remove('temp_out.pdf')


# pytesseract.pytesseract.tesseract_cmd =  self.pytesseract_path
# images = convert_from_path(filename, poppler_path = self.poppler_path)
# ner = pipeline("ner", aggregation_strategy="simple")
# pdf = []

# for image in images:
#     data = pytesseract.image_to_data(image, output_type='dict')

#     text = '' 
#     for i in data['text']:
#         if i == '':
#             pass
#         else:
#             text += i.strip() + ' '

#     bert = ner(text)

#     bbox, matches = [], []

#     find_emails(text, matches)
#     find_numbers(text, matches)
#     find_months(text, matches)

#     # Find names, organizations' names, locations & addresses
#     for obj in bert:
#         group = obj['entity_group']
#         word = obj['word']

#         if (group in ['PER', 'ORG', 'LOC']) and (len(word.strip('#')) > 3):
#             temp = word.strip('#').split(' ')

#             for w in temp:
#                 if len(w) > 2:
#                     matches.append(w)

#     find_coordinates_pytesseract(matches, data, bbox)
#     draw_black_box_pytesseract(bbox, image)

#     pdf.append(image)


# img1 = pdf.pop(0)
# img1.save('D:\\Git Repos\\open-data-anonymizer\\anonympy\\pdf\\temp_out.pdf', save_all=True, append_images=pdf)
# alter_metadata('temp_out.pdf', 'resume_out.pdf')
# os.remove('temp_out.pdf')


# # pytesseract.pytesseract.tesseract_cmd =  r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# # images = convert_from_path('resume.pdf', poppler_path = r"C:\Users\shakhansho.sabzaliev\Downloads\Release-22.01.0-0\poppler-22.01.0\Library\bin")