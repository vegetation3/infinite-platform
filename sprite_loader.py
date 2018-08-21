import pygame


class SpriteSheet:

    def __init__(self, img_path):
        # load sprite sheet in
        self.sprite_sheet = pygame.image.load(img_path).convert()

    def get_image(self, x, y, width, height):
        # create a blank image
        img = pygame.Surface([width, height]).convert()
        # blit desired section to the blank image
        img.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # do not display any black pixels, gives a blank background
        img.set_colorkey((   0,   0,   0))
        return img
