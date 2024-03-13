from pyspark.sql import SparkSession
from sklearn.datasets import load_iris
import pandas as pd
from loguru import logger
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

logger.info("Инициализация Spark сессии")
spark = SparkSession.builder.appName("IrisSklearnPrediction").getOrCreate()

# ------------------------------------------------------------
# Тут должна производиться загрузка модели, например из MLFlow
# Для тестового сценария, мы просто ее еще раз пересоздадим
# ------------------------------------------------------------
logger.info("Загрузка обученной модели")
iris = load_iris()
iris_df = pd.DataFrame(iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target
iris_df = spark.createDataFrame(iris_df).toPandas()
X = iris_df.drop('target', axis=1)
y = iris_df['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

logger.info("Подготовка данных для предсказания. Первые 3 элемента исходного датасета")
iris_data = load_iris().data[:3]
iris_df = pd.DataFrame(iris_data, columns=load_iris().feature_names)
iris_df = spark.createDataFrame(iris_df).toPandas()

logger.info("Выполнение предсказаний")
predictions = model.predict(iris_df)

logger.info(f"Предсказанные классы: {predictions}")

spark.stop()
logger.info("Процесс предсказания завершен")
