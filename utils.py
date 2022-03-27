# -*- coding: utf-8 -*-
import pdfplumber
from PIL import Image
import pytesseract
import cv2 as cv
import fitz
import numpy as np
import os


def extract_pdf_single_column(pdf_name, pdf_path):
    with pdfplumber.open(pdf_path + pdf_name + ".pdf") as pdf:
        text_opts = []
        for page in pdf.pages:
            page_text = page.extract_text()
            text_opts.append(page_text)
        text = ''.join(text_opts)
        text = ''.join(text.split())
        # index = text.find("参考文献")
        # text = text[0:index]
        return text


def extract_pdf_two_columns(pdf_name, pdf_path, image_path, zoom_x, zoom_y, rotation_angle):
    pdf = fitz.open(pdf_path + pdf_name + ".pdf")
    text_opts = []
    for pg in range(0, pdf.page_count):
        page = pdf[pg]
        trans = fitz.Matrix(zoom_x, zoom_y).prerotate(rotation_angle)
        pm = page.get_pixmap(matrix=trans, alpha=False)
        save_path = image_path + pdf_name + '_' + str(pg) + ".png"
        pm.save(save_path)
        img = cv.imdecode(np.fromfile(save_path, dtype=np.uint8), -1)
        page_text = pytesseract.image_to_string(Image.fromarray(img), lang="chi_sim")
        text_opts.append(page_text)
    pdf.close()
    text = ''.join(text_opts)
    text = ''.join(text.split())
    # index = text.find("参考文献")
    # text = text[0:index]
    save_text(text+'\n')
    return text


def get_all_filename(path="./paper"):
    filenames = os.listdir(path)
    filename_list = []
    for filename in filenames:
        index = filename.index(".pdf")
        if index == -1:
            continue
        else:
            filename_list.append(filename[:index])
    return filename_list


def save_text(content, file_path="./result/result.txt"):
    with open(file_path, 'a', encoding="utf-8") as f:
        f.write(content)
