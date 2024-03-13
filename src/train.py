from pyspark.sql import SparkSession
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from joblib import dump
import pandas as pd
from loguru import logger


logger.info("Инициализация Spark сессии")
spark = SparkSession.builder.appName("IrisSklearnTraining").getOrCreate()

logger.info("Загрузка датасета Iris")
iris = load_iris()
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target
iris_df = spark.createDataFrame(iris_df).toPandas()

logger.info("Разделение данных на обучающую и тестовую выборки")
X = iris_df.drop('target', axis=1)
y = iris_df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

logger.info("Обучение модели Logistic Regression")
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

logger.info("Сохранение обученной модели")
dump(model, 'iris_model_sklearn.joblib')

logger.info("Обучение модели завершено")
spark.stop()
