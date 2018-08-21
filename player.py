import pygame
BOUNCE = False


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, images):
        super().__init__()
        self.images = images
        self.image = images["p1_jump"]
        self.rect = self.image.get_rect()
        self.rect.center = pos
        # index 0 represents dx, index 1 represents dy
        self.xy_speed = pygame.math.Vector2(0, 0)
        self.facing = "R"
        self.jump_speed = -14
        self.jumping =True
        self.world_y = 0
        self.progress = 0
        self.frame = 1

    def update(self, platforms):
        screen_info = pygame.display.Info()

        # update the image and direction
        if self.rect.bottom >= screen_info.current_h:
            self.image = self.images['p1_hurt']
        elif self.jumping:
            self.image = self.images['p1_jump']
        elif self.xy_speed[0] == 0:
            self.image = self.images['p1_stand']
        else:
            frame = (pygame.time.get_ticks() // 55 % 11) + 1
            frame = str(frame).zfill(2)
            self.image = self.images['p1_walk{}'.format(frame)]
        if self.facing == "L":
            self.image = pygame.transform.flip(self.image, True, False)
            #move the player
        self.rect.move_ip(self.xy_speed)
        self.xy_speed[0] = 0
        self.world_y += self.xy_speed[1]*-1

        if self.rect.right < 0:
            self.rect.left = screen_info.current_w
        elif self.rect.left > screen_info.current_w:
            self.rect.right = 0


        # handle vertical movement
        if self.world_y > self.progress:
            self.progress = self.world_y
        # scroll platforms down
        if self.rect.top < 100:
            self.rect.top = 100
            for plat in platforms.sprites():
                plat.scroll(-1*self.xy_speed[1])
        # scroll platforms up (player fell offworld)
        elif self.rect.bottom > screen_info.current_h:
            self.rect.bottom = screen_info.current_h
            for plat in platforms.sprites():
                if plat.rect.bottom > 0:
                    plat.scroll(-1 * self.xy_speed[1])
                else:
                    plat.kill()

        #check if the player hit any platforms
        hit_list = pygame.sprite.spritecollide(self, platforms, False)
        for plat in hit_list:
            #player landed kon top of a platform
            if self.xy_speed[1] > 0 and abs(self.rect.bottom - plat.rect.top) <= self.xy_speed[1]:
                self.rect.bottom = plat.rect.top
                if BOUNCE:
                    self.xy_speed[1] = self.jump_speed
                else:
                    self.jumping = False
                    self.xy_speed[1] = 0
        # gravity
        if self.jumping and self.xy_speed[1] < 30:
            self.xy_speed[1] += .5
        else:
            # code for falling off platforms
            self.rect.y += 2
            hit_list = pygame.sprite.spritecollide(self, platforms, False)
            if len(hit_list) == 0:
                self.jumping = True
            else:
                for plat in hit_list:
                    if abs(self.rect.bottom - plat.rect.top) > 2:
                        self.jumping = True
                    else:
                        self.jumping = False
                        self.rect.y -= 2
                        break

    def left(self):
        self.facing = 'L'
        if self.jumping:
            self.xy_speed[0] = -6
        else:
            self.xy_speed[0] = -4

    def right(self):
        self.facing = 'R'
        if self.jumping:
            self.xy_speed[0] = 6
        else:
            self.xy_speed[0] = 4

    def jump(self):
        if not self.jumping:
            self.jumping = True
            self.xy_speed[1] = self.jump_speed

