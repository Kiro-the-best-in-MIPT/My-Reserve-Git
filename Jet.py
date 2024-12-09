import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math

alphaDist = 50/900          # сколько мм в одном шаге
preasureQuiet = np.mean(np.loadtxt("disableVint.txt"))     # среднее давление при выключенном вентиляторе
preasure52 = np.mean(np.loadtxt("preasure52Monometr.txt"))  # показания датчика, соответствующие показаниям монометра 52 па
alphaPres = 52/(preasure52 - preasureQuiet)        # па в одном отсчете датчика

# создаём и заполняем массив координат в мм
dist = np.zeros(100)
for i in range(len(dist)):
    dist[i] = alphaDist * (10 * i - 500)


# Настраиваем оси графика
fig = plt.figure()
ax = plt.axes([0.1, 0.1, 0.8, 0.8])
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1, 0.0))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2, 0.0))
ax.set_title("Скорость потока в сечении затопленной струи")
ax.set_ylabel("Скорость потока, м/с")
ax.set_xlabel("Положение трубки Пито относительно центра струи, мм")
ax.grid(visible=True, which='minor', linestyle='dashed', linewidth=0.5)
ax.grid(visible=True, which='major')

def graf(preasure1, x):
    # Загружаем данные давления из файла и калибруем их
    preasure = np.loadtxt(preasure1)
    preasure = (alphaPres * (preasure - preasureQuiet))
    # Переводим давление в скорость
    velocity = (2 * preasure / 1.2)**0.5
    # Сдвигаем график, чтобы центр его максимума был на нуле
    max1 = 0.95*np.max(velocity)
    maxIndexes = []
    for i in range(100):
        if velocity[i] >= max1:
            maxIndexes.append(i)
    midIndex = (maxIndexes[-1] + maxIndexes[0])/2
    dist1 = dist - alphaDist * (10 * midIndex - 500)
    # Убираем флуктуации скорости там, где потока точно нет (появился из-за сломанного датчика)
    velocity -= 15
    velocity *= max1 / np.max(velocity)
    for i in range(100):
        if dist1[i] <= (-x) or dist1[i] >= x or velocity[i] < 0:
            velocity[i] = 0
    # Вычисляем расход
    q = 0
    for i in range(100):
        if velocity[i] != 0:
            q += math.pi * 0.0012 * (abs(dist1[i]) * velocity[i] + abs(dist1[i+1]) * velocity[i+1]) * abs(abs(dist1[i]) - abs(dist1[i+1]))
    # Строим график
    plt.plot(dist1, velocity, label=('Q(' + preasure1[8:10] + ' мм) = ' + str(round(q, 2)) + " г/с"))
    return q

pr00 = graf('preasure00.txt', 5)
pr10 = graf('preasure10.txt', 6)
pr20 = graf('preasure20.txt', 8)
pr30 = graf('preasure30.txt', 9)
pr40 = graf('preasure40.txt', 11)
pr50 = graf('preasure50.txt', 13)
pr60 = graf('preasure60.txt', 15)
pr70 = graf('preasure70.txt', 16)
pr80 = graf('preasure80.txt', 16)
pr90 = graf('preasure90.txt', 17)
ax.legend()
plt.show()


# Строим график зависимости расхода от расстояния до сопла
fig = plt.figure()
ax = plt.axes([0.1, 0.1, 0.8, 0.8])
ax.xaxis.set_minor_locator(ticker.MultipleLocator(1, 0.0))
ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.2, 0.0))
ax.set_title("Расход в зависимости от расстояния трубки Пито до сопла")
ax.set_ylabel("Расход, г/с")
ax.set_xlabel("Расстояние от сопла, мм")
ax.grid(visible=True, which='minor', linestyle='dashed', linewidth=0.5)
ax.grid(visible=True, which='major')
y = [pr00, pr10, pr20, pr30, pr40, pr50, pr60, pr70, pr80, pr90]
x = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90]
ax.set_ylim(0, round(np.max(y) + 1))
plt.plot(x, y, '-o')
plt.show()

