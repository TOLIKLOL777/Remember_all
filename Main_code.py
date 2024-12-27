import random
import pygame, sys
from pygame.locals import QUIT

pygame.init()

# Настройка окна
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Remember all')

# Обработка картинок
start_img = pygame.image.load('img/start_img.png')
start_img = pygame.transform.scale(start_img, (366, 79))

exit_img = pygame.image.load('img/exit_img.png')
exit_img = pygame.transform.scale(exit_img, (366, 79))

setting_img = pygame.image.load('img/set_img.png')
setting_img = pygame.transform.scale(setting_img, (366, 79))

menu_img = pygame.image.load('img/menu_btn_img.png')
menu_img = pygame.transform.scale(menu_img, (366, 79))

back_img = pygame.image.load('img/back_img.png')
back_img = pygame.transform.scale(back_img, (223, 79))

sound_img = pygame.image.load('img/Group 72.png')
sound_img = pygame.transform.scale(sound_img, (223, 79))

game_img = pygame.image.load('img/Group 7.png')
game_img = pygame.transform.scale(game_img, (223, 79))

bg_img = pygame.image.load('img/bg_image.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))

blank = pygame.image.load('img/blank.png')
blank = pygame.transform.scale(blank, (158, 220))

tr_opt = pygame.image.load('img/True_opt.png')
tr_opt = pygame.transform.scale(tr_opt, (100, 100))

fl_opt = pygame.image.load('img/False_opt.png')
fl_opt = pygame.transform.scale(fl_opt, (100, 100))

shadow = pygame.image.load('img/shadow.png')
shadow = pygame.transform.scale(shadow, (screen_width, screen_height))
shadow.set_alpha(200)

menu_bg = pygame.image.load('img/Frame 9.png')
menu_bg = pygame.transform.scale(menu_bg, (screen_width, screen_height))

setting_menu_img = pygame.image.load('img/Frame 19.png')
setting_menu_img = pygame.transform.scale(setting_menu_img, (720, screen_height))

card_images = []
for i in range(1,17):  # Добавляем 16 карт
    card_images.append(pygame.transform.scale(pygame.image.load(f'img/{i}_img.png'), (158, 220)))

# Цвета
NEON_BLUE = (173, 216, 230)

# Настройки
button_sound = pygame.mixer.Sound('sfx/button_click.mp3')
card_sound = pygame.mixer.Sound('sfx/card_click.mp3')
menu_music = pygame.mixer.Sound('sfx/Kyodai.mp3')
gameover_music = pygame.mixer.Sound('sfx/Endless.mp3')
game_music1 = ('sfx/Forever.mp3')
game_music2 = ('sfx/Timeless.mp3')
game_music3 = ('sfx/Mayaku.mp3')
music_list = [game_music1,game_music2,game_music3]
game_music = random.choice(music_list)
pygame.mixer.music.load(random.choice(music_list))

Font = pygame.font.Font('fonts/floydiancyr.ttf', 50)
setting_font = pygame.font.Font('fonts/Daneehand Regular Cyr.ttf', 70)
setting_font2 = pygame.font.Font('fonts/Daneehand Regular Cyr.ttf', 60)
gameover_font = pygame.font.Font('fonts/Daneehand Regular Cyr.ttf', 100)

clock = pygame.time.Clock()
FPS = 30
timer = FPS
timer_count = 1

sound_on = True
music_on = True
timer_run = False
main_menu = True
run = True
pause = False
game_over = False
setting_menu = False
setting_menu2 = False

card_width = 158  # Размер карт
card_height = 220
grid_width = 4  # Сетка 4x4
grid_height = 4  # Сетка 4x4
x_correct = -200
y_correct = 100
padding_x = (screen_width+x_correct - (card_width * grid_width)) // (grid_width + 1)
padding_y = (screen_height-y_correct - (card_height * grid_height)) // (grid_height + 1)

# Переменные игры
flipped_cards = []
score = 0
combo = 1
multiplier = 1
moves_limit = 0
mov_lim = False
time_limit = False
hard_mode = False
moves = 0
level = 1
max_combo = 0
delay_check = True
matched_pairs = 0
flip_delay_frames = FPS
flip_delay_counter = 0
delay_counter = 0
is_waiting_for_flip = False
clicking = False

# Классы-----------------------------------------------------------------------------------------------------------
class Card:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hidden = True  # Изначально все карты скрыты
        self.flipped = False
        self.locked = False  # Флаг для блокировки карты (если она неправильно перевернута)

    def draw(self):
        if self.hidden:
            screen.blit(blank, (self.rect.x, self.rect.y))
        else:
            screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self):
        global flipped_cards, matched_pairs, flip_delay_counter, is_waiting_for_flip, clicking, score, combo, moves_limit, max_combo, multiplier

        if not game_over and not pause:
            if self.locked:
                return

            mouse_x, mouse_y = pygame.mouse.get_pos()

            if self.rect.collidepoint(mouse_x, mouse_y):
                if pygame.mouse.get_pressed()[0] == 1 and not clicking:
                    clicking = True
                    if not self.flipped and not is_waiting_for_flip:
                        if sound_on:
                            card_sound.play()
                        self.flipped = True
                        self.hidden = False
                        flipped_cards.append(self)

            if len(flipped_cards) == 2:
                if flipped_cards[0].image == flipped_cards[1].image:
                    matched_pairs += 1
                    score = score + (combo*1*multiplier)
                    combo += 1
                    moves_limit -= 1
                    if combo > max_combo:
                        max_combo = combo
                    flipped_cards.clear()
                else:
                    if flip_delay_counter == 0:
                        combo = 1
                        moves_limit -= 1
                        flip_delay_counter = flip_delay_frames + (FPS*6)
                        is_waiting_for_flip = True
                        for card in flipped_cards:
                            card.locked = True

            # Если задержка завершена, переворачиваем карты обратно
            if flip_delay_counter > 0:
                flip_delay_counter -= 1
                if flip_delay_counter == 0:
                    for card in flipped_cards:
                        card.flipped = False
                        card.hidden = True
                        card.locked = False  # Разблокируем карты
                    flipped_cards.clear()
                    is_waiting_for_flip = False  # Разрешаем ввод

            # Проверка, если кнопка мыши отпущена, сбрасываем флаг
            if pygame.mouse.get_pressed()[0] == 0:
                clicking = False

