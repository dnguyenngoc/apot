import joblib
import os

MODEL_PATH = os.environ['MODEL_PATH']


class OcrModel:

    """ Wrapper for loading and serving pre-trained model"""

    def __init__(self):
        self.model = self._load_model_from_path(MODEL_PATH)

    @staticmethod
    def _load_model_from_path(path):
        model = joblib.load(path)
        return model

    def predict(self, image, return_option='Prob'):
        """
        Make batch prediction on list of preprocessed feature dicts.
        Returns class probabilities if 'return_options' is 'Prob', otherwise returns class membership predictions
        """
        if return_option == 'Prob':
            predictions = self.model.predict_proba(image)
        else:
            predictions = self.model.predict(image)
        return predictions