
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных из CSV файла
file_path = '1.04. Real-life example.csv'  # Укажите путь к вашему CSV файлу
data = pd.read_csv(file_path)

# Просмотр первых 5 строк данных
print("Первые 5 строк данных:")
print(data.head())

# Основная информация о данных
print("\nОсновная информация о данных:")
print(data.info())

print("\nВсе колонки в DataFrame:")
print(data.columns.tolist())

# Фильтруем данные по годам и цене
years_to_select = [1969, 1986, 2005, 2014]
min_price = 1000
filtered_cars = data[(data['Year'].isin(years_to_select)) & (data['Price'] >= min_price)]

# Отделяем седаны и кроссоверы
sedans = filtered_cars[filtered_cars['Body'] == 'sedan']
crossovers = filtered_cars[filtered_cars['Body'] == 'crossover']

# Выводим таблицы для седанов и кроссоверов
print("\nСеданы:")
print(sedans)

print("\nКроссоверы:")
print(crossovers)

# Функция для нахождения нескольких самых дорогих автомобилей
def find_most_expensive_vehicles(vehicle_type, top_n=8):
    if not vehicle_type.empty:
        return vehicle_type.nlargest(top_n, 'Price')
    return None

most_expensive_sedans = find_most_expensive_vehicles(sedans, top_n=5)
most_expensive_crossovers = find_most_expensive_vehicles(crossovers, top_n=5)

# Создание DataFrame для самых дорогих автомобилей
most_expensive_vehicles = []

if most_expensive_sedans is not None:
    for _, sedan in most_expensive_sedans.iterrows():
        most_expensive_vehicles.append({
            'Тип': 'Седан',
            'Марка': sedan['Brand'],
            'Модель': sedan['Model'],
            'Год': sedan['Year'],
            'Цена': sedan['Price']
        })

if most_expensive_crossovers is not None:
    for _, crossover in most_expensive_crossovers.iterrows():
        most_expensive_vehicles.append({
            'Тип': 'Кроссовер',
            'Марка': crossover['Brand'],
            'Модель': crossover['Model'],
            'Год': crossover['Year'],
            'Цена в $': crossover['Price']
        })

# Создание DataFrame для самой дорогой информации
if most_expensive_vehicles:
    most_expensive_df = pd.DataFrame(most_expensive_vehicles)
    print("\nТаблица самых дорогих автомобилей:")
    print(most_expensive_df)
else:
    print("\nНет данных о самых дорогих автомобилях.")

# Поиск самого дорогого и самого дешевого автомобиля из отфильтрованных данных
if not filtered_cars.empty:
    most_expensive_car = filtered_cars.loc[filtered_cars['Price'].idxmax()]
    most_cheap_car = filtered_cars.loc[filtered_cars['Price'].idxmin()]

    print("\nСамый дорогой автомобиль из предложенной выборки:")
    print(most_expensive_car)

    print("\nСамый дешевый автомобиль из предложенной выборки:")

    print(most_cheap_car)

    # Расчет средней цены на самые дешевые автомобили
    average_price = filtered_cars['Price'].mean()
    print(f"\nСредняя цена на автомобили самого дешевого сегмента: ${average_price:.2f}")

# Задать марку и модель автомобиля для визуализации
brand = 'Volkswagen'  # Укажите нужный бренд
model = 'Jetta'  # Укажите нужную модель

# Фильтрация данных по марке и модели
filtered_cars_brand_model = data[(data['Brand'] == brand) & (data['Model'] == model)]

# Проверка наличия данных для построения графика
if not filtered_cars_brand_model.empty:
    # Построение графика зависимости цены от года
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=filtered_cars_brand_model, x='Year', y='Price', marker='o', color='blue', linewidth=2)
    plt.title(f'Зависимость цены {brand} {model} от года', fontsize=16)
    plt.xlabel('Год', fontsize=14)
    plt.ylabel('Цена в $', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()  # Подгоняем элементы графика
    # Отображение графика
    plt.show()
else:
    print(f"\nНет данных для марки {brand} и модели {model}.")

# Фильтруем марки автомобилей с пробегом ниже 200, но больше 160 и объемом двигателя ниже или равным 1.6
low_power_small_engine_cars = data[(data['Mileage'] > 160) & (data['Mileage'] < 200) & (data['EngineV'] <= 1.6)]

# Выводим таблицу отфильтрованных автомобилей
print("\nАвтомобили с пробегом ниже 200 и объемом двигателя ниже или равным 1.6:")
print(low_power_small_engine_cars[['Brand', 'Model', 'Mileage', 'EngineV']])

# Для создания диаграммы возьмем 10 наиболее распространенных брендов
top_brands = low_power_small_engine_cars['Brand'].value_counts().head(10)

# Построение диаграммы
plt.figure(figsize=(10, 6))
top_brands.plot(kind='bar')
plt.title('Топ 10 брендов автомобилей с пробегом от 160 до 200 и объемом двигателя ≤ 1.6')
plt.xlabel('Бренд')
plt.ylabel('Количество автомобилей')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Сортируем данные по пробегу
sorted_cars_by_mileage = low_power_small_engine_cars.sort_values(by='Mileage')

# Получаем 5 самых популярных брендов
top_brands_5 = sorted_cars_by_mileage['Brand'].value_counts().head(5).index.tolist()

# Фильтруем данные только для топ-5 брендов
filtered_cars_top_brands = sorted_cars_by_mileage[sorted_cars_by_mileage['Brand'].isin(top_brands_5)]

# Построение графика зависимости пробега
plt.figure(figsize=(10, 6))
sns.boxplot(x='Mileage', y='Brand', data=filtered_cars_top_brands, order=top_brands_5)

plt.title('Зависимость пробега от бренда автомобилей\n (Топ 5 брендов)', fontsize=16)
plt.xlabel('Пробег', fontsize=14)
plt.ylabel('Бренд', fontsize=14)
plt.xticks(rotation=45)
plt.grid(axis='x')
plt.tight_layout()
plt.show()