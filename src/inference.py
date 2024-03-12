# Импортируем необходимые библиотеки
from joblib import load
import numpy as np

# Загружаем обученную модель
model = load('iris_model.joblib')

# Вводим новые данные для предсказания (пример)
new_data = np.array([[5.1, 3.5, 1.4, 0.2],
                     [6.2, 3.4, 5.4, 2.3]])

# Делаем предсказания
predictions = model.predict(new_data)

# Выводим результаты
print(f"Предсказанные классы для новых данных: {predictions}")
