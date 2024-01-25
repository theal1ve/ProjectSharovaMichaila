import io
import pygame
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from PyQt5 import uic
import sys
import sqlite3

templete_get_name = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QWidget" name="verticalLayoutWidget">
   <property name="geometry">
    <rect>
     <x>40</x>
     <y>60</y>
     <width>331</width>
     <height>161</height>
    </rect>
   </property>
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QLabel" name="label">
      <property name="text">
       <string>Здравствуйте, для продолжения введите вашу имя и фамилию</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QLabel" name="label_2">
      <property name="text">
       <string>(В имянительном падеже и через пробел)</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QLabel" name="ErorrLabel">
      <property name="text">
       <string/>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QLineEdit" name="NameLineEdit"/>
    </item>
    <item>
     <widget class="QPushButton" name="NextBtn">
      <property name="text">
       <string>Продолжить</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

templete_Game_over = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>300</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QWidget" name="verticalLayoutWidget">
   <property name="geometry">
    <rect>
     <x>60</x>
     <y>50</y>
     <width>271</width>
     <height>181</height>
    </rect>
   </property>
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QLabel" name="label">
      <property name="text">
       <string>Игра окончена!</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QLabel" name="label_2">
      <property name="text">
       <string>В следующий раз повезёт!</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QLabel" name="CountLabel">
      <property name="text">
       <string>Ваш счёт: </string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QPushButton" name="RestartGameBtn">
      <property name="text">
       <string>Начать заново</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QPushButton" name="BackToMainMenuBtn">
      <property name="text">
       <string>Выйти в главное меню</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

templete_Main_Menu = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>400</width>
    <height>600</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Form</string>
  </property>
  <widget class="QWidget" name="verticalLayoutWidget">
   <property name="geometry">
    <rect>
     <x>89</x>
     <y>39</y>
     <width>231</width>
     <height>171</height>
    </rect>
   </property>
   <layout class="QVBoxLayout" name="verticalLayout">
    <item>
     <widget class="QLabel" name="WelcomeLineEdit">
      <property name="text">
       <string>Привет </string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QLabel" name="LastCountLineEdit">
      <property name="text">
       <string>Ваш последний результат:</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QLabel" name="BestCountLineEdit">
      <property name="text">
       <string>Ваш лучший результат:</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QLabel" name="label_4">
      <property name="text">
       <string>Выберите режим игры</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QPushButton" name="SoloGameBtn">
      <property name="text">
       <string>Играть в solo</string>
      </property>
     </widget>
    </item>
    <item>
     <widget class="QPushButton" name="DuoGameBtn">
      <property name="text">
       <string>Играть в duo</string>
      </property>
     </widget>
    </item>
   </layout>
  </widget>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

pygame.init()
# шрифт для вывода счета
font20 = pygame.font.Font(None, 20)
# цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
# размер окна
WIDTH, HEIGHT = 400, 600
# создаем экран пайгейм
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# изменяем название приложению
pygame.display.set_caption("Пин-Понг(Шаров Михаил Евгеньевич)")
clock = pygame.time.Clock()
# кол-во кадров в секунду
FPS = 30


# класс ракеток
class Racket():
    def __init__(self, posx, posy, width, height, speed, color):
        super().__init__()
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        # создаем прямоугольник
        self.geekRect = pygame.Rect(posx, posy, width, height)
        # отрисовываем его на экране
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    def display(self):
        self.geek = pygame.draw.rect(screen, self.color, self.geekRect)

    # изменяем поожение ракетки на экране
    def update(self, xFac):
        self.posx = self.posx + self.speed * xFac

        if self.posx <= 0:
            self.posx = 0

        elif self.posx + self.width >= WIDTH:
            self.posx = WIDTH - self.width

        self.geekRect = (self.posx, self.posy, self.width, self.height)
    # обновление положения ракеток для двоих
    def update2(self, yFac):
        self.posy = self.posy + self.speed * yFac

        if self.posy <= 0:
            self.posy = 0

        elif self.posy + self.height >= HEIGHT:
            self.posy = HEIGHT - self.height

        self.geekRect = (self.posx, self.posy, self.width, self.height)

    # отображаем игровойй счет
    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        screen.blit(text, textRect)

    # извлекаем кординаты ракетки
    def getRect(self):
        return self.geekRect


