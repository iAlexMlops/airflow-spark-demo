# Импортируем необходимые библиотеки
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from joblib import dump

# Загрузим датасет Iris
iris = load_iris()
X, y = iris.data, iris.target

# Разделим данные на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Создаем и обучаем модель логистической регрессии
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Сохраняем обученную модель
dump(model, 'iris_model.joblib')
print("Модель обучена и сохранена как 'iris_model.joblib'")
