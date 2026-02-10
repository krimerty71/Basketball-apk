import kivy
kivy.require('2.1.0')
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Ellipse, Line
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.properties import NumericProperty, StringProperty
import random

# Настройки
Window.clearcolor = (0.9, 0.9, 0.95, 1)

class BasketballGame(Widget):
    score = NumericProperty(0)
    level = NumericProperty(1)
    status = StringProperty("Бросьте мяч!")
    
    def __init__(self):
        super().__init__()
        self.ball_pos = [100, 200]
        self.ball_vel = [0, 0]
        self.basket_pos = [300, 400]
        self.basket_speed = 2
        self.game_active = True
        self.shots = 0
        self.hits = 0
        
        Clock.schedule_interval(self.update, 1.0/60.0)
    
    def throw_ball(self, power=10, angle=45):
        if self.ball_vel == [0, 0] and self.game_active:
            self.shots += 1
            rad = angle * 3.14159 / 180
            self.ball_vel = [
                power * 0.8 * math.cos(rad),
                power * 0.8 * math.sin(rad)
            ]
            self.status = "Мяч летит!"
    
    def update(self, dt):
        if not self.game_active:
            return
        
        # Физика мяча
        self.ball_pos[0] += self.ball_vel[0]
        self.ball_pos[1] += self.ball_vel[1]
        self.ball_vel[1] -= 0.5  # гравитация
        
        # Движение корзины
        self.basket_pos[0] += self.basket_speed
        if self.basket_pos[0] > 400 or self.basket_pos[0] < 200:
            self.basket_speed *= -1
        
        # Проверка попадания
        basket_rect = [self.basket_pos[0]-60, self.basket_pos[1]-10, 120, 20]
        ball_rect = [self.ball_pos[0]-20, self.ball_pos[1]-20, 40, 40]
        
        # Простое столкновение
        if (ball_rect[0] < basket_rect[0] + basket_rect[2] and
            ball_rect[0] + ball_rect[2] > basket_rect[0] and
            ball_rect[1] < basket_rect[1] + basket_rect[3] and
            ball_rect[1] + ball_rect[3] > basket_rect[1]):
            
            if self.ball_vel[1] < 0:  # Падает вниз
                self.score += 100
                self.hits += 1
                self.ball_pos = [100, 200]
                self.ball_vel = [0, 0]
                self.status = "ПОПАДАНИЕ! +100 очков"
                
                # Новый уровень
                if self.score >= self.level * 300:
                    self.level += 1
                    self.basket_speed *= 1.2
                    if self.level > 15:
                        self.game_active = False
                        self.status = "ПОБЕДА! 15 уровней пройдены!"
        
        # Отскок от стен
        if self.ball_pos[0] < 20 or self.ball_pos[0] > 480:
            self.ball_vel[0] *= -1
        
        # Упал на пол
        if self.ball_pos[1] < 30:
            self.ball_pos = [100, 200]
            self.ball_vel = [0, 0]
            self.status = "Промах. Попробуйте снова!"
        
        # Точность
        accuracy = 0
        if self.shots > 0:
            accuracy = (self.hits / self.shots) * 100
        
        # Обновляем графику
        self.canvas.clear()
        self.draw_game(accuracy)
    
    def draw_game(self, accuracy):
        with self.canvas:
            # Фон
            Color(0.95, 0.95, 0.98, 1)
            Rectangle(pos=(0, 0), size=(500, 800))
            
            # Авторская подпись (маленькая, в углу)
            Color(0.3, 0.3, 0.3, 0.3)
            Rectangle(pos=(5, 5), size=(250, 30))
            Color(0.5, 0.5, 0.5, 0.7)
            Line(rectangle=[5, 5, 250, 30], width=1)
            
            # Пол
            Color(0.7, 0.7, 0.7, 1)
            Rectangle(pos=(0, 0), size=(500, 30))
            
            # Оранжевый баскетбольный мяч
            Color(1, 0.5, 0, 1)
            Ellipse(pos=(self.ball_pos[0]-20, self.ball_pos[1]-20), size=(40, 40))
            
            # Черные линии на мяче
            Color(0, 0, 0, 1)
            Line(ellipse=(self.ball_pos[0]-20, self.ball_pos[1]-20, 40, 40), width=2)
            Line(points=[self.ball_pos[0], self.ball_pos[1]-20, 
                        self.ball_pos[0], self.ball_pos[1]+20], width=2)
            
            # Серая корзина с черными полосками
            Color(0.6, 0.6, 0.6, 1)
            Rectangle(pos=(self.basket_pos[0]-60, self.basket_pos[1]-10), size=(120, 20))
            
            # Черные полоски на корзине
            Color(0, 0, 0, 1)
            Line(rectangle=[self.basket_pos[0]-60, self.basket_pos[1]-10, 120, 20], width=2)
            for i in range(1, 4):
                x = self.basket_pos[0]-60 + i*30
                Line(points=[x, self.basket_pos[1]-10, x, self.basket_pos[1]+10], width=2)
            
            # Панель информации
            Color(0.2, 0.2, 0.2, 0.8)
            Rectangle(pos=(300, 650), size=(180, 130))
            Color(1, 1, 1, 1)
            Line(rectangle=[300, 650, 180, 130], width=2)
    
    def on_touch_down(self, touch):
        if touch.y < 200:  # Нижняя часть экрана
            power = min(100, max(10, (touch.x / 500) * 100))
            angle = min(80, max(10, (touch.y / 200) * 80))
            self.throw_ball(power, angle)
        return True

