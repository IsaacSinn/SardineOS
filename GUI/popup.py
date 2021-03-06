import pygame
from pubsub import pub
from label import Label
import time


class ProfilePopup:
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.set_colorkey((1, 1, 1))
        self.x = 100
        self.y = 75
        self.profile = 0
        teal = (108, 194, 189)
        blue = (90, 128, 158)
        purple = (124, 121, 162)
        coral = (245, 125, 124)
        self.colours = [teal, blue, purple, coral]
        self.pArr = ['A', 'B', 'C', 'D']
        self.labels = ['profile ' + self.pArr[i] for i in range(4)]
        self.font = pygame.font.SysFont("Courier New", 16)
        pub.subscribe(self.profile_handler, "gamepad.profile")
        self.expired = time.time()

    def profile_handler(self, message):
        self.set_profile(message["Profile_Dict"])

    def set_profile(self, profile):
        for i in range(len(self.pArr)):
            if profile == self.pArr[i]:
                profile = i
        if profile != self.profile:
            self.expired = time.time() + 1
        self.profile = profile

    def update(self):
        if self.expired > time.time():
            self.surface.fill((1, 1, 1))
            profSurf = pygame.Surface((self.x, self.y))
            profSurf.fill(self.colours[self.profile])

            textSurf = self.font.render(self.labels[self.profile], True, (0, 0, 0))
            textRect = textSurf.get_rect()
            textRect.center = (self.x/2, self.y/2)
            profSurf.blit(textSurf, textRect)
            self.surface.blit(profSurf, (self.screen_width-self.x, 0))
        else:
            self.surface.fill((1, 1, 1))
            label = Label(self.screen_width, self.screen_height, (0, 1), 14, bgColour=self.colours[self.profile])
            self.surface.blit(label.update(self.labels[self.profile]), (0, 0))
        return self.surface


class EMPopup:
    def __init__(self, screen_width, screen_height, order):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.set_colorkey((1, 1, 1))
        self.x = 100
        self.y = 75
        self.emL = 0
        self.emR = 0
        self.labels = ['OFF', 'ON']
        coral = (245, 125, 124)
        blue = (90, 128, 158)
        colours = [coral, blue]
        self.colour = colours[order-1]
        self.font = pygame.font.SysFont("Courier New", 16)
        pub.subscribe(self.em_handler, "gamepad.EM{}".format(order))
        self.order = order
        self.expired = time.time()

    def em_handler(self, message):
        self.set_em(message["EM_L"], message["EM_R"])

    def set_em(self, emL, emR):
        if emL != self.emL or emR != self.emR:
            self.emL = emL
            self.emR = emR
            self.expired = time.time() + 1

    def update(self):
        if self.expired > time.time():
            self.surface.fill((1, 1, 1))
            emSurf = pygame.Surface((self.x, self.y))
            emSurf.fill(self.colour)

            textSurfL = self.font.render('EM_L: ' + self.labels[self.emL], True, (0, 0, 0))
            textRectL = textSurfL.get_rect()
            textRectL.center = (self.x / 2, self.y / 2 - 10)

            textSurfR = self.font.render('EM_R: ' + self.labels[self.emR], True, (0, 0, 0))
            textRectR = textSurfR.get_rect()
            textRectR.center = (self.x / 2, self.y / 2 + 10)

            emSurf.blit(textSurfL, textRectL)
            emSurf.blit(textSurfR, textRectR)
            self.surface.blit(emSurf, ((self.order-1)*(self.screen_width-self.x), self.screen_height-self.y))
        else:
            self.surface.fill((1, 1, 1))
            label = Label(self.screen_width, self.screen_height, (1, self.order-1), 14, bgColour=self.colour)
            text = 'EM_L: ' + self.labels[self.emL] + ' EM_R: ' + self.labels[self.emR]
            self.surface.blit(label.update(text), (0, 0))
        return self.surface


class InvertPopup:
    def __init__(self, screen_width, screen_height):
        super().__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.surface = pygame.Surface((screen_width, screen_height))
        self.surface.set_colorkey((1, 1, 1))
        self.x = 100
        self.y = 75
        self.invert = 0
        red = (255, 0, 0)
        green = (0, 255, 0)
        self.colours = [green, red]
        self.iArr = ['OFF', 'ON']
        self.labels = ['Invert: ' + self.iArr[i] for i in range(2)]
        self.font = pygame.font.SysFont("Courier New", 16)
        pub.subscribe(self.invert_handler, "gamepad.invert")
        self.expired = time.time()

    def invert_handler(self, message):
        self.set_invert(message["invert"])

    def set_invert(self, invert):
        if bool(self.invert) != invert:
            self.expired = time.time() + 1
        if invert:
            self.invert = 1
        else:
            self.invert = 0

    def update(self):
        if self.expired > time.time():
            self.surface.fill((1, 1, 1))
            invertSurf = pygame.Surface((self.x, self.y))
            invertSurf.fill(self.colours[self.invert])

            textSurf = self.font.render(self.labels[self.invert], True, (0, 0, 0))
            textRect = textSurf.get_rect()
            textRect.center = (self.x / 2, self.y / 2)
            invertSurf.blit(textSurf, textRect)
            self.surface.blit(invertSurf, (0, 0))
        else:
            self.surface.fill((1, 1, 1))
            label = Label(self.screen_width, self.screen_height, (0, 0), 14, bgColour=self.colours[self.invert])
            self.surface.blit(label.update(self.labels[self.invert]), (0, 0))
        return self.surface