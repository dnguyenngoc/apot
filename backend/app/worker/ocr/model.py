from worker.ocr.recognition import TextRecognition


class OcrModel(object):

    """ Wrapper for loading and serving pre-trained model"""

    def __init__(self, path_to_checkpoint):
        self.model = self._load_model_from_path(path_to_checkpoint)


    @staticmethod
    def _load_model_from_path(path):
        return TextRecognition(path_to_checkpoint=path)


    def predict_text(self, image, return_option='normal'):
        """
        Make batch prediction on list of preprocessed feature dicts.
        Returns class probabilities if 'return_options' is 'Prob', otherwise returns class membership predictions
        """
        if return_option == 'batch':
            predictions = self.model.predict_on_batch(image)
        else:
            predictions = self.model.predict(image)
        return predictions

   