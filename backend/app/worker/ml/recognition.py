from PIL import Image
import os
import yaml
from predictor import Predictor


FILE_BASE = './worker/ml/config/base.yml'
FILE_CONFIG = './worker/ml/config/vgg-transformer.yml'

class TextRecognition(object):
    def __init__(self, path_to_checkpoint):
        self.config = self.load_config(path_to_checkpoint)
        self.detector = Predictor(self.config)


    def load_config(self, path_to_checkpoint):
        base_config = self.read_from_config(file_yml=FILE_BASE)
        config = self.read_from_config(file_yml=FILE_CONFIG)

        # update base config
        base_config.update(config)

        # load model from checkpoint
        base_config['weights'] = path_to_checkpoint
        base_config['device'] = 'cpu'
        base_config['predictor']['beamsearch'] = False

        return base_config


    @staticmethod
    def read_from_config(file_yml):
        with open(file_yml, encoding='utf-8') as f:
            config = yaml.safe_load(f)

        return config

    def predict(self, image):
        image = Image.fromarray(image)
        result = self.detector.predict(image)

        return result

    def predict_on_batch(self, batch_images):
        return self.detector.batch_predict(batch_images)