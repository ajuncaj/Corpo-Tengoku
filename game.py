
import pygame
import time
from enum import Enum
# Self imports

# globals :(
global running
running = True

def main():
    # pygame setup
    pygame.init()
    running = True

    # load sounds + music
    #buttonSound = pygame.mixer.Sound("sounds/button_beat.wav")
    #buttonSound = pygame.mixer.Sound()

    UI = UserInterface()
    
    # ----Game loop---- #
    while running:
        #UI.update()
        
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        #for event in pygame.event.get():
        #    if (event.type == pygame.QUIT):
        #        running = False
                

        # LOGIC GOES HERE :

        UI.process_input()
        
        # RENDERING GOES HERE:
        UI.clear_screen()
        UI.update()
        UI.blit()
        UI.flip()
        # ----Game loop---- #
    pygame.quit()


# handles beats
class Beatmaster():

    def __init__(self):
        self.current_beat = 0
        self.bpm = 60
        self.beat_this_tick = False
        self.early = False
        self.late = False
        self.is_beating = False
        self.clockEx = 0
        self.clock = pygame.time.Clock()

    def get_current_beat(self):
        return self.current_beat
    
    def get_clock(self):
        return self.clock

    def get_clockEx(self):
        return self.clockEx

    # Total time for a single beat (to completion)
    def get_absTime(self):
        return float(60000 / self.bpm)

    def is_beat_this_tick(self):
        return self.beat_this_tick

    def is_beat_loose(self):
        if (self.get_clockEx() >= self.get_absTime() * 0.9):
            return True
        else:
            return False

    # Is current beat within xms of beat
    def is_late(self):
        return self.late

    def is_early(self):
        return self.early

    # Sets BPM.
    def set_bpm(self, bpmIn):
        self.bpm = bpmIn
        
    def start_beats(self):
        self.is_beating = True

    def stop_beats(self):
        self.is_beating = False
        self.current_beat = 0
        self.clockEx = 0

    # Sets info for where in the rhythm we are: early, late, or exact
    # Animation should be tied to exact, early and late for input / correctness
    def check_beat(self):
        #set beat flags to false
        self.beat_this_tick = False
        self.early = False
        self.late = False
        # Check Exact Beat
        if (self.get_clockEx() > self.get_absTime()):
            self.clockEx = 0
            self.current_beat += 1
            self.beat_this_tick = True
        # Check early
        elif (self.get_clockEx() > self.get_absTime() * 0.9 and self.get_clockEx() < self.get_absTime()):
            self.early = True
        # Check Late
        elif (self.get_clockEx() >= 0 and self.get_clockEx() < self.get_absTime() * 0.1):
            self.late = True

    # Updates the current beat. Should be run every event loop.
    def update_beat(self):
        if (self.is_beating):
            # Update clock and clock Exact
            self.clock.tick_busy_loop(60)
            self.clockEx += self.clock.get_time()
            self.check_beat()


# Receives inputs from gameLoop, stores scores and outputs results during game.
class Grader():
    def __init__(self):
        self.score = 0

# To better represent different game modes
class Mode(Enum):
    MAINMENU = 1
    LEVELSELECT = 2
    TUTORIAL = 3
    MRBITFLIP = 4
    STAIRMASTER = 5
    DEATHCHICKS = 6

# Handles user input
# TODO: Implement observer to do stuff with player input and scoring
class UserInterface():
    def __init__(self):
        self.beats = Beatmaster()
        self.gamestate = GameState(self.beats)
        self.animate = Animation(self.gamestate)
        self.mixer = Mixer(self.gamestate)
        self.gamemode = GameMode(self.gamestate, self.animate, self.mixer)
        #FOR TESTING - REMOVE
        self.gamestate.currentMode = Mode.TUTORIAL
        

    # Process player input
    # TODO: Use process_input of GameMode object to use for each individial mode 
    def process_input(self):
        self.check_mode()
        self.gamemode.process_input()
    
    @property
    def get_animate(self):
        return self.animate

    # Detects change in gameMode and switches
    # **Should be run every loop**
    def check_mode(self):
        if (self.gamestate.lastMode != self.gamestate.currentMode):
            if (self.gamestate.currentMode == Mode.MAINMENU):
                self.gamemode = GameModeMenu(self.gamestate, self.animate, self.mixer)
                self.gamestate.lastMode = Mode.MAINMENU
            elif (self.gamestate.currentMode == Mode.TUTORIAL):
                self.gamemode = GameModeTutorial(self.gamestate, self.animate, self.mixer)
                self.gamestate.lastMode = Mode.TUTORIAL
            elif (self.gamestate.currentMode == Mode.MRBITFLIP):
                self.gamemode = GameModeMrbitflip(self.gamestate, self.animate, self.mixer)
                self.gamestate.lastMode = Mode.MRBITFLIP
            else:
                return

    def clear_screen(self):
        self.gamemode.animate.screen.fill("purple")

    def blit(self):
        self.gamemode.animate.blit()

    def flip(self):
        self.gamemode.animate.flip()

    def update(self):
        self.gamemode.update()

