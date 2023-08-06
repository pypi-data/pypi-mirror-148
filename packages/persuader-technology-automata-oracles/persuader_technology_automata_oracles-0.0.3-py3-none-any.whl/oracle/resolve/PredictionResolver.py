from typing import List

from oracle.Oracle import Oracle
from oracle.Prediction import Prediction


class PredictionResolver:

    def __init__(self, oracles):
        self.oracles: List[Oracle] = oracles

    def resolve(self, instrument, data):
        self.set_all_oracle_with_data(data)
        predictions = self.collect_predictions_from_all_oracles(instrument)
        best_prediction = self.determine_best_profitable_prediction(predictions)
        return best_prediction

    def set_all_oracle_with_data(self, data):
        for oracle in self.oracles:
            oracle.set_data(data)

    def collect_predictions_from_all_oracles(self, instrument) -> List[Prediction]:
        predictions = []
        for oracle in self.oracles:
            prediction = oracle.predict(instrument)
            predictions.append(prediction)
        valid_predictions = [p for p in predictions if p is not None]
        return valid_predictions

    @staticmethod
    def determine_best_profitable_prediction(predictions: List[Prediction]):
        if not predictions:
            return None
        sorted_predictions = sorted(predictions, key=lambda prediction: prediction.profit)
        return sorted_predictions[0]
