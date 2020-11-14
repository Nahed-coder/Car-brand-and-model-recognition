
from tensorflow.keras.layers import Dense, Flatten, Dropout
import keras
import tensorflow as tf
from keras.applications.vgg16 import VGG16
from keras.layers.normalization import BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
import numpy as np
from glob import glob
import matplotlib.pyplot as plt


IMAGE_SIZE = [224, 224]

train_Path ='train'
test_Path ='validation'

folders = glob(train_Path + '/*')

vgg = VGG16(input_shape=IMAGE_SIZE + [3], weights='imagenet', include_top=False)

for layer in vgg.layers:
    layer.trainable = False

x = Flatten()(vgg.output)

x = BatchNormalization()(x)
x = Dropout(0.8)(x)
x = Dense(512, activation='relu')(x)
x = BatchNormalization()(x)
x = Dropout(0.8)(x)
x = Dense(len(folders), activation='softmax')(x)

model = Model(vgg.input, outputs=x)
model.summary()

opt = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile (
    loss = 'categorical_crossentropy',
    optimizer = opt,
    metrics = ['AUC']
)

train_datagen = ImageDataGenerator(
    rescale = 1./255,
    shear_range = 0.2,
    zoom_range = 0.2,
    horizontal_flip = True
)

test_datagen = ImageDataGenerator(
    rescale = 1./255
)

training_set = train_datagen.flow_from_directory(
    train_Path,
    target_size = IMAGE_SIZE,
    shuffle=True,
    batch_size = 16,
    class_mode = 'categorical' 

test_set = train_datagen.flow_from_directory(
    test_Path,
    target_size = IMAGE_SIZE,
    shuffle=True,
    batch_size = 16,
    class_mode = 'categorical'
)

checkpoint_path ="/vgg/vgg.ckpt"

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_path,
    verbose=1,
    save_weights_only=True,
    save_freq='epoch')

early = tf.keras.callbacks.EarlyStopping(
    monitor="loss",
    min_delta=1,
    patience=30,
    verbose=1,
    mode="min",
    baseline=0.15,
    restore_best_weights=False,
)

callbacks_list = [checkpoint, early]

checkpoint_dir = os.path.dirname(checkpoint_path)
#latest = tf.train.latest_checkpoint(checkpoint_dir)
#model.load_weights(latest)


history = model.fit(
    training_set,
    validation_data = test_set,
    epochs = 30,
    steps_per_epoch = len(training_set),
    validation_steps = len(test_set),
    callbacks=callbacks_list
)


plt.plot(history.history['loss'], label = 'train_loss')
plt.plot(history.history['val_loss'], label ='val loss')
plt.legend()
plt.show()


plt.plot(history.history['auc'], label = 'auc')
plt.plot(history.history['val_auc'], label ='val accuracy')
plt.legend()
plt.show()

model.save('./vgg.h5')