# Stores information based on whats currently happening in-game
# TODO: Implement
class GameState():
    def __init__(self, beatmaster):
        self.currentMode = Mode.MAINMENU
        self.lastMode = Mode.MAINMENU
        self.beats = beatmaster

        self.score = 0
        self.is_beating = False

    def update(self):
        self.beats.update_beat()

    def get_beatmaster(self):
        return self.beats

    def is_beat_loose(self):
        return self.beats.is_beat_loose()

    def is_beating(self):
        return self.is_beating()

    def start_beats(self):
        self.beats.start_beats()
        self.is_beating = True

    def stop_beats(self):
        self.beats.stop_beats()
        self.is_beating = False

    def reset_score(self):
        self.score = 0

    # Increase score based on mode
    # Return true if done, false if not
    def increase_score(self):
        if (self.currentMode == Mode.TUTORIAL):
            self.score += 1
            if (self.score == 3):
                return True
            return False

    def check_correct_input(self):
        if (self.is_beat_loose()):
            self.increase_score()

# Loads and sets images for animation
# To-do: Integrate with player input (observer?)
class Animation():
    def __init__(self, gamestateIn):
        #Init obj.
        self.gamestate = gamestateIn
        
        #Init screen
        self.screen = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Corpo-tenguku")
        
        #Init vars
        self.FRAMESONSCREEN = 15
        self.blitMe = []

    def add_to_blitMe(self, sprite, pos, name = "Remove"):
        self.blitMe.append(Sprite(sprite, pos, name))

    def initialize_tutorial(self):
        # Load sprite pos + recs
        leftButtonPos = pygame.Vector2(self.screen.get_width() * 0.33, self.screen.get_height() / 2 )
        rightButtonPos = pygame.Vector2(self.screen.get_width() * 0.67, self.screen.get_height() / 2 )

        # load sprites
        button_sprites = pygame.image.load("sprites/button.png")
        early_sprite = pygame.image.load("sprites/early!.png")
        late_sprite = pygame.image.load("sprites/late!.png")

        # load into blitMe
        self.add_to_blitMe(button_sprites, leftButtonPos, "blueButton")
        self.add_to_blitMe(button_sprites, rightButtonPos, "redButton")

    # TODO: Make one button blue or something and put them farther apart
    def left_button_down(self):
       for image in self.blitMe:
           if (image.name == "blueButton"):
               image.isAnimate = True

    def right_button_down(self):
         for image in self.blitMe:
           if (image.name == "redButton"):
               image.isAnimate = True

    # TODO: Figure out correct dependencies for animations 
    # current idea is to add some sort of update function to blit, which will check + correct sprites, and change them depending on member variables.
    def blit(self):
        # For testing maybe? at least statement should be used somewhere for sure
        if (self.gamestate.is_beat_loose()):
            self.screen.fill("grey")
        
        # Stay on screen for FRAMESONSCREEN ticks
        for image in self.blitMe:
            if (image.isVisable and image.isAnimate):
                image.next_frame()
                self.screen.blit(image.sprite, image.pos, image.rect)
            elif (image.isVisable):
                self.screen.blit(image.sprite, image.pos, image.rect)
            
    def flip(self):
         pygame.display.flip()