class MyachikApp(App):
    def build(self):
        self.title = "МЯЧИК - Антоха-кодер"
        
        # Создаем игру
        game = BasketballGame()
        
        # Создаем интерфейс
        layout = BoxLayout(orientation='vertical')
        
        # Верхняя панель
        top_panel = BoxLayout(size_hint=(1, 0.1))
        top_panel.add_widget(Label(text=f'Уровень: {game.level}/15', font_size=20))
        top_panel.add_widget(Label(text=f'Счет: {game.score}', font_size=20))
        
        # Статус
        status_label = Label(text=game.status, font_size=18, size_hint=(1, 0.05))
        
        # Кнопки
        buttons = BoxLayout(size_hint=(1, 0.15))
        btn_throw = Button(text='БРОСИТЬ', background_color=(0, 0.7, 0, 1))
        btn_throw.bind(on_press=lambda x: game.throw_ball(
            random.randint(30, 70), 
            random.randint(30, 60)
        ))
        
        btn_reset = Button(text='СБРОС', background_color=(0.8, 0.2, 0, 1))
        btn_reset.bind(on_press=lambda x: (
            setattr(game, 'score', 0),
            setattr(game, 'level', 1),
            setattr(game, 'game_active', True),
            setattr(game, 'basket_speed', 2),
            setattr(game.ball, 'pos', [100, 200]),
            setattr(game.ball, 'vel', [0, 0])
        ))
        
        buttons.add_widget(btn_throw)
        buttons.add_widget(btn_reset)
        
        # Авторская надпись
        author = Label(
            text='Сделано Антоха-кодер\n@AnTOhaKoding',
            font_size=12,
            color=(0.5, 0.5, 0.5, 0.7),
            size_hint=(1, 0.05)
        )
        
        # Собираем все вместе
        layout.add_widget(top_panel)
        layout.add_widget(game)
        layout.add_widget(status_label)
        layout.add_widget(buttons)
        layout.add_widget(author)
        
        # Обновляем статус
        def update_status(dt):
            status_label.text = game.status
        
        Clock.schedule_interval(update_status, 0.5)
        
        return layout

# Глобально импортируем math
import math

if __name__ == "__main__":
    MyachikApp().run()
