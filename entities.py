import pygame
import random

from settings import *


class Dragon(pygame.sprite.Sprite):

    def __init__(self, game, image, loc):
        super().__init__()

        self.game = game # Lets the dragon interact in with variables in game.py
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = loc

        self.heart_points = SHIP_HEART_POINTS
        self.speed = SELF_SPEED
        self.shot_cooldown = 0
        self.ghost_pepper_time_remaining = 0
        self.frame_countdown = FRAME_COUNTDOWN
        self.shooting = False
        self.is_ghost_pepper = False

    def animate_normal(self):
        if self.frame_countdown > 0:
            self.frame_countdown -= 1
        else:
            if self.image == self.game.dragon_1st_img:
                self.image = self.game.dragon_2nd_img
            elif self.image == self.game.dragon_2nd_img:
                self.image = self.game.dragon_3rd_img
            elif self.image == self.game.dragon_3rd_img:
                self.image = self.game.dragon_4th_img
            else:
                self.image = self.game.dragon_1st_img
            self.frame_countdown = FRAME_COUNTDOWN

    def animate_shooting(self):
        if self.frame_countdown > 0:
            self.frame_countdown -= 1
        else:
            if self.image == self.game.dragon_shooting_1st_img:
                self.image = self.game.dragon_shooting_2nd_img
            elif self.image == self.game.dragon_shooting_2nd_img:
                self.image = self.game.dragon_shooting_3rd_img
            elif self.image == self.game.dragon_shooting_3rd_img:
                self.image = self.game.dragon_shooting_4th_img
            else:
                self.image = self.game.dragon_shooting_1st_img
            self.frame_countdown = FRAME_COUNTDOWN

    def animate_ghost_pepper(self):
        if self.frame_countdown > 0:
            self.frame_countdown -= 1
        else:
            if self.image == self.game.dragon_ghost_pepper_1st_img:
                self.image = self.game.dragon_ghost_pepper_2nd_img
            elif self.image == self.game.dragon_ghost_pepper_2nd_img:
                self.image = self.game.dragon_ghost_pepper_3rd_img
            elif self.image == self.game.dragon_ghost_pepper_3rd_img:
                self.image = self.game.dragon_ghost_pepper_4th_img
            else:
                self.image = self.game.dragon_ghost_pepper_1st_img
            self.frame_countdown = FRAME_COUNTDOWN   

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def shoot(self):
        if self.shot_cooldown == 0:
            fireball = Fireball(self.game.fireball_img, self.rect.midright)
            self.game.fireballs.add(fireball)
            self.game.fireball_sfx.play()
    
            if self.ghost_pepper_time_remaining == 0:
                self.shot_cooldown = FIREBALL_COOLDOWN
            else:
                self.shot_cooldown = FAST_COOLDOWN
        
    def check_boundaries(self):
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < -35:
            self.rect.top = -35
        elif self.rect.bottom > HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10

    def check_arrows(self):
        hits = pygame.sprite.spritecollide(self, self.game.arrows, True, pygame.sprite.collide_mask)

        self.heart_points -= len(hits)
        if hits:
            self.game.damage_sfx.play()
        if self.heart_points <= 0:
            self.kill()

    def check_balloons(self):
        hits = pygame.sprite.spritecollide(self, self.game.balloons, True, pygame.sprite.collide_mask)

        self.heart_points -= len(hits * 2)
        if hits:
            self.game.damage_sfx.play()
            self.game.explosion_sfx.play()
        if self.heart_points <= 0:
            self.kill()

    def check_items(self):
        hit_items = pygame.sprite.spritecollide(self, self.game.items, True, pygame.sprite.collide_mask)

        for item in hit_items:
            item.apply(self)

        if self.shot_cooldown > 0:
            self.shot_cooldown -= 1
            
        if self.ghost_pepper_time_remaining > 0:
            self.ghost_pepper_time_remaining -= 1
        else:
            self.is_ghost_pepper = False

    def update(self):
        if self.shooting == True:
            if self.is_ghost_pepper == True:    
                self.animate_ghost_pepper()
            else:
                self.animate_shooting()
        else:
            if self.is_ghost_pepper == True:
                self.animate_ghost_pepper()
            else:
                self.animate_normal()
        self.check_boundaries()
        self.check_arrows()
        self.check_balloons()
        self.check_items()


class Fireball(pygame.sprite.Sprite):

    def __init__(self, image, loc):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = loc

    def update(self):
        self.rect.x += FIREBALL_SPEED
        if self.rect.left > WIDTH:
            self.kill()


class HotAirBalloon(pygame.sprite.Sprite):

    def __init__(self, game, loc, shield):
        super().__init__()

        self.game = game
        self.image = self.game.balloon_enemy_img
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()        
        self.rect.center = loc

        self.shield = shield
        self.vy = ENEMY_SPEED
        self.vx = ENEMY_SPEED
        self.arrow_cooldown = 0
        self.move_countdown = ENEMY_FIRST_MOVE_COOLDOWN

    def move_into_position(self):
        pass

    def move(self):
        self.rect.y += self.vy

        if self.rect.top < -160 or self.rect.bottom > HEIGHT + 50:
            self.vy *= -1

    def check_fireballs(self):
        hits = pygame.sprite.spritecollide(self, self.game.fireballs, True, pygame.sprite.collide_mask)

        self.shield -= len(hits)

        if self.shield <= 0:
            self.game.explosion_sfx.play()
            self.kill()

    def check_dragon(self):
        hits = pygame.sprite.spritecollide(self, self.game.player, False, pygame.sprite.collide_mask)

        self.shield -= len(hits)

        if hits:
            self.game.explosion_sfx.play()
            self.kill()

    def shoot(self):
        r = random.randrange(0, 3000)
        if r >= 4 and r <= 50:
            self.image = self.game.balloon_enemy_shoot_img
            arrow = Arrow(self.game.arrow_img, [self.rect.left, self.rect.centery + 155])
            self.game.arrows.add(arrow)
            self.arrow_cooldown = ARROW_COOLDOWN
            self.game.arrow_sfx.play()
        elif r >= 1 and r <= 3:
            self.image = self.game.balloon_enemy_shoot_img
            item = GhostPepper(self.game.ghost_pepper_img, [self.rect.left, self.rect.centery + 155])
            self.game.items.add(item)
            self.arrow_cooldown = ARROW_COOLDOWN
            self.game.arrow_sfx.play()
        else:
            if self.arrow_cooldown > 0:
                self.arrow_cooldown -= 1
            else:
                self.image = self.game.balloon_enemy_img
        
    def update(self):
        self.move()
        self.check_fireballs()
        #self.check_dragon()
        self.shoot()


class Arrow(pygame.sprite.Sprite):

    def __init__(self, image, loc):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = loc

    def update(self):
        self.rect.x -= ARROW_SPEED
        if self.rect.right > WIDTH:
            self.kill()


class GhostPepper(pygame.sprite.Sprite):

    def __init__(self, image, loc):
        super().__init__()
        
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = loc
        
    def apply(self, player):
        player.ghost_pepper_time_remaining = ITEM_TIMER
        player.is_ghost_pepper = True
        self.kill()
        
    def update(self):
        self.rect.x -= ARROW_SPEED

        if self.rect.right > WIDTH:
            self.kill()


class Background(pygame.sprite.Sprite):

    def __init__(self, game, image, loc):
        super().__init__()
        
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = loc

    def update(self):
        self.rect.x -= BACKGROUND_SPEED
        if self.rect.right <= 0:
            self.rect.left = WIDTH * 2