class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        global clicking
        action = False
        # Получение позиции мыши
        pos = pygame.mouse.get_pos()

        # Проверка условий наведения и нажатия
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked and not clicking:
                if sound_on:
                    button_sound.play()
                action = True
                self.clicked = True
                clicking = True

        if pygame.mouse.get_pressed()[0] == 0:
            clicking = False
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action

# Создание кнопок
start_button = Button(screen_width // 2, screen_height // 2, start_img)
setting_button = Button(screen_width // 2, screen_height // 2 + 100, setting_img)
exit_button = Button(screen_width // 2, screen_height // 2 + 200, exit_img)
menu_button = Button(screen_width // 2, screen_height // 2 + 200, menu_img)
tr_fl_opt_button_1 = Button(screen_width // 2+200, screen_height - 700, fl_opt)
tr_fl_opt_button_2 = Button(screen_width // 2+200, screen_height - 550, fl_opt)
tr_fl_opt_button_3 = Button(screen_width // 2+200, screen_height - 400, fl_opt)
tr_fl_opt_button_4 = Button(screen_width // 2+200, screen_height - 700, tr_opt)
tr_fl_opt_button_5 = Button(screen_width // 2+200, screen_height - 550, tr_opt)
back_button = Button(screen_width // 2+800, screen_height - 1020, back_img)
back_button2 = Button(screen_width // 2+800, screen_height - 920, sound_img)

# Создание списка карт
cards = []

def display_option():
    global level, score, moves_limit, time_limit, combo
    if not time_limit:
        screen.blit(Font.render(f'Раунд {level}', True, (0, 0, 0)),(screen_width // 2 - 310, screen_height // 2 - 485))
        screen.blit(Font.render(f'Счет {score}', True, (0, 0, 0)), (screen_width // 2 + 30, screen_height // 2 - 485))
        if mov_lim:
            screen.blit(Font.render(f'Ходов осталось {moves_limit}', True, (0, 0, 0)), (screen_width // 2 + 290, screen_height // 2 - 485))
        else:
            screen.blit(Font.render(f'Комбо {combo-1}', True, (0, 0, 0)),(screen_width // 2 + 370, screen_height // 2 - 485))
    else:
        screen.blit(Font.render(f'Раунд {level}', True, (0, 0, 0)),(screen_width // 2 - 210, screen_height // 2 - 485))
        screen.blit(Font.render(f'Счет {score}', True, (0, 0, 0)), (screen_width // 2 + 90, screen_height // 2 - 485))
        if mov_lim:
            screen.blit(Font.render(f'Ходов осталось {moves_limit}', True, (0, 0, 0)),(screen_width // 2 + 390, screen_height // 2 - 485))
        else:
            screen.blit(Font.render(f'Комбо {combo-1}', True, (0, 0, 0)),(screen_width // 2 + 440, screen_height // 2 - 485))

def start_new_round():
    global cards, flip_delay_counter, matched_pairs, delay_check, timer_count, moves_limit
    cards = []
    flip_delay_counter = 0
    create_cards()
    matched_pairs = 0
    delay_check = True
    flipped_cards.clear()
    if time_limit:
        timer_count = 60
    if mov_lim:
        if hard_mode:
            moves_limit = 35
        else:
            moves_limit = 25
    else:
        moves_limit = 0

def create_cards():
    global cards, card_images
    card_images_copy = card_images.copy()  # Копируем, чтобы не изменить исходный список карт
    random.shuffle(card_images_copy)

    if grid_width == 4 and grid_height == 4:
        card_images_copy = card_images_copy[:8] * 2  # 8 карт, которые дублируются
    elif grid_width == 6 and grid_height == 4:
        card_images_copy = card_images_copy[:12] * 2  # 12 карт, которые дублируются
    elif grid_width == 4 and grid_height == 6:
        card_images_copy = card_images_copy[:12] * 2  # 12 карт, которые дублируются
    elif grid_width == 6 and grid_height == 6:
        card_images_copy = card_images_copy[:18] * 2  # 18 карт, которые дублируются

    random.shuffle(card_images_copy)

    # Генерация карт с учетом ширины и высоты
    for i in range(grid_height):
        for j in range(grid_width):
            x = (padding_x * (j + 1)) + (card_width * j)
            y = (padding_y * (i + 1)) + (card_height * i)
            card = Card(x - (x_correct // 2), y + y_correct, card_images_copy.pop())
            cards.append(card)

menu_music.play()
while run:
    clock.tick(FPS)
    screen.blit(menu_bg,(0,0))
    if main_menu and not setting_menu:
        if start_button.draw():
            pygame.mixer.music.load(random.choice(music_list))
            main_menu = False
            score = 0
            timer_count = 0
            combo = 1
            level = 1
            moves = 0
            clicking = True
            pause = False
            timer_run = True
            is_waiting_for_flip = False
            menu_music.stop()
            if music_on:
                pygame.mixer.music.play()
            start_new_round()
        if exit_button.draw():
            run = False
        if setting_button.draw():
            setting_menu = True
    elif not main_menu and not setting_menu:
        screen.blit(bg_img, (0, 0))
        display_option()
        for card in cards:
            card.draw()  # Отображаем карту
            card.update()  # Обновляем состояние карты каждый кадр
    if setting_menu and not setting_menu2:
        screen.blit(shadow, (0, 0))
        screen.blit(setting_menu_img, (screen_width//2-360, 0))
        if multiplier % 1 == 0:
            multiplier = int(multiplier)
        screen.blit(setting_font.render('Настройка сложности игры', True, (0, 0, 0)),(screen_width // 2 - 335, 80))
        screen.blit(setting_font2.render(f'Множитель очков {multiplier}', True, (0, 0, 0)),(screen_width // 2 - 200, screen_height - 200))
        screen.blit(setting_font2.render('Лимит времени', True, (0, 0, 0)),(screen_width // 2 - 250, screen_height - 675))
        screen.blit(setting_font2.render('Лимит ходов', True, (0, 0, 0)), (screen_width // 2 - 250, screen_height - 520))
        screen.blit(setting_font2.render('Режим 4х6', True, (0, 0, 0)), (screen_width // 2 - 250, screen_height - 375))
        if back_button.draw() and back_button.image == back_img:
            setting_menu = False
        if back_button2.draw():
            back_button2.image = game_img
            setting_menu2 = True
            continue
        if tr_fl_opt_button_1.draw():
            if tr_fl_opt_button_1.image == fl_opt:
                tr_fl_opt_button_1.image = tr_opt
                time_limit = True
                multiplier += 0.5
                continue
            if tr_fl_opt_button_1.image == tr_opt:
                time_limit = False
                multiplier -= 0.5
                tr_fl_opt_button_1.image = fl_opt
        if tr_fl_opt_button_2.draw():
            if tr_fl_opt_button_2.image == fl_opt:
                mov_lim = True
                tr_fl_opt_button_2.image = tr_opt
                multiplier += 0.5
                continue
            if tr_fl_opt_button_2.image == tr_opt:
                mov_lim = False
                multiplier -= 0.5
                tr_fl_opt_button_2.image = fl_opt
        if tr_fl_opt_button_3.draw():
            if tr_fl_opt_button_3.image == fl_opt:
                grid_width = 6
                grid_height = 4
                multiplier += 1
                hard_mode = True
                padding_x = (screen_width + x_correct - (card_width * grid_width)) // (grid_width + 1)
                padding_y = (screen_height - y_correct - (card_height * grid_height)) // (grid_height + 1)
                tr_fl_opt_button_3.image = tr_opt
                continue
            if tr_fl_opt_button_3.image == tr_opt:
                hard_mode = False
                grid_width = 4
                grid_height = 4
                multiplier -= 1
                padding_x = (screen_width + x_correct - (card_width * grid_width)) // (grid_width + 1)
                padding_y = (screen_height - y_correct - (card_height * grid_height)) // (grid_height + 1)
                tr_fl_opt_button_3.image = fl_opt

    if setting_menu2:
        screen.blit(shadow, (0, 0))
        screen.blit(setting_menu_img, (screen_width // 2 - 360, 0))
        screen.blit(setting_font.render('Настройка звуков и музыки', True, (0, 0, 0)), (screen_width // 2 - 350, 80))
        screen.blit(setting_font2.render('Музыка', True, (0, 0, 0)),
                    (screen_width // 2 - 250, screen_height - 675))
        screen.blit(setting_font2.render('Звуки', True, (0, 0, 0)),
                    (screen_width // 2 - 250, screen_height - 520))
        if back_button.draw() and back_button.image == back_img:
            setting_menu = False
            setting_menu2 = False
        if back_button2.draw():
            back_button2.image = sound_img
            setting_menu2 = False
        if tr_fl_opt_button_4.draw():
            if tr_fl_opt_button_4.image == fl_opt:
                tr_fl_opt_button_4.image = tr_opt
                music_on = True
                menu_music.play()
                continue
            if tr_fl_opt_button_4.image == tr_opt:
                music_on = False
                menu_music.stop()
                tr_fl_opt_button_4.image = fl_opt
        if tr_fl_opt_button_5.draw():
            if tr_fl_opt_button_5.image == fl_opt:
                sound_on = True
                tr_fl_opt_button_5.image = tr_opt
                continue
            if tr_fl_opt_button_5.image == tr_opt:
                sound_on = False
                tr_fl_opt_button_5.image = fl_opt
    if timer_run and not time_limit:
        if not game_over and not pause:
            timer -= 1
        if timer == 0:
            if delay_check:
                timer_count += 1
            timer = FPS
        screen.blit(Font.render(f'Время {timer_count}', True, (0, 0, 0)), (screen_width//2 - 640, screen_height//2-485))
    elif time_limit and timer_run:
        if not game_over and not pause:
            timer -= 1
        if timer == 0:
            if delay_check:
                timer_count -= 1
            timer = FPS
        screen.blit(Font.render(f'Времени осталось {timer_count}', True, (0, 0, 0)),(screen_width // 2 - 800, screen_height // 2 - 485))


    if (matched_pairs == 8 and not hard_mode) or (matched_pairs == 12 and hard_mode):
        if delay_check:
            delay_counter = FPS * 3
            delay_check = False
            timer_run = True
        if delay_counter > 0:
            if not pause:
                delay_counter -= 1
            if delay_counter == 0:
                level += 1
                start_new_round()

    if not main_menu and not setting_menu and not game_over:
        if time_limit and timer_count == 0:
            if music_on:
                gameover_music.play()
            game_over = True
        if moves_limit == 0 and mov_lim:
            if music_on:
                gameover_music.play()
            game_over = True
    if game_over:
        pygame.mixer.music.stop()
        screen.blit(shadow,(0,0))
        game_over_text = gameover_font.render('Игра окончена', True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 300))
        screen.blit(game_over_text,game_over_text_rect)
        game_over_text = setting_font.render(f'Итоговый счет {score}', True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 150))
        screen.blit(game_over_text, game_over_text_rect)
        game_over_text = setting_font.render(f'Максимальное комбо {max_combo}', True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        screen.blit(game_over_text, game_over_text_rect)
        game_over_text = setting_font.render(f'Пройдено раундов {level-1}', True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(game_over_text, game_over_text_rect)
        if menu_button.draw():
            gameover_music.stop()
            if music_on:
                menu_music.play()
            main_menu = True
            game_over = False
            timer_run = False

    if pause:
        pygame.mixer.music.pause()
        screen.blit(shadow, (0, 0))
        game_over_text = gameover_font.render('Игра приостановлена', True, (255, 255, 255))
        game_over_text_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 100))
        screen.blit(game_over_text, game_over_text_rect)
        if menu_button.draw():
            pygame.mixer.music.stop()
            if music_on:
                menu_music.play()
            main_menu = True
            pause = False
            timer_run = False
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE  and not game_over and not main_menu and not setting_menu:
                if pause:
                    pause = False
                    pygame.mixer.music.unpause()
                    continue
                pause = True
    pygame.display.update()

pygame.quit()
sys.exit()
