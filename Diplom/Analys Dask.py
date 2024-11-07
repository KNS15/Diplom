
import dask.dataframe as dd
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Считывание данных
ddf = dd.read_csv('1.04. Real-life example.csv', dtype={'Price': 'float64'})

# Настройки отображения
pd.set_option('display.max_columns', 9)

# Вывод первых пяти строк базы данных
print(ddf.head())

# Информация по базе данных
print(ddf.info())

# Удаление строк с пустыми значениями
complete_ddf = ddf.dropna()

# Описание данных
description = complete_ddf.describe().compute()
print(description)

# Группировка данных по 'Year' и агрегация цен
yearly_price_summary = complete_ddf.groupby('Year')['Price'].agg(['mean', 'min', 'max', 'count']).compute()
print(yearly_price_summary)

# **Добавление графика зависимости цены от года для средних значений**
plt.figure(figsize=(10, 6))
sns.lineplot(data=yearly_price_summary.reset_index(), x='Year', y='mean', marker='o')
plt.title('Изменение средней цены автомобилей по годам')
plt.xlabel('Год')
plt.ylabel('Средняя цена')
plt.xticks(rotation=45)  # Поворот меток по оси X для лучшей читаемости
plt.grid()  # Добавление сетки для удобства восприятия
plt.show()

# Визуализация распределения цен
plt.figure(figsize=(10, 6))
sns.histplot(complete_ddf['Price'].compute(), bins=30, kde=True)
plt.title('Распределение цен')
plt.xlabel('Цена')
plt.ylabel('От бюджетных, до премиум класса')
plt.show()

# Фильтрация бензиновых автомобилей
gasoline_cars = complete_ddf[complete_ddf['Engine Type'] == 'Petrol']

# Проверка на наличие бензиновых автомобилей
if len(gasoline_cars.index) > 0:
    # Вычисление самой дорогой и самой дешевой бензиновой машины
    most_expensive_price = gasoline_cars['Price'].max().compute()
    most_expensive_cars = gasoline_cars[gasoline_cars['Price'] == most_expensive_price].compute()

    least_expensive_price = gasoline_cars['Price'].min().compute()
    least_expensive_cars = gasoline_cars[gasoline_cars['Price'] == least_expensive_price].compute()

    print("Самый дорогой бензиновый автомобиль:")
    print(most_expensive_cars)

    print("\nСамый дешевый бензиновый автомобиль:")
    print(least_expensive_cars)
else:
    print("Нет бензиновых автомобилей в наборе данных.")

# Группировка данных по 'Engine Type' и агрегация средних цен
engine_price_summary = complete_ddf.groupby('Engine Type')['Price'].agg('mean').compute().reset_index()

# Визуализация средних цен по типам двигателей
plt.figure(figsize=(10, 6))
sns.barplot(data=engine_price_summary, x='Engine Type', y='Price', hue='Engine Type', palette='viridis', legend=False)
plt.title('Средняя цена автомобилей по типу двигателя')
plt.xlabel('Тип двигателя')
plt.ylabel('Средняя цена')
plt.xticks(rotation=45)  # Поворот меток по оси X для лучшей читаемости
plt.grid(axis='y')  # Добавление сетки по оси Y
plt.show()


# Группировка данных по типу двигателя и подсчет количества автомобилей
engine_type_count = complete_ddf['Engine Type'].value_counts().compute().reset_index()
engine_type_count.columns = ['Engine Type', 'Count']

# Построение диаграммы количества автомобилей по типу двигателя
plt.figure(figsize=(10, 6))
sns.barplot(data=engine_type_count, x='Engine Type', y='Count', hue='Engine Type', palette='viridis', legend=False)
plt.title('Количество автомобилей по типу двигателя')
plt.xlabel('Тип двигателя')
plt.ylabel('Количество автомобилей')
plt.xticks(rotation=45)  # Поворот меток по оси X для лучшей читаемости
plt.grid(axis='y')  # Добавление сетки по оси Y
plt.show()


# Фильтрация данных для мощности более 250 л.с.
high_power_cars = complete_ddf[complete_ddf['Mileage'] > 250]

# Группировка данных по марке автомобиля и подсчет количества
brand_power_count = high_power_cars['Brand'].value_counts().compute().reset_index()
brand_power_count.columns = ['Brand', 'Count']

# Построение диаграммы количества автомобилей по марке
plt.figure(figsize=(10, 6))
sns.barplot(data=brand_power_count, x='Brand', y='Count', hue='Brand', palette='viridis', legend=False)
plt.title('Количество автомобилей с мощностью более 250 л.с. по марке')
plt.xlabel('Марка автомобиля')
plt.ylabel('Количество автомобилей')
plt.xticks(rotation=45)  # Поворот меток по оси X для лучшей читаемости
plt.grid(axis='y')  # Добавление сетки по оси Y
plt.show()

