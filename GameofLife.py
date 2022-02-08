# Модули
import pygame as pg # Модуль визуализации
import random # Модуль для генерации случайных чисел
import sys
import os

# Настройки игры
size = 15 # Размер клеток
k = 1 # Число, во сколько раз окно будет меньше изначального, при k = 1
gridturn = 1 # Вкл(1)/Выкл(0) сетку
ncell = 0 # Количество первичных случайно закрашенных клеток (в случае, если аргумент равен 0 выведется случайное количество клеток)
livecell = "green" # Цвет живой клетки
deadcell = "black" # Цвет мертвой клетки
grid = "grey" # Цвет сетки


# Для регулирования настроек через txt файл
lof = os.path.abspath(sys.argv[0])
lof = [lof[w] for w in range(len(lof))]
for _ in range(13):
    del lof[-1]

string = [line for line in open("".join(lof) + "Settings.txt")]
size = int(string[0])
k = float(string[1])
gridturn = int(string[2])
ncell = int(string[3])
livecell = [_ for _ in string[4]]
del livecell[-1]
livecell = "".join(livecell)
deadcell = string[5]



# Переменные экрана
FPS = 21 # Количество кадров в секунду (скорость работы программы)
pg.display.init()
i = pg.display.Info()
currentw = i.current_w // k # Размер окна по горизонтали
currenth = (i.current_h - 80) // k # Размер клеток по вертикали
reswidth = int(currentw - (currentw) % size)
resheight = int(currenth - (currenth) % size) 
width_count, height_count = reswidth // size, resheight // size # Количество клеток по горизонтали и вертикали соответственно
pg.display.set_caption("Game of Life  " + "Поколение: 0 " + "FPS: "  + str(FPS)) # Название программы и дополнительная информация
resolution = width, height = reswidth, resheight # Расчет высоты и ширины экрана
screen = pg.display.set_mode(resolution) # Создание окна с расчитанным разрешением экрана
clock = pg.time.Clock()
screen.fill(pg.Color('black')) # Цвет фона


color = []
for x in range(width_count): # Создание поля с пустыми клетками
    for y in range(height_count):
        pg.draw.rect(screen, deadcell, pg.Rect(size * x, size * y, size, size))
        color.append("x" + str(x) + "y" + str(y))

color1, color2 = color.copy(), color.copy()
paused = True
k = 0


