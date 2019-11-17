import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense
from tensorflow.keras.models import Model


# ! Don't forget add default weights
def make_model(model_name='mobilenet_v2', weights=''):
    
    try:
        if (model_name == 'mobilenet_v2'):
            base_model = MobileNetV2(weights='imagenet',input_shape=(224, 224, 3), include_top=False)

            x = base_model.output

            x = GlobalAveragePooling2D()(x)

            x = Dense(1024, activation='relu')(x)

            predictions = Dense(2, activation='softmax')(x)

            model = Model(inputs=base_model.input, outputs=predictions)

            model.load_weights(weights)

        return model

    except:
        print('ERROR::MODEL')
        return
        


