import pygame
import sys
from classes import Text, Button, Slider, PaintBoard, BoardImage
from os import listdir
from random import choice

COLORS = {
    "BUTTON_COLOR_1": (165, 90, 195),
    "BUTTON_SECOND_COLOR_1": (195, 110, 215),
    "CLICK_BUTTON_COLOR_1": (95, 60, 125),
    "TEXT_COLOR_1": (60, 90, 110),
    "TEXT_COLOR_2": (255, 130, 255)
}

with open(file="system_files/settings.txt", mode="r", encoding="utf8") as file:
    SETTINGS = {i[0]: i[1] for i in [j.split(":") for j in file.read().split()]}

with open(file="system_files/statistics.txt") as file:
    STATISTICS = {i[0]: i[1] for i in [j.split(":") for j in file.read().split()]}


# функция для прекращения работы программы
def terminate():
    pygame.quit()
    sys.exit()


def save_settings():
    with open(file="system_files/settings.txt", mode="w", encoding="utf8") as file:
        file.write("\n".join([":".join((i, SETTINGS[i])) for i in SETTINGS]))


def save_statistics():
    with open(file="system_files/statistics.txt", mode="w", encoding="utf8") as file:
        file.write("\n".join([":".join((i, STATISTICS[i])) for i in STATISTICS]))


