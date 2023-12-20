import cv2
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import numpy as np
import torch as t
from torchvision import transforms
import segmentation_models_pytorch as smp
from myutils import logits2rgb
from utils_whole import import_data_whole
import skimage.transform as skt
import matplotlib.pyplot as plt

def convert_data(image):
    image = (image - np.min(image)) / np.ptp(image)
    image = skt.resize(image, (512, 512, 3), order=0)
    convert_tensor = transforms.ToTensor()   
    image = convert_tensor(image)

    return image
    
def predict(image, model, device):
    image = t.unsqueeze(image, dim=0).float()[0,:,:,:]
    if t.cuda.is_available():
        image = image.to(device="cuda")
    logits = model(image)
    logits_max = logits.max(1)[1].float().cpu().numpy()
    
    image = image.float().cpu().numpy()[0][:,:,:]
    image = np.moveaxis(image, 0, -1)
    classes = logits_max[0,:,:]
    classes_color = logits2rgb(logits_max[0,:,:])

    return classes, image, classes_color


def process_whole(image, model, device):
    # Initialize a dictionary to count categorical values
    category_counts = {}

    tensor = convert_data(image)
    classes, _, classes_color = predict(tensor, model, device)    

    #_ , axarr = plt.subplots(1,2)
    #image = np.moveaxis(image, 0, -1)
    #axarr[0].imshow(classes_color)
    #axarr[1].imshow(image)
    #plt.show()
    #cv2.imshow('labels', labels.astype(np.uint8))
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    #cv2.imshow('image', image.astype(np.uint8))
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    unique_values, counts = np.unique(classes, return_counts=True)


    # Update the category counts
    for value, count in zip(unique_values, counts):
        if value not in category_counts:
            category_counts[value] = count
        else:
            category_counts[value] += count

    # Print the counts for each categorical value
    for category, count in category_counts.items():
        print(f"Category {category}: {count} pixels")
    print('Sum: ')
    print(sum(category_counts.values()))

    # Initialize a dictionary to count categorical values for the whole image
    category_counts_whole = {}

    flat_grid = classes.reshape(-1)

    # Count the occurrences of each categorical value in the whole image to compare with the previous method
    unique_values, counts = np.unique(flat_grid, return_counts=True)

    # Update the category counts
    for value, count in zip(unique_values, counts):
        if value not in category_counts_whole:
            category_counts_whole[value] = count
        else:
            category_counts_whole[value] += count

    for category, count in category_counts_whole.items():
        print(f"Whole Image Category {category}: {count} pixels")
    print('Sum: ')
    print(sum(category_counts_whole.values()))

    return image, classes, classes_color

def get_model(device,num_classes, path):
    unet = smp.Unet('mit_b5', classes=num_classes, activation=None, encoder_weights='imagenet')
    print("Loading model")
    unet.load_state_dict(t.load(path))
    unet.eval()
    #unet = unet.to(device)
    if t.cuda.is_available():
        print('gpu detected')
        unet.cuda() 

    return unet

image_path = './raw_data/DF01.JPG'
image = cv2.imread(image_path)

grid_size = 512
num_classes = 7
device = t.device('cuda' if t.cuda.is_available() else 'cpu')

model_path = './models/best_validation_whole_ckpt.pt'
model = get_model(device, num_classes, model_path)

image, classes, classes_color = process_whole(image, model, device)
