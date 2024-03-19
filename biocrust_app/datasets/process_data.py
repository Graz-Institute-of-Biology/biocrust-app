import json
import requests
from PIL import Image
from io import BytesIO
from collections import defaultdict
import  numpy as np
import os


"""
This file contains the helper functions for the datasets app.
"""

# Mask_ModelViewSet

def load_image(parent_image_url):
    response = requests.get(parent_image_url)
    img = Image.open(BytesIO(response.content))

    return img

def generate_class_dist(image):
    pixels = image.load()
    class_counts = defaultdict(int)
    class_colors = {}
    with open('./biocrust_app/datasets/ontology.json', 'r') as file:
        color_config = json.load(file)

    pixel_to_label = {tuple(value['color']): value['name'] for value in color_config.values()}

    for class_label in color_config:
        class_counts[color_config[class_label]['name']] = 0
    print('Class Counts: ', class_counts)
    if len(image.size) == 3:
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                pixel_value = pixels[i, j]
                class_label = pixel_to_label.get(pixel_value)
                if class_label:
                    class_counts[class_label] += 1
    if len(image.size) == 2:
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                #print(color_config)
                #print(pixels[i, j])
                class_label = color_config[str(pixels[i, j])]['name']
                #print(class_label)
                class_counts[class_label] += 1

    total_pixels = sum(class_counts.values())
    class_distribution = {key: round(value / total_pixels, 3) for key, value in class_counts.items()}
    
    class_colors = {value['name']: str(value['color']) for value in color_config.values()}
    
    return json.dumps({"class_distributions": class_distribution, "class_colors": class_colors})

def get_ontology():
        ontology_path = './biocrust_app/datasets/ontology.json'
        with open(ontology_path, 'r') as f:
            ontology = json.load(f)
        return ontology

def get_color(category):
    ontology = get_ontology()
    return ontology.get(str(category), {}).get('color', [0, 0, 0])  

def translate_categorical_to_color(input_image):
    pixels = input_image.load()
    if len(input_image.size) == 2:
        print('Translating categorical to color')
        colored_image = np.zeros((input_image.size[1], input_image.size[0], 3), dtype=np.uint8) 
        ontology_path = './biocrust_app/datasets/ontology.json'
        with open(ontology_path, 'r') as f:
            ontology = json.load(f)
        
        for i in range(input_image.size[0]):
            for j in range(input_image.size[1]):
                color = ontology.get(str(pixels[i, j]), {}).get('color', [0, 0, 0])
                colored_image[j, i, :] = color
        return input_image, colored_image
    else:
        return input_image, pixels