# Represents an individual sprite
# Pygame has one of these but it just does this...basically?
class Sprite():
    def __init__(self, spriteIn, posIn, nameIn = "remove"):
        self.sprite = spriteIn
        self.pos = posIn
        self.rect = pygame.Rect(0, 0, 64, 64)
        self.name = nameIn
        self.isVisable = True
        self.isAnimate = False

    # Move to next frame of animation based on size of spritesheet
    # TODO: Some sprites are transformed, changes the width of sprite sheet
    def next_frame(self):
        if (self.rect.x >= self.sprite.get_width()):
            self.rect.x = 64
            self.rect.y += 64
        else:
            self.rect.x += 64
        self.check_frames()

    #checks to see if the animation has finished. Reset if it is
    def check_frames(self):
        if (self.rect.y > self.sprite.get_height()):
            self.isAnimate = False
            self.rect.x = 0
            self.rect.y = 0

class Mixer():
    def __init__(self, gamestateIn):
        self.gamestate = gamestateIn
        pygame.mixer.init()
        # Load music here:
        #self.tutorial = pygame.mixer.Sound("test.wav")

    def initalize_tutorial(self):
        pass

    def start_music(self):
        pygame.mixer.start()

    def stop_music(self):
        pygame.mixer.stop()
    
        

# Represents what mode the game is currently in:
#   1. MenuIntro
#   2. MenuLevels
#   3. 1 for each game
#
# Will handle input for each individual "level"
# For example: Go to menu -> menu inputs + animations -> Select game -> game inputs + animations
# TODO: Implement
class GameMode():
    def __init__(self, gamestateIn, animationIn, mixerIn):
        self.animate = animationIn
        self.gamestate = gamestateIn
        self.mixer = mixerIn

    def process_input(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_RIGHT:
                    self.right_mouse()
                if event.button == pygame.BUTTON_LEFT:
                    self.left_mouse()
            if (event.type == pygame.QUIT):
                running = False

    def start_beats(self):
        self.gamestate.start_beats()

    def stop_beats(self):
         self.gamestate.stop_beats()

    def right_mouse(self):
        pass

    def left_mouse(self):
        pass

    def update(self):
        self.gamestate.update()


# NOTE: Menus might want their own control scheme, dont forget to override
class GameModeMenu(GameMode):
    def process_input(self):
        pass

    def update():
        pass
    def render():
        pass

class GameModeLevels(GameMode):
    def process_input(self):
        pass

class GameModeTutorial(GameMode):
    def __init__(self, gamestateIn, animationIn, mixerIn):
        super().__init__(gamestateIn, animationIn, mixerIn)
        
        self.section = 0 # 1 = basics, 2 = left, 3 = right, 4 = both
        self.prevSection = 0

        self.animate.initialize_tutorial()
        #self.mixer.initialize_tutorial()
        self.start_tutorial()

    def update(self):
        super().update()

        # check and switch mode only once
        if (self.section == self.prevSection):
            pass
        elif (self.section == 1 and self.prevSection == 0):
            self.basics()
            self.prevSection += 1
        elif (self.section == 2 and self.prevSection == 1):
            self.left_beat()
            self.prevSection += 1
        elif (self.section == 3 and self.prevSection == 2):
            self.right_beat()
            self.prevSection += 1
        elif (self.section == 4 and self.prevSection == 3):
            self.switch_beat()
            self.prevSection += 1

        if (self.gamestate.score == 3 and self.gamestate.is_beating()):
            self.section += 1
            self.gamestate.reset_score()
            self.gamestate.stop_beats()
    
    def right_mouse(self):
        self.animate.right_button_down()
        #self.gamestate.check_correct_input()

    def left_mouse(self):
         self.animate.left_button_down()

    def start_tutorial(self):
        # play voicelines
        self.section += 1

    def basics(self):
        # Play voicelines
    
        # Start tracking until the player does well enough
         self.gamestate.start_beats()
        # switch to next

class GameModeMrbitflip(GameMode):
    def __init__(self, gamestateIn, animationIn, mixerIn):
        super().__init__(gamestateIn, animationIn, mixerIn)
        
        #self.animate.initialize_mrbitflip()
        #self.mixer.initialize_mrbitflip()
        #self.start_game()
    
    def update():
        super().update()

    def render():
        pass

    def right_mouse(self):
        self.animate.right_hand_down()

    def left_mouse(self):
        self.animate.left_hand_down()

class GameModeRemix(GameMode):
    def update():
        pass
    def render():
        pass
    
if __name__ == '__main__':
    main()