# класс мячика
class Ball():
    def __init__(self, posx, posy, radius, speed, color):
        super().__init__()
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        # рисуем круг(мячик)
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    # отображаем мячик на экране
    def display(self):
        self.ball = pygame.draw.circle(
            screen, self.color, (self.posx, self.posy), self.radius)

    # изменяем кординаты мячика, дабы создать иллюзию движения
    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac
        # имитируем отскок
        if self.posx <= 0 or self.posx >= WIDTH:
            self.xFac *= -1
        # имитируем отскок от верхней "стенки"
        if self.posy <= 0 and self.firstTime:
            self.yFac *= -1
        # если мяч попадает в нижнюю "стенку"
        elif self.posy >= HEIGHT and self.firstTime:
            self.firstTime = 0
            return 1
        else:
            return 0

    # имитируем удар об ракетку
    def hit(self, point):
        # чтобы мяч при ударе об боковую стенку ракетки не забогавался
        if point <= 0 or point >= 550:
            self.xFac *= -1

        else:
            self.yFac *= -1
    # имитирование удара об ракетку только для двоих
    def hit2(self):
        self.xFac *= -1

    # восстановление мяча в середине экрана
    def reset(self):
        self.posx = WIDTH // 2
        self.posy = HEIGHT // 2
        self.xFac *= -1
        self.firstTime = 1

    # обновление положения мача
    def update2(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        if self.posy <= 0 or self.posy >= HEIGHT:
            self.yFac *= -1

        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    # получаем кординаты мячика
    def getRect(self):
        return self.ball


# окно после проигрыша
class GameOver(QWidget):
    def __init__(self, name, last_count):
        super().__init__()
        self.name = name
        self.last_count = last_count
        f = io.StringIO(templete_Game_over)
        uic.loadUi(f, self)
        self.setGeometry(760, 240, 400, 600)
        self.setWindowTitle('Игра окончена')
        self.CountLabel.setText(f'Ваш счёт: {self.last_count}')
        self.RestartGameBtn.clicked.connect(self.Restart_Game)
        self.BackToMainMenuBtn.clicked.connect(self.Back_To_Main_Menu)

    # перезапустить игру
    def Restart_Game(self):
        self.close()
        main(name=self.name)

    # вернуться в главное меню
    def Back_To_Main_Menu(self):
        self.close()
        self.a = MainMenu(name=self.name)
        self.a.show()


# получение имени игрока
class GetName(QWidget):
    def __init__(self):
        super().__init__()
        f = io.StringIO(templete_get_name)
        uic.loadUi(f, self)
        self.setGeometry(760, 240, 400, 600)
        self.setWindowTitle('Введите свое имя')
        self.NextBtn.clicked.connect(self.CheckNameInDB)

    # проверка пользователя по имени в базе данных
    def CheckNameInDB(self):
        try:
            # приводим имя пользователя к общему ввиду
            name = ' '.join(self.NameLineEdit.text().lower().split())
            # проверка на то, что имя только из букв
            if ''.join(self.NameLineEdit.text().split()).isalpha():
                with sqlite3.connect('pin-pong.sqlite') as con:
                    cur = con.cursor()
                    # проверка на существование пользователя
                    check = cur.execute(f'''SELECT EXISTS(SELECT * FROM people 
            WHERE name = "{name}")''').fetchall()[0]
                    # если нет, то создаем нового пользователя
                    if check[0] == 0:
                        cur.execute(
                            f'''INSERT INTO people(name, last_count, best_count) 
                        values("{name}", 0, 0)''')
                        con.commit()
                self.close()
                # запускаем главное меню и передаем туда имя пользователя для выкачки следуйщей информации в базе данных
                self.main_menu = MainMenu(name=name)
                self.main_menu.show()
            else:
                self.ErorrLabel.setText('В строке должны быть только буквы!')
        except:
            pass


# главное меню
class MainMenu(QWidget):
    def __init__(self, name):
        super().__init__()
        self.setGeometry(760, 240, 400, 600)
        f = io.StringIO(templete_Main_Menu)
        self.name = name.split()[0].capitalize()
        self.surname = name.split()[1].capitalize()
        uic.loadUi(f, self)
        self.setWindowTitle('Главное меню')
        with sqlite3.connect('pin-pong.sqlite') as con:
            cur = con.cursor()
            # извлекаем счет последней попытки и лучший счет из базы данных и выводим ее на QLabelы
            data_of_people = cur.execute(f'''SELECT * FROM people WHERE name = "{name}"''').fetchall()
        self.WelcomeLineEdit.setText(f'Привет, {self.name} {self.surname}!')
        self.LastCountLineEdit.setText(f'{self.LastCountLineEdit.text()} {data_of_people[0][1]}')
        self.BestCountLineEdit.setText(f'{self.BestCountLineEdit.text()} {data_of_people[0][2]}')
        self.SoloGameBtn.clicked.connect(self.SoloGame)
        self.DuoGameBtn.clicked.connect(self.DuoGame)

    # запускается игра для одного
    def SoloGame(self):
        self.close()
        main(name=f'{self.name.lower()} {self.surname.lower()}')

    # запускается игра для двоих
    def DuoGame(self):
        self.close()
        main2(name=f'{self.name.lower().capitalize()}', surname=f'{self.surname.lower().capitalize()}')


def main(name):
    running = True
    # создаем ракетки и мячик
    racket1 = Racket(150, 550, 100, 10, 15, BLACK)
    racket2 = Racket(100, 0, 200, 10, 15, BLACK)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 10, BLACK)
    # создаем отдельный список ракеток
    listOfRackets = [racket1, racket2]
    # счет и коэффициент на который потом надо будет смещать ракеткку
    racket2Score = 0
    racket1XFac = 0

    while running:
        # заливаем экран белым цветом
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            # перемещенние ракеток клавишами w a s d и сдрелочками
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    racket1XFac = -1
                if event.key == pygame.K_d:
                    racket1XFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    racket1XFac = 0
        # проверяем столкновение ракеток с мячем
        for racket in listOfRackets:
            if pygame.Rect.colliderect(ball.getRect(), racket.getRect()):
                point = ball.getRect()[1]
                # если ракетка верхняя, то начисляем очко
                if racket == racket2:
                    racket2Score += 1
                ball.hit(point)
        # перемещаем ракетку и мяч
        racket1.update(racket1XFac)
        point = ball.update()
        # если мяч попал по нижней стенке, записываем данные в базу данных
        if point:
            with sqlite3.connect('pin-pong.sqlite') as con:
                cur = con.cursor()
                cur.execute(f'''UPDATE people SET last_count = {racket2Score} WHERE name = "{name}"''')
                best_count = cur.execute(f'''SELECT best_count FROM people WHERE name = "{name}"''').fetchone()

                if best_count[0] < racket2Score:
                    cur.execute(f'''UPDATE people SET best_count = {racket2Score} WHERE name = "{name}"''')
            a = GameOver(name=name, last_count=racket2Score)
            a.show()
        # отрисовываем ракетки и мяч
        racket1.display()
        racket2.display()
        ball.display()

        # отображаем счет
        racket2.displayScore('',
                             racket2Score, 200, 300, BLACK)

        pygame.display.update()
        clock.tick(FPS)


