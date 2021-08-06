from recognition import TextRecognition


MODEL_PATH = './worker/ml/config/transformerocr.pth'


class OcrModel(object):

    """ Wrapper for loading and serving pre-trained model"""

    def __init__(self):
        self.model = self._load_model_from_path(MODEL_PATH)

    @staticmethod
    def _load_model_from_path(path):
        return TextRecognition(path_to_checkpoint=path)


    def predict(self, image, return_option=''):
        """
        Make batch prediction on list of preprocessed feature dicts.
        Returns class probabilities if 'return_options' is 'Prob', otherwise returns class membership predictions
        """
        if return_option == 'batch':
            predictions = self.model.predict_on_batch(image)
        else:
            predictions = self.model.predict(image)
        return predictions

   