class Window:
    def __init__(self):
        pygame.init()

        # инициализация переменных
        self.b = None
        self.ticks_timer = 0
        self.fps = 60
        self.groups = {"all_sprites": pygame.sprite.Group(),
                       "drawing_sprites": pygame.sprite.Group(),
                       "interactive_sprites": pygame.sprite.Group()}
        self.font = pygame.font.Font(None, 25)
        self.show_scene = None

        self.screen = pygame.display.set_mode([int(i) for i in SETTINGS["screen_size"].split("x")])
        self.clock = pygame.time.Clock()
        self.sound = pygame.mixer.Sound("music/main_menu_theme.mp3")
        self.background = pygame.transform.scale(pygame.image.load("images/backgrounds_images/background1.jpg"),
                                                 self.screen.get_size())

        self.sound.play(-1)
        self.sound.set_volume(int(SETTINGS["music_volume"]) / 100)
        self.init_main_menu()
        self.run()

    def resize(self, size: tuple[int, int]):
        if self.screen.get_size() != size:
            self.screen = pygame.display.set_mode(size)
            self.background = pygame.transform.scale(self.background, size)
            SETTINGS["screen_size"] = "x".join(str(i) for i in size)
            for sprite in self.groups["all_sprites"]:
                sprite.set_indent(screen_size=size)

    def clear_groups(self):
        self.ticks_timer = 0
        self.groups.clear()
        self.groups["all_sprites"] = pygame.sprite.Group()
        self.groups["drawing_sprites"] = pygame.sprite.Group()
        self.groups["interactive_sprites"] = pygame.sprite.Group()

    def init_main_menu(self):
        self.clear_groups()

        button_size = button_w, button_h = 150, 40
        c_w, c_h = 0.5, 0.11
        button_b_r = button_h // 3

        Text("text",
             (c_w, c_h),
             self.screen.get_size(),
             "Главное меню",
             self.font,
             COLORS["TEXT_COLOR_2"],
             self.groups["all_sprites"],
             self.groups["drawing_sprites"])

        Button("game_menu_button",
               (c_w, c_h * 2),
               self.screen.get_size(),
               button_size,
               self.init_game_menu,
               "Играть",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        Button("settings_menu_button",
               (c_w, c_h * 3),
               self.screen.get_size(),
               button_size,
               self.init_settings_menu,
               "Настройки",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        Button("exit_button",
               (c_w, c_h * 4),
               self.screen.get_size(),
               button_size,
               terminate,
               "Выйти",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        self.show_scene = self.main_menu

    def init_game_menu(self):
        self.clear_groups()

        button_size = button_w, button_h = 150, 40
        c_w, c_w_2, c_h = 0.5, 0.25, 0.15
        button_b_r = button_h // 3

        Text("text_1",
             (c_w, c_h),
             self.screen.get_size(),
             "Игровое меню",
             self.font,
             COLORS["TEXT_COLOR_2"],
             self.groups["all_sprites"],
             self.groups["drawing_sprites"])

        Button("main_menu_button",
               (c_w, c_h * 2),
               self.screen.get_size(),
               button_size,
               self.init_main_menu,
               "Главное меню",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        Button("statistics_button",
               (c_w, c_h * 3),
               self.screen.get_size(),
               button_size,
               self.init_statistics,
               "Статистика",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        Text("text_2",
             (c_w, c_h * 4),
             self.screen.get_size(),
             "Выберите уровень сложности",
             self.font,
             COLORS["TEXT_COLOR_2"],
             self.groups["all_sprites"],
             self.groups["drawing_sprites"],
             self.groups["interactive_sprites"])

        Button("button_1",
               (c_w_2, c_h * 5),
               self.screen.get_size(),
               button_size,
               lambda: self.init_level(1),
               "Уровень 1",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        Button("button_2",
               (c_w_2 * 2, c_h * 5),
               self.screen.get_size(),
               button_size,
               lambda: self.init_level(2),
               "Уровень 2",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        Button("button_3",
               (c_w_2 * 3, c_h * 5),
               self.screen.get_size(),
               button_size,
               lambda: self.init_level(3),
               "Уровень 3",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        self.show_scene = self.game_menu

    def init_settings_menu(self):
        self.clear_groups()

        button_size = button_w, button_h = 150, 40
        c_w, c_w_2, c_h = 0.5, 0.25, 0.1
        button_b_r = button_h // 3

        Text("text_1",
             (c_w, c_h),
             self.screen.get_size(),
             "Настройки",
             self.font,
             COLORS["TEXT_COLOR_2"],
             self.groups["all_sprites"],
             self.groups["drawing_sprites"],
             self.groups["interactive_sprites"])

        Button("button_main_menu",
               (c_w, c_h * 2),
               self.screen.get_size(),
               button_size,
               self.init_main_menu,
               "Главное меню",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        Text("text_2",
             (c_w, c_h * 3),
             self.screen.get_size(),
             "Разрешение экрана",
             self.font,
             COLORS["TEXT_COLOR_2"],
             self.groups["all_sprites"],
             self.groups["drawing_sprites"],
             self.groups["interactive_sprites"])

        Button("button_1",
               (c_w_2, c_h * 4),
               self.screen.get_size(),
               button_size,
               lambda: self.resize((1440, 900)),
               "1440x900",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        Button("button_2",
               (c_w_2 * 2, c_h * 4),
               self.screen.get_size(),
               button_size,
               lambda: self.resize((1024, 768)),
               "1024x768",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        Button("button_3",
               (c_w_2 * 3, c_h * 4),
               self.screen.get_size(),
               button_size,
               lambda: self.resize((800, 600)),
               "800x600",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        Text("text_2",
             (c_w, c_h * 5),
             self.screen.get_size(),
             "Изменить громкость",
             self.font,
             COLORS["TEXT_COLOR_2"],
             self.groups["all_sprites"],
             self.groups["drawing_sprites"])

        Slider("volume_slider",
               (c_w, c_h * 6),
               self.screen.get_size(),
               (300, 40),
               0,
               100,
               int(SETTINGS["music_volume"]),
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               (255, 255, 255),
               self.groups["all_sprites"],
               self.groups["drawing_sprites"])

        Button("save_button",
               (c_w, c_h * 7),
               self.screen.get_size(),
               button_size,
               save_settings,
               "Сохранить",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        self.show_scene = self.settings_menu

    def init_level(self, level):
        if level == 1:
            file_name = "images/10/" + choice(listdir("images/10"))
            size = 10, 10
        elif level == 2:
            file_name = "images/20/" + choice(listdir("images/20"))
            size = 20, 20
        elif level == 3:
            file_name = "images/30/" + choice(listdir("images/30"))
            size = 30, 30

        self.clear_groups()

        Text("time_text",
             (0.5, 0.9),
             self.screen.get_size(),
             "",
             self.font,
             COLORS["TEXT_COLOR_2"],
             self.groups["all_sprites"],
             self.groups["drawing_sprites"])

        colors = BoardImage("board_image",
                            (0.5, 0.5),
                            self.screen.get_size(),
                            size,
                            (15, 15),
                            self.groups["all_sprites"],
                            self.groups["drawing_sprites"],
                            self.groups["interactive_sprites"],
                            file_name=file_name).colors

        self.ticks_timer = self.fps * 20 * level

        button_size = button_w, button_h = 150, 40
        c_x, c_x_2, c_y, c_y_2 = 0.5, 0.8, 0.5, 1 / ((len(colors) + 1) * 2)
        button_b_r = button_h // 3

        Button("game_menu_button",
               (c_x, 0.06),
               self.screen.get_size(),
               button_size,
               lambda: self.check(level),
               "Завершить",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        PaintBoard("paint_board",
                   (c_x, c_y),
                   self.screen.get_size(),
                   size,
                   (15, 15),
                   colors,
                   self.groups["all_sprites"])

        for i in range(len(colors)):
            Button("b" + str(i + 1),
                   (c_x_2, c_y_2 * (i + 1)),
                   self.screen.get_size(),
                   button_size,
                   self.change_color(colors[i]),
                   "Цвет " + str(i + 1),
                   colors[i],
                   colors[i],
                   colors[i],
                   COLORS["TEXT_COLOR_2"],
                   self.groups["all_sprites"],
                   border_radius=button_b_r)

        Button("button_" + str(i + 2),
               (c_x_2, c_y_2 * (i + 2)),
               self.screen.get_size(),
               button_size,
               self.change_brush("fill"),
               "Заполнить",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               border_radius=button_b_r)

        self.show_scene = lambda: self.show_image(level)

    def init_statistics(self):
        self.clear_groups()
        c_x, c_y = 0.5, 0.10
        button_size = 150, 40
        button_b_r = button_size[1] // 3

        Button("button_game_menu",
               (c_x, c_y),
               self.screen.get_size(),
               button_size,
               self.init_game_menu,
               "Игровое меню",
               COLORS["BUTTON_COLOR_1"],
               COLORS["BUTTON_SECOND_COLOR_1"],
               COLORS["CLICK_BUTTON_COLOR_1"],
               COLORS["TEXT_COLOR_1"],
               self.groups["all_sprites"],
               self.groups["drawing_sprites"],
               self.groups["interactive_sprites"],
               border_radius=button_b_r)

        Text("T1",
             (c_x, c_y * 4),
             self.screen.get_size(),
             "Пройдено 1-ых уровней: " + STATISTICS["levels1"],
             self.font,
             COLORS["TEXT_COLOR_2"],
             self.groups["all_sprites"],
             self.groups["drawing_sprites"])

        Text("T2",
             (c_x, c_y * 5),
             self.screen.get_size(),
             "Пройдено 2-ых уровней: " + STATISTICS["levels2"],
             self.font,
             COLORS["TEXT_COLOR_2"],
             self.groups["all_sprites"],
             self.groups["drawing_sprites"])

        Text("T3",
             (c_x, c_y * 6),
             self.screen.get_size(),
             "Пройдено 3-их уровней: " + STATISTICS["levels3"],
             self.font,
             COLORS["TEXT_COLOR_2"],
             self.groups["all_sprites"],
             self.groups["drawing_sprites"])

        Text("T4",
             (c_x, c_y * 7),
             self.screen.get_size(),
             "Пройдено сего уровней: " + STATISTICS["levels1"],
             self.font,
             COLORS["TEXT_COLOR_2"],
             self.groups["all_sprites"],
             self.groups["drawing_sprites"])

        self.show_scene = self.statistics

    def main_menu(self):
        click_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or (
                    event.type == pygame.MOUSEBUTTONUP):
                for sprite in self.groups["interactive_sprites"]:
                    if type(sprite) is Button:
                        button_event = sprite.check_click(event)
                        if callable(button_event):
                            click_events.append(button_event)
        self.groups["all_sprites"].update()
        self.screen.blit(self.background, (0, 0))
        self.groups["drawing_sprites"].draw(self.screen)
        pygame.display.flip()
        for event in click_events:
            event()
        self.clock.tick(self.fps)

    def game_menu(self):
        click_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or (
                    event.type == pygame.MOUSEBUTTONUP):
                for sprite in self.groups["interactive_sprites"]:
                    if type(sprite) is Button:
                        button_event = sprite.check_click(event)
                        if callable(button_event):
                            click_events.append(button_event)
                    if type(sprite) is Slider:
                        sprite.check_click(event)
                        if sprite.name == "volume_slider":
                            SETTINGS["music_volume"] = str(sprite.value)
                            self.sound.set_volume(sprite.value / 100)
        self.groups["all_sprites"].update()
        self.screen.blit(self.background, (0, 0))
        self.groups["drawing_sprites"].draw(self.screen)
        pygame.display.flip()
        for event in click_events:
            event()
        self.clock.tick(self.fps)

    def show_image(self, level):
        click_events = []
        if self.ticks_timer <= 0:
            for sprite in self.groups["all_sprites"]:
                if sprite not in self.groups["drawing_sprites"]:
                    if type(sprite) is not Text:
                        self.groups["drawing_sprites"].add(sprite)
                        self.groups["interactive_sprites"].add(sprite)
            for sprite in self.groups["drawing_sprites"]:
                if sprite.name == "board_image":
                    self.groups["drawing_sprites"].remove(sprite)
            self.ticks_timer = self.fps * 90 * level
            self.show_scene = lambda: self.level(level)
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            for sprite in self.groups["interactive_sprites"]:
                if type(sprite) is Button:
                    button_event = sprite.check_click(event)
                    if callable(button_event):
                        click_events.append(button_event)
        for sprite in self.groups["drawing_sprites"]:
            if sprite.name == "time_text":
                sprite.set_text("У вас осталось " + str(self.ticks_timer // self.fps) + " с.")
        self.groups["all_sprites"].update()
        self.screen.blit(self.background, (0, 0))
        self.groups["drawing_sprites"].draw(self.screen)
        pygame.display.flip()
        for event in click_events:
            event()
        self.ticks_timer -= 1
        self.clock.tick(self.fps)

    def level(self, level):
        click_events = []
        if self.ticks_timer <= 0:
            self.check(level)
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or (
                    event.type == pygame.MOUSEBUTTONUP):
                for sprite in self.groups["interactive_sprites"]:
                    if type(sprite) is Button:
                        button_event = sprite.check_click(event)
                        if callable(button_event):
                            click_events.append(button_event)
                    elif type(sprite) is PaintBoard:
                        sprite.check_click(event)
        for sprite in self.groups["all_sprites"]:
            if type(sprite) is Text:
                if sprite.name == "time_text":
                    sprite.set_text("У вас осталось " + str(self.ticks_timer // self.fps) + " с.")
        self.groups["all_sprites"].update()
        self.screen.blit(self.background, (0, 0))
        self.groups["drawing_sprites"].draw(self.screen)
        pygame.display.flip()
        for event in click_events:
            event()
        self.ticks_timer -= 1
        self.clock.tick(self.fps)

    def settings_menu(self):
        click_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or (
                    event.type == pygame.MOUSEBUTTONUP):
                for sprite in self.groups["interactive_sprites"]:
                    if type(sprite) is Button:
                        button_event = sprite.check_click(event)
                        if callable(button_event):
                            click_events.append(button_event)
                    if type(sprite) is Slider:
                        sprite.check_click(event)
                        if sprite.name == "volume_slider":
                            SETTINGS["music_volume"] = str(sprite.value)
                            self.sound.set_volume(sprite.value / 100)
        self.groups["all_sprites"].update()
        self.screen.blit(self.background, (0, 0))
        self.groups["drawing_sprites"].draw(self.screen)
        pygame.display.flip()
        for event in click_events:
            event()
        self.clock.tick(self.fps)

    def statistics(self):
        click_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEMOTION or (
                    event.type == pygame.MOUSEBUTTONUP):
                for sprite in self.groups["interactive_sprites"]:
                    if type(sprite) is Button:
                        button_event = sprite.check_click(event)
                        if callable(button_event):
                            click_events.append(button_event)
        self.groups["all_sprites"].update()
        self.screen.blit(self.background, (0, 0))
        self.groups["drawing_sprites"].draw(self.screen)
        pygame.display.flip()
        for event in click_events:
            event()
        self.clock.tick(self.fps)

    def run(self):
        while True:
            if self.show_scene is not None:
                self.show_scene()
            else:
                terminate()

    def change_color(self, color):
        for sprite in self.groups["all_sprites"]:
            if sprite.name == "paint_board":
                return lambda: sprite.set_brush_color(color)

    def change_brush(self, type_name):
        for sprite in self.groups["all_sprites"]:
            if sprite.name == "paint_board":
                return lambda: sprite.set_drawing_type(type_name)

    def check(self, level):
        for sprite in self.groups["all_sprites"]:
            if sprite.name == "paint_board":
                paint_board = sprite
            elif sprite.name == "board_image":
                image_board = sprite
        if image_board.check(paint_board) >= 0.6:
            STATISTICS["levels" + str(level)] = str(int(STATISTICS["levels" + str(level)]) + 1)
            STATISTICS["all_levels"] = str(int(STATISTICS["all_levels"]) + 1)
            save_statistics()
        self.init_statistics()
