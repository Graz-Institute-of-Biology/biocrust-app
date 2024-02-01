#!/usr/bin/python3
# -*- coding: utf-8 -*-

import torch
import segmentation_models_pytorch as smp
import requests
from io import BytesIO

# from config import CONFIG
import numpy as np


def preprocess(package: dict, input: list) -> list:
    """
    Preprocess data before running with model, for example scaling and doing one hot encoding
    :param package: dict from fastapi state including model and preocessing objects
    :param input: list of input to be proprocessed
    :return: list of proprocessed input
    """

    # scale the data based with scaler fit during training
    scaler = package['scaler']
    input = scaler.transform(input)

    return input

def prepare_load_model(model_path):
    encoder = 'mit_b5'
    encoder_weights = 'imagenet'
    activation = 'sigmoid'
    class_values = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    model = smp.Unet(
        encoder_name=encoder, 
        encoder_weights=encoder_weights, 
        classes=len(class_values), 
        activation=activation,
    )

    response = requests.get(model_path)
    # print(response.content)
    checkpoint = torch.load(BytesIO(response.content), map_location=torch.device('cpu'))
    model.load_state_dict(checkpoint['model_state_dict'])

    return model

def predict(package: dict, input: list) -> np.ndarray:
    """
    """
    print(package)
    model_path = package['model_path']
    image_path = package['file_path']
    print("preparing model...")
    model = prepare_load_model(model_path)
    print("model prepared")
    print("loading model...")
    # optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
    # model = torch.load()
    print("state dict loaded")
    print("predicting...")
    print(image_path)
    return {"mask" : "Pred_Mask"}