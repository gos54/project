import pygame


# закончен
class Pixel(pygame.sprite.Sprite):
    def __init__(self,
                 indent_coefficients: tuple[float, float],
                 screen_size: tuple[int, int],
                 size: tuple[int, int],
                 color: tuple[int, int, int]):
        super().__init__()
        self.color = color

        self.image = pygame.Surface(size)

        self.indent_coefficients = self.indent_x, self.indent_y = indent_coefficients
        self.screen_size = self.screen_w, self.screen_h = screen_size
        self.rect = pygame.Rect(int(self.indent_x * self.screen_w - self.image.get_width() // 2),
                                int(self.indent_y * self.screen_h - self.image.get_height() // 2),
                                *self.image.get_size())
        self.update()

    def set_pos(self, new_pos: tuple[int, int]):
        self.rect.update(*new_pos, *self.rect.size)

    def update(self):
        self.image.fill(self.color)

    def is_mouse_inside(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


class BoardImage(pygame.sprite.Sprite):
    def __init__(self,
                 name,
                 indent_coefficients: tuple[float, float],
                 screen_size: tuple[int, int],
                 size_in_cell: tuple[int, int],
                 cell_size: [int, int],
                 *groups,
                 file_name: str | None = None):
        super().__init__(*groups)
        self.name = name
        self.cell_size = cell_size
        self.size_in_cell = size_in_cell

        self.image = pygame.Surface(
            (self.size_in_cell[0] * self.cell_size[0], self.size_in_cell[1] * self.cell_size[1]))

        self.indent_coefficients = self.indent_x, self.indent_y = indent_coefficients
        self.screen_size = self.screen_w, self.screen_h = screen_size
        self.rect = pygame.Rect(int(self.indent_x * self.screen_w - self.image.get_width() // 2),
                                int(self.indent_y * self.screen_h - self.image.get_height() // 2),
                                *self.image.get_size())

        self.board = []
        c_x, c_y = self.cell_size[0] / self.image.get_width(), self.cell_size[1] / self.image.get_height()
        if type(file_name) is str:
            with open(file=file_name, mode="r") as file:
                colors, lines = file.read().split("\n-\n")
            colors = {i[0]: [int(a) for a in i[1].split()] for i in [line.split("|") for line in colors.split("\n")]}
            self.colors = []
            for i in colors:
                self.colors.append(colors[i])
            lines = lines.split("\n")[:-1]
            for i in range(len(lines)):
                self.board.append([])
                for j in range(len(lines[i])):
                    self.board[i].append(Pixel((c_x / 2 + c_x * j,
                                                c_y / 2 + c_y * i),
                                               self.image.get_size(),
                                               self.cell_size,
                                               colors[lines[i][j]]))
        else:
            self.colors = [(0, 0, 0)]
            for i in range(self.size_in_cell[1]):
                self.board.append([])
                for j in range(self.size_in_cell[0]):
                    self.board[i].append(Pixel((c_x / 2 + c_x * j,
                                                c_y / 2 + c_y * i),
                                               self.image.get_size(),
                                               self.cell_size,
                                               (0, 0, 0)))

    def update(self):
        for line in self.board:
            for cell in line:
                cell.update()
                self.image.blit(cell.image, (cell.rect.x, cell.rect.y))

    def check(self, board_class):
        number = len(self.board) * len(self.board[0])

        count = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                c1 = self.board[i][j].color
                c2 = board_class.board[i][j].color
                if c1[0] == c2[0] and c1[1] == c2[1] and c1[2] == c2[2]:
                    count += 1
        return count / number

    def set_indent(self,
                   indent_coefficients: tuple[float, float] | None = None,
                   screen_size: tuple[int, int] | None = None):
        if indent_coefficients is not None:
            self.indent_coefficients = self.indent_x, self.indent_y = indent_coefficients
        if screen_size is not None:
            self.screen_size = self.screen_w, self.screen_h = screen_size
        self.rect.update(int(self.indent_x * self.screen_w - self.image.get_width() // 2),
                         int(self.indent_y * self.screen_h - self.image.get_height() // 2),
                         *self.image.get_size())

    def is_mouse_inside(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


class PaintBoard(BoardImage):
    def __init__(self,
                 name,
                 indent_coefficients: tuple[float, float],
                 screen_size: tuple[int, int],
                 size_in_cell: tuple[int, int],
                 cell_size: [int, int],
                 colors,
                 *groups):
        super().__init__(name, indent_coefficients, screen_size, size_in_cell, cell_size, *groups)
        self.colors = colors
        self.brush_color = self.colors[0]

        self.is_drawing = False
        self.draw_type = "brush"

    def set_brush_color(self, color: tuple[int, int, int]):
        self.brush_color = color

    def set_drawing_type(self, draw_type):
        self.draw_type = draw_type

    def filling(self, cell_pos: tuple[int, int], old_color: tuple[int, int, int]):
        x, y = cell_pos
        if self.brush_color == self.board[y][x].color:
            return
        self.board[y][x].color = self.brush_color
        if y - 1 >= 0:
            if self.board[y - 1][x].color == old_color:
                self.filling((x, y - 1), old_color)
        if y + 1 < self.size_in_cell[1]:
            if self.board[y + 1][x].color == old_color:
                self.filling((x, y + 1), old_color)
        if x - 1 >= 0:
            if self.board[y][x - 1].color == old_color:
                self.filling((x - 1, y), old_color)
        if x + 1 < self.size_in_cell[0]:
            if self.board[y][x + 1].color == old_color:
                self.filling((x + 1, y), old_color)

    def update(self):
        if self.is_drawing:
            cell_pos = self.get_cell_pos()
            if cell_pos is not None:
                if self.draw_type == "brush":
                    self.board[cell_pos[1]][cell_pos[0]].color = self.brush_color
                elif self.draw_type == "fill":
                    self.filling(cell_pos, self.board[cell_pos[1]][cell_pos[0]].color)
                    self.draw_type = "brush"
        self.image.fill((0, 0, 0))
        for line in self.board:
            for cell in line:
                cell.update()
                self.image.blit(cell.image, (cell.rect.x, cell.rect.y))

    def get_cell_pos(self):
        if self.is_mouse_inside():
            mouse_pos = pygame.mouse.get_pos()
            return (mouse_pos[0] - self.rect.x) // self.cell_size[0], (mouse_pos[1] - self.rect.y) // self.cell_size[1]

    def check_click(self, event):
        if not self.is_drawing and event.type == pygame.MOUSEBUTTONDOWN and self.is_mouse_inside():
            self.is_drawing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_drawing = False

    def is_mouse_inside(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())


# закончен
class Text(pygame.sprite.Sprite):
    def __init__(self,
                 name: str,
                 indent_coefficients: tuple[float, float],
                 screen_size: tuple[int, int],
                 text: str,
                 font: pygame.font.Font,
                 color: tuple[int, int, int],
                 *groups):
        super().__init__(*groups)
        self.name = name
        self.indent_coefficients = self.indent_x, self.indent_y = indent_coefficients
        self.screen_size = self.screen_w, self.screen_h = screen_size
        self.text = text
        self.font = font
        self.color = color

        self.image = self.font.render(text, True, self.color)
        self.rect = pygame.Rect(int(self.indent_x * self.screen_w - self.image.get_width() // 2),
                                int(self.indent_y * self.screen_h - self.image.get_height() // 2),
                                *self.image.get_size())

    def update(self):
        self.image = self.font.render(self.text, True, self.color)

    def set_text(self, text):
        self.text = text
        self.image = self.font.render(self.text, True, self.color)
        self.rect.update(int(self.indent_x * self.screen_w - self.image.get_width() // 2),
                         int(self.indent_y * self.screen_h - self.image.get_height() // 2),
                         *self.image.get_size())

    def set_indent(self,
                   indent_coefficients: tuple[float, float] | None = None,
                   screen_size: tuple[int, int] | None = None):
        if indent_coefficients is not None:
            self.indent_coefficients = self.indent_x, self.indent_y = indent_coefficients
        if screen_size is not None:
            self.screen_size = self.screen_w, self.screen_h = screen_size
        self.rect.update(int(self.indent_x * self.screen_w - self.image.get_width() // 2),
                         int(self.indent_y * self.screen_h - self.image.get_height() // 2),
                         *self.image.get_size())


# закончен
class Button(pygame.sprite.Sprite):
    def __init__(self,
                 name: str,
                 indent_coefficients: tuple[float, float],
                 screen_size: tuple[int, int],
                 size: tuple[int, int],
                 click_event: callable,
                 text: str | Text,
                 color: tuple[int, int, int],
                 second_color: tuple[int, int, int],
                 color_clicked: tuple[int, int, int],
                 text_color: tuple[int, int, int],
                 *groups,
                 border_radius=0):
        super().__init__(*groups)
        self.name = name
        self.indent_coefficients = self.indent_x, self.indent_y = indent_coefficients
        self.screen_size = self.screen_w, self.screen_h = screen_size
        self.click_event = click_event
        self.color = color
        self.second_color = second_color
        self.color_clicked = color_clicked

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = pygame.Rect(int(self.indent_x * self.screen_w - self.image.get_width() // 2),
                                int(self.indent_y * self.screen_h - self.image.get_height() // 2),
                                *self.image.get_size())

        if type(text) is str:
            font = pygame.font.Font(None, 25)
            self.text = Text("text_" + self.name, (0.5, 0.5), self.rect.size, text, font, text_color)
        elif type(text) is Text:
            self.text = text
        self.text.set_indent((0.5, 0.5), self.rect.size)
        self.border_radius = border_radius

        self.is_clicked = False

        self.update()

    def check_click(self, event):
        if not self.is_clicked and event.type == pygame.MOUSEBUTTONDOWN and self.is_mouse_inside():
            self.is_clicked = True
        elif self.is_clicked and event.type == pygame.MOUSEBUTTONUP and self.is_mouse_inside():
            self.is_clicked = False
            return self.click_event
        elif self.is_clicked and event.type == pygame.MOUSEBUTTONUP:
            self.is_clicked = False

    def update(self):
        color = self.color
        if self.is_clicked:
            color = self.color_clicked
        elif self.is_mouse_inside():
            color = self.second_color
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, color, (0, 0, *self.image.get_size()), border_radius=self.border_radius)
        self.image.blit(self.text.image, (self.text.rect.x, self.text.rect.y))

    def is_mouse_inside(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def set_indent(self,
                   indent_coefficients: tuple[float, float] | None = None,
                   screen_size: tuple[int, int] | None = None):
        if indent_coefficients is not None:
            self.indent_coefficients = self.indent_x, self.indent_y = indent_coefficients
        if screen_size is not None:
            self.screen_size = self.screen_w, self.screen_h = screen_size
        self.rect.update(int(self.indent_x * self.screen_w - self.image.get_width() // 2),
                         int(self.indent_y * self.screen_h - self.image.get_height() // 2),
                         *self.image.get_size())


# закончен
class Slider(pygame.sprite.Sprite):
    def __init__(self,
                 name: str,
                 indent_coefficients: tuple[float, float],
                 screen_size: tuple[int, int],
                 size: tuple[int, int],
                 min_value: int,
                 max_value: int,
                 value: int,
                 color: tuple[int, int, int],
                 second_color: tuple[int, int, int],
                 background_color: tuple[int, int, int],
                 *groups):
        super().__init__(*groups)
        self.name = name
        self.indent_coefficients = self.indent_x, self.indent_y = indent_coefficients
        self.screen_size = self.screen_w, self.screen_h = screen_size
        self.min_value = min_value
        self.max_value = max_value
        self.value = value
        self.color = color
        self.second_color = second_color
        self.background_color = background_color

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = pygame.Rect(int(self.indent_x * self.screen_w - self.image.get_width() // 2),
                                int(self.indent_y * self.screen_h - self.image.get_height() // 2),
                                *self.image.get_size())

        self.difference = self.max_value - self.min_value
        self.step = self.difference / (self.rect.width - self.rect.height)
        self.is_clicked = False

        self.update()

    def update(self):
        color = self.color
        if self.is_clicked:
            color = self.second_color

        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, self.background_color, (0, 0, *self.image.get_size()),
                         border_radius=self.image.get_height() // 2)
        pygame.draw.circle(
            self.image, color,
            (self.value * (1 / self.step) + (self.rect.width - (self.rect.width - self.rect.height)) // 2,
             self.rect.height // 2),
            self.image.get_height() // 2)

    def check_click(self, event):
        if not self.is_clicked and event.type == pygame.MOUSEBUTTONDOWN and self.is_mouse_inside():
            self.is_clicked = True
            mouse_position = pygame.mouse.get_pos()
            self.value = int((mouse_position[0] - self.rect.x) * (self.difference / self.rect.width))
        elif self.is_clicked and event.type == pygame.MOUSEMOTION:
            mouse_x = pygame.mouse.get_pos()[0]
            if mouse_x - self.rect.x >= self.rect.width:
                self.value = self.max_value
            elif mouse_x - self.rect.x <= 0:
                self.value = self.min_value
            else:
                self.value = int((mouse_x - self.rect.x) * (self.difference / self.rect.width))
        elif self.is_clicked and event.type == pygame.MOUSEBUTTONUP:
            self.is_clicked = False
            return self.value

    def is_mouse_inside(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def set_indent(self,
                   indent_coefficients: tuple[float, float] | None = None,
                   screen_size: tuple[int, int] | None = None):
        if indent_coefficients is not None:
            self.indent_coefficients = self.indent_x, self.indent_y = indent_coefficients
        if screen_size is not None:
            self.screen_size = self.screen_w, self.screen_h = screen_size
        self.rect.update(int(self.indent_x * self.screen_w - self.image.get_width() // 2),
                         int(self.indent_y * self.screen_h - self.image.get_height() // 2),
                         *self.image.get_size())