while 1:
    for event in pg.event.get():
        if event.type == pg.QUIT: # Закрытие программы
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if pg.key.get_pressed()[pg.K_SPACE]: # Подсчет случайного количества закрашенных клеток при нажатии клавиши пробел
                color, color1 = color2.copy(), color2.copy()
                for x in range(width_count):
                    for y in range(height_count):
                        pg.draw.rect(screen, deadcell, pg.Rect(size * x, size * y, size, size))

                number = [_ for _ in range(1, width_count * height_count + 1)]

                if ncell == 0:
                    num = random.choice(number)
                else:
                    num = ncell
                # Для генерации случайного местонахождения клетки по горизонтали
                xr = [_ for _ in range(width_count)]

                # Для генерации случайного местонахождения клетки по вертикали
                yr = [_ for _ in range(height_count)]

                xye = []
                for n in range(num): # Расположение случайной клетки
                    xrc = random.choice(xr)
                    yrc = random.choice(yr)
                    if ("x" + str(xrc) + "y" + str(yrc)) in xye:
                        continue
                    xye.append(("x" + str(xrc) + "y" + str(yrc)))
                    pg.draw.rect(screen, livecell, pg.Rect(size * xrc, size * yrc, size, size))
                    i = color2.index("x" + str(xrc) + "y" + str(yrc))
                    del color[i]
                    color.insert(i, "1")
                color1 = color.copy()
                paused = False
                k = 0

        if (event.type == pg.MOUSEBUTTONDOWN and event.button == 3) or (event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_p]): # Задание паузы при щелчке правой кнопки мыши или нажатии буквы "P"
            paused = not paused

        if ((event.type == pg.MOUSEBUTTONDOWN and event.button == 4) or (event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_UP])) and FPS < 59: # Изменение скорости игры при прокрутке средней кнопки мыши или нажатии вверхних и нижних стрелок
            FPS += 2
        if ((event.type == pg.MOUSEBUTTONDOWN and event.button == 5) or (event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_DOWN])) and 1 < FPS < 60:
            FPS -= 2

        if color1 == color2:
            paused = True
            k = 0

        pg.display.set_caption("Game of Life  " + "Поколение: " + str(k) + " FPS: " + str(FPS))

        if (event.type == pg.MOUSEBUTTONDOWN and event.button == 2) or (event.type == pg.KEYDOWN and pg.key.get_pressed()[pg.K_o]): # Очистка поля при нажатии средней кнопки мыши или буквы "O"
            color, color1 = color2.copy(), color2.copy()
            for x in range(width_count):
                for y in range(height_count):
                    pg.draw.rect(screen, deadcell, pg.Rect(size * x, size * y, size, size))
            k = 0

        if paused:

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1: # Закрашивание клетки при нажатии левой кнопки мыши
                pos = event.pos
                if 0 <= pos[0] <= (width_count * size - 1) and 0 <= pos[1] <= (height_count * size - 1):
                    mousex = pos[0] // size
                    mousey = pos[1] // size

                    cind = color2.index("x" + str(mousex) + "y" + str(mousey))

                    if color[cind] == "1":
                        pg.draw.rect(screen, deadcell, pg.Rect(size * mousex, size * mousey, size, size))
                        del color[cind]
                        color.insert(cind, color2[cind])
                        del color1[cind]
                        color1.insert(cind, color2[cind])
                    else:
                        pg.draw.rect(screen, livecell, pg.Rect(size * mousex, size * mousey, size, size))
                        del color[cind]
                        color.insert(cind, "1")
                        del color1[cind]
                        color1.insert(cind, "1")

            if gridturn == 1:
                # Параметры сетки
                [pg.draw.line(screen, grid, (x,0), (x, height)) for x in range(0, width, size)]
                [pg.draw.line(screen, grid, (0,y), (width, y)) for y in range(0, height, size)]
            # FPS
            clock.tick(60)
            pg.display.flip()

    if not paused:
        k += 1
        pg.display.set_caption("Game of Life  " + "Поколение: " + str(k) + " FPS: " + str(FPS))

        for x in range(width_count): # Проверка клеток по правилам "игры жизнь"
            for y in range(height_count):
                
                xy = y + height_count * x
                b0 = color1[xy]

                if 0 < x < (width_count - 1) and 0 < y < (height_count - 1):
                    ind = 0

                    b1 = color1[xy - height_count - 1]
                    b2 = color1[xy - 1]
                    b3 = color1[xy + height_count - 1]
                    b4 = color1[xy + height_count]
                    b5 = color1[xy + height_count + 1]
                    b6 = color1[xy + 1]
                    b7 = color1[xy - height_count + 1]
                    b8 = color1[xy - height_count]

                    if b1 == "1":
                        ind += 1
                    if b2 == "1":
                        ind += 1
                    if b3 == "1":
                        ind += 1
                    if b4 == "1":
                        ind += 1
                    if b5 == "1":
                        ind += 1
                    if b6 == "1":
                        ind += 1
                    if b7 == "1":
                        ind += 1
                    if b8 == "1":
                        ind += 1

                elif 0 < x < (width_count - 1) and y == 0:
                    ind = 0

                    b4 = color1[xy + height_count]
                    b5 = color1[xy + height_count + 1]
                    b6 = color1[xy + 1]
                    b7 = color1[xy - height_count + 1]
                    b8 = color1[xy - height_count]

                    if b4 == "1":
                        ind += 1
                    if b5 == "1":
                        ind += 1
                    if b6 == "1":
                        ind += 1
                    if b7 == "1":
                        ind += 1
                    if b8 == "1":
                        ind += 1

                elif 0 < x < (width_count - 1) and y == (height_count - 1):
                    ind = 0

                    b1 = color1[xy - height_count - 1]
                    b2 = color1[xy - 1]
                    b3 = color1[xy + height_count - 1]
                    b4 = color1[xy + height_count]
                    b8 = color1[xy - height_count]

                    if b1 == "1":
                        ind += 1
                    if b2 == "1":
                        ind += 1
                    if b3 == "1":
                        ind += 1
                    if b4 == "1":
                        ind += 1
                    if b8 == "1":
                        ind += 1

                elif x == 0 and y == 0:
                    ind = 0

                    b4 = color1[xy + height_count]
                    b5 = color1[xy + height_count + 1]
                    b6 = color1[xy + 1]

                    if b4 == "1":
                        ind += 1
                    if b5 == "1":
                        ind += 1
                    if b6 == "1":
                        ind += 1
                    
                elif x == 0 and y == (height_count - 1):
                    ind = 0

                    b2 = color1[xy - 1]
                    b3 = color1[xy + height_count - 1]
                    b4 = color1[xy + height_count]

                    if b2 == "1":
                        ind += 1
                    if b3 == "1":
                        ind += 1
                    if b4 == "1":
                        ind += 1

                elif x == (width_count - 1) and y == 0:
                    ind = 0

                    b6 = color1[xy + 1]
                    b7 = color1[xy - height_count + 1]
                    b8 = color1[xy - height_count]

                    if b6 == "1":
                        ind += 1
                    if b7 == "1":
                        ind += 1
                    if b8 == "1":
                        ind += 1

                elif x == (width_count - 1) and y == (height_count - 1):
                    ind = 0

                    b1 = color1[xy - height_count - 1]
                    b2 = color1[xy - 1]
                    b8 = color1[xy - height_count]

                    if b1 == "1":
                        ind += 1
                    if b2 == "1":
                        ind += 1
                    if b8 == "1":
                        ind += 1

                elif x == 0 and 0 < y < (height_count - 1):
                    ind = 0

                    b2 = color1[xy - 1]
                    b3 = color1[xy + height_count - 1]
                    b4 = color1[xy + height_count]
                    b5 = color1[xy + height_count + 1]
                    b6 = color1[xy + 1]

                    if b2 == "1":
                        ind += 1
                    if b3 == "1":
                        ind += 1
                    if b4 == "1":
                        ind += 1
                    if b5 == "1":
                        ind += 1
                    if b6 == "1":
                        ind += 1

                elif x == (width_count - 1) and 0 < y < (height_count - 1):
                    ind = 0

                    b1 = color1[xy - height_count - 1]
                    b2 = color1[xy - 1]
                    b6 = color1[xy + 1]
                    b7 = color1[xy - height_count + 1]
                    b8 = color1[xy - height_count]

                    if b1 == "1":
                        ind += 1
                    if b2 == "1":
                        ind += 1
                    if b6 == "1":
                        ind += 1
                    if b7 == "1":
                        ind += 1
                    if b8 == "1":
                        ind += 1

                if b0 != "1":
                    if ind == 3:
                        pg.draw.rect(screen, livecell, pg.Rect(size * x, size * y, size, size))
                        del color[xy]
                        color.insert(xy, "1")

                elif b0 == "1":
                    if ind == 2 or ind == 3:
                        pg.draw.rect(screen, livecell, pg.Rect(size * x, size * y, size, size))
                    else:
                        pg.draw.rect(screen, deadcell, pg.Rect(size * x, size * y, size, size))
                        del color[xy]
                        color.insert(xy, ("x" + str(x) + "y" + str(y)))
        if color1 == color: # Пауза, если в окне не происходит никаких изменений
            paused = True     
        color1 = color.copy()
        if gridturn == 1:
            # Параметры сетки
            [pg.draw.line(screen, grid, (x,0), (x, height)) for x in range(0, width, size)]
            [pg.draw.line(screen, grid, (0,y), (width, y)) for y in range(0, height, size)]
        # FPS
        clock.tick(FPS)
        pg.display.flip()
    
        

    









    












    