from typing import List

from oracle.Oracle import Oracle
from oracle.Prediction import Prediction


class PredictionResolver:

    def __init__(self, oracles):
        self.oracles: List[Oracle] = oracles

    # todo: position + data needs to be injected (at run)
    # todo: test with 'simple oracles'
    def resolve(self):
        predictions = self.collect_predictions_from_all_oracles()
        best_prediction = self.determine_best_profitable_prediction(predictions)
        return best_prediction

    def collect_predictions_from_all_oracles(self) -> List[Prediction]:
        predictions = []
        for oracle in self.oracles:
            # todo: need instrument (could be position <- instrument)
            # todo: what to predict from (data - high level interface)
            prediction = oracle.predict()
            predictions.append(prediction)
        valid_predictions = [p for p in predictions if p is not None]
        return valid_predictions

    @staticmethod
    def determine_best_profitable_prediction(predictions: List[Prediction]):
        if not predictions:
            return None
        sorted_predictions = sorted(predictions, key=lambda prediction: prediction.profit)
        return sorted_predictions[0]
