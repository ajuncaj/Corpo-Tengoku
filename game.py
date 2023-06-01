# Example file showing a circle moving on screen
import pygame

# pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
pygame.display.set_caption("Corpo-tenguku")

# load sounds + music
buttonSound = pygame.mixer.Sound("sounds/button_beat.wav")

# load sprites
button_sprites = pygame.image.load("sprites/button.png")
textureRect = pygame.Rect(64, 0, 64, 64)
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# handles beats
class Beatmaster():
    current_beat = 0
    bpm = 0.0
    clock = 0.0
    beat_this_tick = False

    def __init__(self):
        current_beat = 0
        bpm = 0.0
        clock = 0.0
        beat_this_tick = False

    def get_current_beat(self):
        return self.current_beat
    
    def get_clock(self):
        return self.clock

    def get_absTime(self):
        return float(60000 / self.bpm)

    def get_beat_this_tick(self):
        return self.beat_this_tick

    # Sets BPM. Used to convert to
    def set_bpm(self, bpmIn):
        self.bpm = bpmIn
        
    # Updates the current beat. Should be run every event loop.
    def update_beat(self):
        # Get beats per tick
        self.clock += clock.get_time()
        self.beat_this_tick = False
        if (self.clock > self.get_absTime()):
            self.clock = 0
            self.current_beat += 1
            self.beat_this_tick = True

beats = Beatmaster();
beats.set_bpm(60);
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    textureRect = pygame.Rect(64, 0, 64, 64)

    beats.update_beat()
    if (beats.get_clock() >= beats.get_absTime() * 0.9):
        textureRect = pygame.Rect(64, 64, 64, 64)
        pygame.mixer.Sound.play(buttonSound)
    if (beats.get_beat_this_tick()):
        textureRect = pygame.Rect(64, 64, 64, 64)
        pygame.mixer.Sound.play(buttonSound)
    
    # check left / right mouse presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        
        pygame.mixer.Sound.play(buttonSound)
    if keys[pygame.K_l]:
        pygame.draw.circle(screen, "blue", player_pos, 40, 
                           draw_bottom_left = False, draw_top_left = False)
        pygame.mixer.Sound.play(buttonSound)
    
    screen.blit(button_sprites,player_pos,textureRect)
    
    pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick_busy_loop(60) / 1000
pygame.quit()