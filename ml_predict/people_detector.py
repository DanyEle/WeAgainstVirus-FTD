#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 16:57:11 2020

@author: daniele
"""

import requests
import cv2
from sightengine.client import SightengineClient
import argparse


#Input: -image_path(str): a string containing the path to the image whose crowd is to be analyzed
def perform_prediction(image_path):
    url = 'https://app.nanonets.com/api/v2/ObjectDetection/Model/5305efe3-f03e-4e79-b4d9-b6bebb78ebc9/LabelFile/'
    
    data = {'file': open(image_path, 'rb')}
    response = requests.post(url, auth=requests.auth.HTTPBasicAuth('5kZQ1enyezAt0BeHuYkGlx1XP5WYvyFY', ''), files=data)
    return(response.json())

def extract_number_people_response(response_json):
    number_people = len(response_json["result"][0]["prediction"])
    return(number_people)

def draw_bounding_box(source_image, destination_image, response_json):
    
    rectangles_list = response_json["result"][0]["prediction"]
    
    image = cv2.imread(source_image)

    for rectangle in rectangles_list:
        cv2.rectangle(image,(rectangle["xmin"],rectangle["ymin"]),(rectangle["xmax"],rectangle["ymax"]),(255,0,0),5) # add rectangle to image
        
    cv2.imwrite(destination_image,image)
    
def parse_args():
    parser = argparse.ArgumentParser(
        description='Process the input image and draw a bounding box around it, creating an output image.')
    parser.add_argument('--image_input', required=True,
                        metavar='./path/to/input_image.jpg',
                        help='Path to a folder that contains the image where the people should be detected. '
                             'Images can be arbitrarily nested in subfolders and will still be found.')
    parser.add_argument('--image_output', required=True,
                        metavar='/path/to/output_image.jpg',
                        help='Path to a folder that will contain the image with the bounding box placed on detected people'
                             'Will mirror the folder structure of the input folder.')
    
    args = parser.parse_args()

    print(f'image_input: {args.image_input}')
    print(f'image_output: {args.image_output}')

    return (args)


if __name__ == '__main__':
    args = parse_args()
    
    print("Parsing image with the detector...")

    #Detect people in the image passed as input
    response_json = perform_prediction(args.image_input)
    number_people = extract_number_people_response(response_json)
    print("There are " + str(number_people) + " people in this picture")
    draw_bounding_box(args.image_input, args.image_output, response_json)


