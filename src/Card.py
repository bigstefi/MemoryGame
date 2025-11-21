import pygame

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
BACK = 0
FACE = 1

class Card:
    # Constructor
    def __init__(self, x, y, width, height, colorFace, colorBack):
        self._rectangle = pygame.Rect(x, y, width, height)
        self._side = BACK
        self._colorFace = colorFace
        self._colorBack = colorBack
        self._color = colorBack

    def GetRectangle(self):
        return self._rectangle
    
    def Show(self, screen):
        if self._side == BACK:
            self._color = self._colorBack
        else:
            self._color = self._colorFace

        pygame.draw.rect(screen, self._color, (self._rectangle.x, self._rectangle.y, self._rectangle.width, self._rectangle.height))

    def OnClick(self, screen):
        self.SwapSide()
        self.Show(screen)

        #pygame.time.delay(1000)  # Pause for a moment to show the cards

    def SwapSide(self):
        if self._side == BACK:
            self._side = FACE
            self._color = self._colorFace
        else:
            self._side = BACK
            self._color = self._colorBack

        print(self._color)

    def GetColor(self):
        print(self._color)
        return self._color
