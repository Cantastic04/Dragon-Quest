print("LOADING...")

# Imports
import pygame
import random

from entities import *
from settings import *


# Main game class 
class Game:
    
    # Scenes
    START = 0
    INSTRUCT = 11
    PLAYING = 1
    LOSE = 2
    WIN = 3
    PAUSE = 4
    
    def __init__(self):
        # Initialize pygame
        pygame.mixer.pre_init()
        pygame.init()

        # Make window
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        self.pause_option = 1

        # Set up game
        self.load_assets()
        self.new_game()

    def load_assets(self):
        # Fonts
        self.title_font = pygame.font.Font('assets/fonts/Dragonlands.ttf', 64)
        self.subtitle_font = pygame.font.Font('assets/fonts/Dragonlands.ttf', 32)

        # Images
        self.title_screen_img = pygame.image.load('assets/images/starting_screen.png').convert_alpha()
        self.lose_screen_img = pygame.image.load('assets/images/lose_screen.png').convert_alpha()
        self.win_screen_img = pygame.image.load('assets/images/win_screen.png').convert_alpha()
        self.pause_option_1_img = pygame.image.load('assets/images/pause_option_1.png').convert_alpha()
        self.pause_option_2_img = pygame.image.load('assets/images/pause_option_2.png').convert_alpha()
        self.pause_option_3_img = pygame.image.load('assets/images/pause_option_3.png').convert_alpha()
        self.instructions_screen_img = pygame.image.load('assets/images/instructions_screen.png').convert_alpha()
        self.bye_bye_screen_img = pygame.image.load('assets/images/exit_screen.png').convert_alpha()
        self.background_img = pygame.image.load('assets/images/scrolling_background_v2.png').convert_alpha()
        self.three_hp_img = pygame.image.load('assets/images/three_hearts.png').convert_alpha()
        self.two_hp_img = pygame.image.load('assets/images/two_hearts.png').convert_alpha()
        self.one_hp_img = pygame.image.load('assets/images/one_heart.png').convert_alpha()
        self.zero_hp_img = pygame.image.load('assets/images/zero_hearts.png').convert_alpha()

        self.dragon_1st_img = pygame.image.load('assets/images/dragon.png').convert_alpha()
        self.dragon_2nd_img = pygame.image.load('assets/images/dragon_2nd.png').convert_alpha()
        self.dragon_3rd_img = pygame.image.load('assets/images/dragon_3rd.png').convert_alpha()
        self.dragon_4th_img = pygame.image.load('assets/images/dragon_4th.png').convert_alpha()
        self.dragon_shooting_1st_img = pygame.image.load('assets/images/dragon_shooting.png').convert_alpha()
        self.dragon_shooting_2nd_img = pygame.image.load('assets/images/dragon_shooting_2nd.png').convert_alpha()
        self.dragon_shooting_3rd_img = pygame.image.load('assets/images/dragon_shooting_3rd.png').convert_alpha()
        self.dragon_shooting_4th_img = pygame.image.load('assets/images/dragon_shooting_4th.png').convert_alpha()
        self.dragon_ghost_pepper_1st_img = pygame.image.load('assets/images/dragon_ghost_pepper.png').convert_alpha()
        self.dragon_ghost_pepper_2nd_img = pygame.image.load('assets/images/dragon_ghost_pepper_2nd.png').convert_alpha()
        self.dragon_ghost_pepper_3rd_img = pygame.image.load('assets/images/dragon_ghost_pepper_3rd.png').convert_alpha()
        self.dragon_ghost_pepper_4th_img = pygame.image.load('assets/images/dragon_ghost_pepper_4th.png').convert_alpha()
        self.fireball_img = pygame.image.load('assets/images/fire_breath.png').convert_alpha()

        self.balloon_enemy_img = pygame.image.load('assets/images/balloon.png').convert_alpha()
        self.balloon_enemy_shoot_img = pygame.image.load('assets/images/balloon_shoot.png').convert_alpha()
        self.arrow_img = pygame.image.load('assets/images/arrow.png').convert_alpha()
        self.ghost_pepper_img = pygame.image.load('assets/images/ghost_pepper.png').convert_alpha()
        self.black_pepper_img = pygame.image.load('assets/images/black_pepper.png').convert_alpha()
        self.root_beer_img = pygame.image.load('assets/images/root_beer.png').convert_alpha()

        # Sounds
        self.fireball_sfx = pygame.mixer.Sound('assets/sounds/fireball.mp3')
        self.damage_sfx = pygame.mixer.Sound('assets/sounds/damage.mp3')
        self.explosion_sfx = pygame.mixer.Sound('assets/sounds/explode.mp3')
        self.arrow_sfx = pygame.mixer.Sound('assets/sounds/arrow.mp3')
        self.lose_sfx = pygame.mixer.Sound('assets/sounds/scene_lose.mp3')
        self.winner_sfx = pygame.mixer.Sound('assets/sounds/scene_win.mp3')

        # Music
        self.start_music = 'assets/music/scene_start.mp3'
        self.playing_music = 'assets/music/scene_playing.mp3'

    def new_game(self):
        pygame.mixer.stop()
        self.player = pygame.sprite.Group()
        self.dragon = Dragon(self, self.dragon_1st_img, [300, HEIGHT // 2])
        self.player.add(self.dragon)
        self.fireballs = pygame.sprite.Group()
        self.balloons = pygame.sprite.Group()
        self.arrows = pygame.sprite.Group()
        self.items = pygame.sprite.Group()

        self.level = 1
        self.scene = Game.START
        pygame.mixer.music.load(self.start_music)
        pygame.mixer.music.play(-1)
        self.scroll_background()
        self.load_current_level()

    def scroll_background(self):
        self.backgrounds = pygame.sprite.Group()

        bg1 = Background(self, self.background_img, [0, 0])
        bg2 = Background(self, self.background_img, [WIDTH * 2, 0])
        self.backgrounds.add(bg1, bg2)

    def show_heart_points(self, x, y):
        if self.dragon.heart_points >= 3:
            self.screen.blit(self.three_hp_img, [x, y])
        elif self.dragon.heart_points == 2:
            self.screen.blit(self.two_hp_img, [x, y])
        elif self.dragon.heart_points == 1:
            self.screen.blit(self.one_hp_img, [x, y])
        else:
            self.screen.blit(self.zero_hp_img, [x, y])
        
    def load_current_level(self):
        if self.level == 1:
            b1 = HotAirBalloon(self, [1000, 200], 10)
            self.balloons.add(b1)
        if self.level == 2:
            b1 = HotAirBalloon(self, [950, 200], 10)
            b2 = HotAirBalloon(self, [1100, 600], 10)
            self.balloons.add(b1, b2)
        if self.level == 3:
            b1 = HotAirBalloon(self, [900, 300], 10)
            b2 = HotAirBalloon(self, [1000, 600], 10)
            b3 = HotAirBalloon(self, [1100, 400], 10)
            self.balloons.add(b1, b2, b3)

    def play(self):
        self.scene = Game.PLAYING
        pygame.mixer.music.load(self.playing_music)
        pygame.mixer.music.play(-1)

    def instruct(self):
        self.scene = Game.INSTRUCT

    def advance(self):
        self.level += 1
        self.load_current_level()
        
    def lose(self):
        self.scene = Game.LOSE
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.lose_sfx.play()

    def win(self):
        self.scene = Game.WIN
        pygame.mixer.stop()
        pygame.mixer.music.stop()
        self.winner_sfx.play()

    def pause(self):
        self.pause_option = 1
        self.scene = Game.PAUSE

    def show_title_screen(self):
        self.screen.blit(self.title_screen_img, [0, 0])

    def show_lose_screen(self):
        self.screen.blit(self.lose_screen_img, [0, 0])

    def show_win_screen(self):
        self.screen.blit(self.win_screen_img, [0, 0])

    def show_instructions_screen(self):
        self.screen.blit(self.instructions_screen_img, [0, 0])

    def show_pause_screen(self):
        if self.pause_option == 1:
            self.screen.blit(self.pause_option_1_img, [0, 0])
        elif self.pause_option == 2:
            self.screen.blit(self.pause_option_2_img, [0, 0])
        elif self.pause_option == 3:
            self.screen.blit(self.pause_option_3_img, [0, 0])
        elif self.pause_option == 2.763:
            self.screen.blit(self.bye_bye_screen_img, [0, 0])

    def process_input(self):        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if self.scene == Game.START:
                    if event.key == pygame.K_SPACE:
                        self.play()
                    elif event.key == pygame.K_i:
                        self.instruct()
                elif self.scene == Game.INSTRUCT:
                    if event.key == pygame.K_SPACE:
                        self.play()
                elif self.scene == Game.WIN or self.scene == Game.LOSE:
                    if event.key == pygame.K_SPACE:
                        self.new_game()
                elif self.scene == Game.PLAYING:
                    if event.key == pygame.K_RETURN:
                        self.pause()
                elif self.scene == Game.PAUSE:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if self.pause_option == 1:
                            self.scene = Game.PLAYING
                        elif self.pause_option == 2:
                            self.new_game()
                        elif self.pause_option == 3:
                            pygame.mixer.stop()
                            pygame.mixer.music.stop()
                            0/0
                    elif event.key == pygame.K_UP:
                        if self.pause_option < 2:
                            self.pause_option = 3
                        else:
                            self.pause_option -= 1
                    elif event.key == pygame.K_DOWN:
                        if self.pause_option > 2:
                            self.pause_option = 1
                        else:
                            self.pause_option += 1

        pressed = pygame.key.get_pressed()

        if self.scene == Game.PLAYING:
            if pressed[pygame.K_LEFT]:
                self.dragon.move_left()
            elif pressed[pygame.K_RIGHT]:
                self.dragon.move_right()
            if pressed[pygame.K_UP]:
                self.dragon.move_up()
            elif pressed[pygame.K_DOWN]:
                self.dragon.move_down()

            if pressed[pygame.K_SPACE]:
                self.dragon.shoot()
                self.dragon.shooting = True
            else:
                self.dragon.shooting = False

    def update(self):
        if self.scene == Game.PLAYING:
            self.backgrounds.update()
            self.player.update()
            self.fireballs.update()
            self.balloons.update()
            self.arrows.update()
            self.items.update()

            if len(self.player) == 0:
                self.lose()
            if len(self.balloons) == 0:
                if self.level > 3:
                    self.win()
                else:
                    self.advance()

    def render(self):
        self.screen.fill(BLACK)
        self.backgrounds.draw(self.screen)
        self.show_heart_points(10, 10)
        self.player.draw(self.screen)
        self.balloons.draw(self.screen)
        self.fireballs.draw(self.screen)
        self.arrows.draw(self.screen)
        self.items.draw(self.screen)

        if self.scene == Game.START:
            self.show_title_screen()
        if self.scene == Game.INSTRUCT:
            self.show_instructions_screen()
        if self.scene == Game.LOSE:
            self.show_lose_screen()
        if self.scene == Game.WIN:
            self.show_win_screen()
        if self.scene == Game.PAUSE:
            self.show_pause_screen()
        
    def run(self):
        while self.running:
            self.process_input()     
            self.update()     
            self.render()
            
            pygame.display.update()
            self.clock.tick(FPS)

        pygame.quit()


# Let's do this!
if __name__ == "__main__":
   g = Game()
   g.run()
