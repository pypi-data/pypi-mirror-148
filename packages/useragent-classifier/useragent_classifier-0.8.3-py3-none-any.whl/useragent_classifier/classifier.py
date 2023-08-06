from typing import List, Dict

import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import (
    TfidfVectorizer,
    CountVectorizer,
    TfidfTransformer,
)

from features_importances import FeatureImportance
from custom_transformers.transformers import SplitWords, AutomatedKMeans


class UserAgentClassifier:
    def __init__(self, n_clusters: List[int], n_top_words: int):
        self.pipe = Pipeline(
            [
                ("splitter", SplitWords("ua")),
                ("tfidf", TfidfVectorizer(ngram_range=(1, 3))),
            ]
        )
        self.n_clusters = n_clusters
        self.n_top_words = n_top_words
        self._features_importances = None
        self._features_importances_json = None

    def __features_names(self):
        return self.pipe.named_steps["tfidf"].get_feature_names_out()

    def __compute_feature_importance(
        self, labels: List[int], df: pd.DataFrame
    ) -> Dict[int, pd.DataFrame]:
        computer = FeatureImportance(
            self.__features_names(), labels, df, self.n_top_words
        )
        self._features_importances = computer.get_features_importances_one_vs_all()

        self._features_importances_json = {
            str(k): v.to_json() for k, v in self._features_importances.items()
        }

    def preprocessing(self, df: pd.DataFrame) -> pd.DataFrame:
        self.pipe.fit(df)
        res = self.pipe.transform(df)
        return res

    def get_cluster(self, df: pd.DataFrame) -> pd.DataFrame:
        df_preprocessed = self.preprocessing(df)

        kmeans = AutomatedKMeans(self.n_clusters)
        kmeans.fit(df_preprocessed)
        cluster = kmeans.predict(df_preprocessed)

        self.__compute_feature_importance(cluster, df_preprocessed)
        return pd.Series(cluster)
