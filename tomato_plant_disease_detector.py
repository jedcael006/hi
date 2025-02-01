# -*- coding: utf-8 -*-
"""Tomato_plant_disease_detector.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/16Jv-mYSv_x4_liUBkffBD1GnrVipdVyX

<a href="https://colab.research.google.com/github/sudhir2016/Google-Colab-11/blob/master/Tomato_plant_disease_detector.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

Load Python, TensorFlow and Keras libraries.
"""

import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing.image import load_img
import cv2
import glob
import os
import shutil
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Input
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.layers import GlobalAveragePooling2D
from tensorflow.keras.models import load_model
from sklearn.metrics import confusion_matrix, precision_score

"""Load Plant Village Dataset."""

!git clone https://github.com/spMohanty/PlantVillage-Dataset

"""Create empty lists for tomato leaf images (X) and labels(Y) for testing."""

X=[]
Y=[]

"""Create and sort list of label names."""

label=[]

for i in range (10):
  label.append(1)

label[0]='Tomato___healthy'
label[1]='Tomato___Tomato_mosaic_virus'
label[2]='Tomato___Tomato_Yellow_Leaf_Curl_Virus'
label[3]='Tomato___Target_Spot'
label[4]='Tomato___Spider_mites Two-spotted_spider_mite'
label[5]='Tomato___Septoria_leaf_spot'
label[6]='Tomato___Leaf_Mold'
label[7]='Tomato___Late_blight'
label[8]='Tomato___Early_blight'
label[9]='Tomato___Bacterial_spot'

label.sort()

print(label)

"""Path for Tomato dataset."""

# Define the source directory and the new directory
source_dir = 'PlantVillage-Dataset/raw/color'
new_dir = 'PlantVillage-Dataset/raw/color/Tomato'

# Create the new directory if it doesn't exist
os.makedirs(new_dir, exist_ok=True)

# Define the files to move
files_to_move = ['Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']

# Loop through the files and move them to the new directory
for file in files_to_move:
    source_path = os.path.join(source_dir, file)
    destination_path = os.path.join(new_dir, file)

    # Use shutil.move to move the files
    try:
        shutil.move(source_path, destination_path)
        print(f"Moved '{file}' to '{destination_path}'")
    except FileNotFoundError:
        print(f"Error: '{source_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

a='/content/PlantVillage-Dataset/raw/color/Tomato'
c='*.*'

"""Load and preprocess small set of 50 images, 5 of each category for test dataset."""

for i in range (10):
  b=label[i]
  path=os.path.join(a,b,c)
  image1= [cv2.imread(file) for file in glob.glob(path)]
  for j in range (5):
    image2 = cv2.resize(image1[j], dsize=(224, 224), interpolation=cv2.INTER_CUBIC)
    X.append(image2)
    out=i
    Y.append(out)

len(X)

X=np.array(X)/255.0

Y=np.array(Y)

"""Set up dataset generator as flow from directory."""

train_datagen=ImageDataGenerator(rescale=1./255, rotation_range=45,
                    width_shift_range=.15, height_shift_range=.15,
                    horizontal_flip=True,  zoom_range=0.5)

train_generator=train_datagen.flow_from_directory('/content/PlantVillage-Dataset/raw/color/Tomato',target_size=(224, 224),
        batch_size=32,
        class_mode='sparse')

def plotImages(images_arr):
    fig, axes = plt.subplots(2, 5, figsize=(20,20))
    axes = axes.flatten()
    for img, ax in zip( images_arr, axes):
        ax.imshow(img)
        ax.axis('off')
    plt.tight_layout()
    plt.show()

augmented_images = [train_generator[0][0][2] for i in range(10)]
plotImages(augmented_images)

import matplotlib.pyplot as plt

# Get a batch of images and labels from the generator
images, labels = next(train_generator)

# Choose an image from the batch to display
image_index = 1  # You can change this to view a different image

# Display the image
plt.imshow(images[image_index])
plt.title(f"Label: {labels[image_index]}")
plt.show()

print(train_generator.class_indices)

"""Build the model"""

baseModel = VGG16(weights="imagenet", include_top=False,input_shape=(224,224,3))

for layer in baseModel.layers:
	layer.trainable = False

headModel = baseModel.output
headModel = GlobalAveragePooling2D() (headModel)
headModel = Dense(64, activation="relu")(headModel)
headModel = Dense(10, activation="softmax")(headModel)

model = Model(inputs=baseModel.input, outputs=headModel)

"""Compile the model

"""

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])

model.summary()

"""Train the model"""

model.fit(train_generator,
        steps_per_epoch=500,
        epochs=10)

#model.save('model.h5')

#model=load_model('model.h5')

"""Evaluate the model"""

model.evaluate(X,Y)

"""Make predictions"""

p=model.predict(X)

y_pred = p
y_true = Y
y_pred_classes = np.argmax(y_pred, axis=1)

# Calculate the confusion matrix
cm = confusion_matrix(y_true, y_pred_classes)

# Print the confusion matrix
print("Confusion Matrix:")
print(cm)

# Calculate precision for each class
precision_per_class = precision_score(y_true, y_pred_classes, average=None)

# Print precision for each class
for i, precision in enumerate(precision_per_class):
    print(f"Precision for class {i}: {precision:.2f}")

# Calculate overall precision (macro or weighted average if needed)
macro_precision = precision_score(y_true, y_pred_classes, average='macro')
print(f"Overall Precision (Macro Average): {macro_precision:.2f}")

"""Verify prediction

Make a selection
"""

s=11

pred=p[s]
print(pred)

m1=np.argmax(pred)
l1=label[m1]
print('prediction :',l1)

m2=Y[s]
l2=label[m2]
print('actual :',l2)

plt.imshow(X[s])