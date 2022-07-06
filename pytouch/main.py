from random import choice

import pyxel as px

from elements import Score, Circle, ReachCircle
from constants import Screen, State
from colors import select_colors, DEFUALT_COLORS
from settings import Settings
from menu import Menu



class Game:
    def __init__(self):
        px.init(Screen.width, Screen.height, quit_key=False)
        px.mouse(True)

        self._init_colors()
        self.colors = DEFUALT_COLORS
        self.current_color = 0

        self.state = State.MENU
        self.menu = Menu()
        self.settings = Settings()
        self.colors = select_colors()
        self.circ = Circle()
        self.reach_circ = ReachCircle()
        self.score = Score()

        px.run(self._update, self._draw)

    def _init_colors(self):
        px.colors[14] = px.colors[1]
        px.colors[15] = px.colors[7]

    def _update_colors(self):
        px.colors[0] = self.colors[self.current_color].bg
        px.colors[1] = self.colors[self.current_color].user_circ
        px.colors[2] = self.colors[self.current_color].reach_circ
        self.current_color = choice(tuple(filter(lambda color: color != self.current_color, range(len(self.colors)))))

    def _process_keys(self):
        if px.btnp(px.KEY_ESCAPE):
            self.state = State.MENU
            px.mouse(True)

        if px.btnp(px.MOUSE_BUTTON_LEFT) or px.btnp(px.KEY_SPACE):
            if self.reach_circ.is_collided_with_circ(self.circ):
                self.score.score += 1

            self._update_colors()
            self.reach_circ.respawn()
            self.circ.r = 0

    def _update(self):
        self.menu.update(self)
        self._process_keys()
        self.circ.r += 1

    def _draw(self):
        match self.state:
            case State.MENU:
                self.menu.draw()
            case State.PLAY:
                px.cls(Screen.bg)
                self.reach_circ.draw()
                self.circ.draw(px.mouse_x, px.mouse_y)
                self.score.draw()
            case State.SETTINGS:
                self.settings.process()
                self.settings.draw()


if __name__ == '__main__':
    Game()
