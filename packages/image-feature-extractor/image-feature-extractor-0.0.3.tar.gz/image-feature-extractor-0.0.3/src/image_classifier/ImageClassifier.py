from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Flatten
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


class ImageClassifier(object):
    # user calls extract, fit, predict

    def __init__(self, use_classifier_or_feat_extractor, model=None):
        # initializing the model
        # if no saved model is provided, then download resnet50 and tune it
        self.img_size = 224
        self.model = model
        self.init_model = None
        if use_classifier_or_feat_extractor == 'classifier':
            if model is None:
                self.init_model = ResNet50(weights='imagenet', include_top=False,
                                           input_shape=(self.img_size, self.img_size, 3),
                                           pooling='max')
        else:
            # use_classifier_or_feat_extractor == 'feat_extractor'
            self.init_model = model
            self.init_model_feat_extractor()

    def init_model_feat_extractor(self):
        if self.init_model:
            from tensorflow.keras.models import Model

            self.model = Model(inputs=self.init_model.input,
                               outputs=self.init_model.layers[-2].output)
        else:
            base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(self.img_size, self.img_size, 3), pooling='max')
            # Customize the model to return features from fully-connected layer
            self.model = base_model

    def extract(self, input_image):
        # the user calls it to extract image features
        if self.model is not None:
            # Resize the image
            img = input_image.resize((224, 224))
            # Convert the image color space
            img = img.convert('RGB')
            # Reformat the image
            x = image.img_to_array(img)
            # (1, height, width, channels), add a dimension because the model expects this shape: (batch_size, height, width, channels)
            img_tensor = np.expand_dims(x, axis=0)
            input_to_model = preprocess_input(img_tensor)
            # Extract Features
            feature = self.model.predict(input_to_model)[0]
            return feature / np.linalg.norm(feature)

    def tune_resnet_model(self, tune_from, num_classes, lr):
        self.init_model.trainable = True
        # Fine-tune from this layer onwards
        fine_tune_at = tune_from
        # Freeze all the layers before the `fine_tune_at` layer
        for layer in self.init_model.layers[:fine_tune_at]:
            layer.trainable = False
        resnet50_x = Flatten()(self.init_model.output)
        resnet50_x = Dense(num_classes, activation='softmax')(resnet50_x)
        resnet50_x_final_model = Model(inputs=self.init_model.input, outputs=resnet50_x)
        base_learning_rate = lr
        resnet50_x_final_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=base_learning_rate),
                                       loss=tf.keras.losses.categorical_crossentropy,
                                       metrics=['accuracy'])

        self.model = resnet50_x_final_model

    def fit(self, train_data, val_data, epochs, tune_from=120, lr=0.0001, batch_size=32):
        # the user calls it to tune and train resnet50
        num_classes = len(train_data.class_indices.keys())
        if not self.model:
            # No input model, so tune resnet50, and insert model to self.model
            self.tune_resnet_model(tune_from, num_classes, lr)
        history_fine = self.model.fit(train_data,
                                      epochs=epochs, validation_data=val_data, batch_size=batch_size)
        return self.model, history_fine

    def predict(self, image_path):
        # the user calls it to predict an image class
        if self.model is not None:
            img = image.load_img(image_path, target_size=(self.img_size, self.img_size))
            img_tensor = image.img_to_array(img)  # (height, width, channels)
            img_tensor = np.expand_dims(img_tensor,
                                        axis=0)
            img_tensor /= 255.  # imshow expects values in the range [0, 1]
            classes_prob = self.model.predict(img_tensor)
            return classes_prob
