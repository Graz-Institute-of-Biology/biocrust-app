#!/usr/bin/python3
# -*- coding: utf-8 -*-

# import torch
# from config import CONFIG
import numpy as np


def preprocess(package: dict, input: list) -> list:
    """
    Preprocess data before running with model, for example scaling and doing one hot encoding
    :param package: dict from fastapi state including model and preocessing objects
    :param package: list of input to be proprocessed
    :return: list of proprocessed input
    """

    # scale the data based with scaler fit during training
    scaler = package['scaler']
    input = scaler.transform(input)

    return input


def predict(package: dict, input: list) -> np.ndarray:
    """
    """
    y_pred = "Prediction_Mask"
    print("predicting...")
    print(y_pred)
    return {"mask" : y_pred}