# аналогчно функции main()
def main2(name, surname):
    running = True

    racket1 = Racket(20, 0, 10, 100, 15, BLACK)
    racket2 = Racket(WIDTH - 30, 0, 10, 100, 15, BLACK)
    ball = Ball(WIDTH // 2, HEIGHT // 2, 7, 7, BLACK)

    listOfRackets = [racket1, racket2]

    racket1Score, racket2Score = 0, 0
    racket1YFac, racket2YFac = 0, 0

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    racket2YFac = -1
                if event.key == pygame.K_DOWN:
                    racket2YFac = 1
                if event.key == pygame.K_w:
                    racket1YFac = -1
                if event.key == pygame.K_s:
                    racket1YFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    racket2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    racket1YFac = 0

        for geek in listOfRackets:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                point = ball.getRect()[0]
                ball.hit2()

        racket1.update2(racket1YFac)
        racket2.update2(racket2YFac)
        point = ball.update2()

        if point == -1:
            racket1Score += 1
        elif point == 1:
            racket2Score += 1

        if point:
            ball.reset()

        racket1.display()
        racket2.display()
        ball.display()

        racket1.displayScore(f"{name} {surname}: ",
                             racket1Score, 100, 20, BLACK)
        racket2.displayScore("Гость: ",
                             racket2Score, WIDTH - 100, 20, BLACK)

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = GetName()
    ex.show()
    sys.exit(app.exec())
