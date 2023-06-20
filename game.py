# Example file showing a circle moving on screen
import pygame
import time

# pygame setup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0
pygame.display.set_caption("Corpo-tenguku")

# load sounds + music
#buttonSound = pygame.mixer.Sound("sounds/button_beat.wav")
#buttonSound = pygame.mixer.Sound()

# load sprites
button_sprites = pygame.image.load("sprites/button.png")
button_sprites = pygame.transform.scale2x(button_sprites)
early_sprite = pygame.image.load("sprites/early!.png")
late_sprite = pygame.image.load("sprites/late!.png")

# Load sprite pos
textureRect = pygame.Rect(64, 0, 64, 64)
singleRect = pygame.Rect(0, 0, 64, 64)
player_pos = pygame.Vector2(screen.get_width() / 2 - 64, screen.get_height() / 2)
earlyPos = pygame.Vector2(screen.get_width() * 0.33, screen.get_height() / 2 )
latePos = pygame.Vector2(screen.get_width() * 0.67, screen.get_height() / 2 )

# random vars
early = False
late = False
blitMe = 0
FRAMESONSCREEN = 30

# handles beats
class Beatmaster():
    current_beat = 0
    bpm = 0.0
    clock = 0.0
    beat_this_tick = False
    early = False
    late = False
    
    def __init__(self):
        current_beat = 0
        bpm = 0.0
        clock = 0.0
        beat_this_tick = False
        early = False
        late = False

    def get_current_beat(self):
        return self.current_beat
    
    def get_clock(self):
        return self.clock

    def get_absTime(self):
        return float(60000 / self.bpm)

    def get_beat_this_tick(self):
        return self.beat_this_tick

    def get_late(self):
        return self.late

    def get_early(self):
        return self.early

    # Sets BPM. Used to convert to
    def set_bpm(self, bpmIn):
        self.bpm = bpmIn
        
    # Updates the current beat. Should be run every event loop.
    def update_beat(self):
        # Update clock and set beat flags tpo false
        self.clock += clock.get_time()
        self.beat_this_tick = False
        self.early = False
        self.late = False

        # Check Exact Beat
        if (self.clock > self.get_absTime()):
            self.clock = 0
            self.current_beat += 1
            self.beat_this_tick = True
        # Check Early
        if (self.clock > self.get_absTime() * 0.95 and self.clock < self.get_absTime()):
            self.early = True
        # Check Late
        if (self.clock >= 0 and self.clock < self.get_absTime() * 0.05):
            self.late = True

# Receives inputs from gameLoop, stores scores and outputs results during game.
class Grader():
    def __init__(self):
        score = 0

beats = Beatmaster()
beats.set_bpm(60)
while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")
    textureRect = pygame.Rect(0, 0, 128, 128)
    beats.update_beat()

    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if (event.type == pygame.QUIT):
            running = False

        if (event.type == pygame.KEYDOWN):
            if (beats.get_early()):
               blitMe = FRAMESONSCREEN
               early = True
            if (beats.get_late()):
               blitMe = FRAMESONSCREEN
               late = True
            if (event.key == pygame.K_a or event.key == pygame.K_l):
                #pygame.mixer.Sound.play(buttonSound)
                textureRect = pygame.Rect(128, 0, 128, 128) # Button down

    # Rough beat: Do stuff within a few frames of a beat
    # *Do sprites here*
    #if (beats.get_clock() >= beats.get_absTime() * 0.9):
        #textureRect = pygame.Rect(64, 0, 64, 64)
    # Actual beat: Do stuff once on the beat
    # if (beats.get_beat_this_tick()):
        #pygame.mixer.Sound.play(buttonSound)
    
    # Blit for FRAMESONSCREEN frames
    if (blitMe > 0):
        blitMe = blitMe - 1
        if (early):
             screen.blit(early_sprite, earlyPos, singleRect)
        if (late):
             screen.blit(late_sprite, latePos, singleRect)
    else:
        early = False
        late = False


    screen.blit(button_sprites,player_pos,textureRect)
    pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick_busy_loop(60) / 1000
pygame.quit()