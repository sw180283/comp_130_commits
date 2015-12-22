# import all these things so that the .pv file can access them

import random # import random allows for random generation of values

from kivy.app import App # import abilities of kivy to run app
from kivy.uix.widget import Widget # import widgets from kivy
#from kivy.graphics import Color, Rectangle # commented out as image used instead
from kivy.core.window import Window # import window adjustment
from kivy.uix.image import Image # import use of images
from kivy.clock import Clock # import kivy clock
from kivy.uix.label import Label # import kivy label
from kivy.core.audio import SoundLoader # import sound usage

# set the sound source
sfx_flap = SoundLoader.load("Resources/kivy-game-dev/flappy/audio/flap.wav")
sfx_score = SoundLoader.load("Resources/kivy-game-dev/flappy/audio/score.wav")
sfx_die = SoundLoader.load("Resources/kivy-game-dev/flappy/audio/die.wav")

# create the main menu using the widget to add the background, ground, label
class Menu(Widget):
    def __init__(self):
        super(Menu, self).__init__()
        self.add_widget(Sprite(source="Resources/kivy-game-dev/flappy/images/background.png"))
        self.size = self.children[0].size
        self.add_widget(Ground(source="Resources/kivy-game-dev/flappy/images/ground.png"))
        self.add_widget(Label(center=self.center, text="tap to start"))
# when click down remove the menu widget and add the game widget as the new parent
    def on_touch_down(self, *ignore):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(Game())

# when calling sprites use the image import, **kwargs stop from messing with functionality, size is set to the size of the image
class Sprite(Image):
    def __init__(self, **kwargs):
        super(Sprite, self).__init__(**kwargs)
        self.size = self.texture_size

# the pipe class used as widget, set the top and bottom image as different pipes, add each as widget
# set top image position to x, with y being 5.5 * the size of the player
# set the score to false as default
class Pipe(Widget):
    def __init__(self, pos):
        super(Pipe, self).__init__(pos=pos)
        self.top_image = Sprite(source="Resources/kivy-game-dev/flappy/images/pipe_top.png")
        self.top_image.pos = (self.x, self.y + 5.5 * 24)
        self.add_widget(self.top_image)
        self.bottom_image = Sprite(source="Resources/kivy-game-dev/flappy/images/pipe_bottom.png")
        self.bottom_image.pos = (self.x, self.y - self.bottom_image.height)
        self.add_widget(self.bottom_image)
        self.width = self.top_image.width
        self.scored = False

# update the pipe widget with the x position moving 2 pipes worth of space
# set the top and bottom image as the updating self.x value
# if the pipe is less than 0 position remove the pipe widget
    def update(self):
        self.x -= 2
        self.top_image.x = self.bottom_image.x = self.x
        if self.right < 0:
            self.parent.remove_widget(self)

# the pipes class changes the calling of pipes
# update the pipes by time
# add a pipe at random height for gap position
class Pipes(Widget):
    add_pipe = 0
    def update(self, dt):
        for child in list(self.children):
            child.update()
        self.add_pipe -= dt
        if self.add_pipe < 0:
            y = random.randint(self.y + 50, self.height - 50 - 5.5 * 24)
            self.add_widget(Pipe(pos=(self.width, y)))
            self.add_pipe = 1.5

# add background widget where image sprite is used
# duplicate the image with x position set at end of last image
class Background(Widget):
    def __init__(self, source):
        super(Background, self).__init__()
        self.image = Sprite(source=source)
        self.add_widget(self.image)
        self.size = self.image.size
        self.image_dupe = Sprite(source=source, x=self.width)
        self.add_widget(self.image_dupe)

# update the image and duplicate
# when the image is less than 0 place image duplicate at the end of the last image
    def update(self):
        self.image.x -= 2
        self.image_dupe.x -= 2

        if self.image.right <= 0:
            self.image.x = 0
            self.image_dupe.x = self.width

# the bird class is called as a sprite with the velocity and gravity of player is set
class Bird(Sprite):
    def __init__(self, pos):
        super(Bird, self).__init__(source="atlas://Resources/kivy-game-dev/flappy/images/bird_anim/wing-up", pos=pos)
        self.velocity_y = 0
        self.gravity = -.3

# the max velocity is set and the y position of the player is set as the updating velocity
# the image of the bird is dependent on the velocity
    def update(self):
        self.velocity_y += self.gravity
        self.velocity_y = max(self.velocity_y, -10)
        self.y += self.velocity_y
        if self.velocity_y < -5:
            self.source = "atlas://Resources/kivy-game-dev/flappy/images/bird_anim/wing-up"
        elif self.velocity_y < 0:
            self.source = "atlas://Resources/kivy-game-dev/flappy/images/bird_anim/wing-mid"

# when clicked set the velocity and change the bird image and make flap sound
    def on_touch_down(self, *ignore):
        self.velocity_y = 5.5
        self.source = "atlas://Resources/kivy-game-dev/flappy/images/bird_anim/wing-down"
        sfx_flap.play()

# the ground is called as a sprite with the ground being updated moving it's x position
class Ground(Sprite):
    def update(self):
        self.x -= 2
        if self.x < -24:
            self.x += 24

# the game is called as a widget
# the background is set and added as a widget
# the pipes are added as a widget under the ground so that the ground covers bottom edge
# the ground is added as a widget
# the score label is centered but at the top of the screen with a default text of "0" score
# the over label of "Game Over" text has it's opacity set to 0 so is invisible
# the bird player is set (x, y) = (20, half of screen) and added as a widget
# the clock calls for updates at 60 times per second
# game_over is default set to false and the score is default set to 0
class Game(Widget):
    def __init__(self):
        super(Game, self).__init__()
        self.background = Background(source="Resources/kivy-game-dev/flappy/images/background.png")
        self.size = self.background.size
        self.add_widget(self.background)
        self.ground = Ground(source="Resources/kivy-game-dev/flappy/images/ground.png")
        self.pipes = Pipes(pos=(0, self.ground.height), size=self.size)
        self.add_widget(self.pipes)
        self.add_widget(self.ground)
        self.score_label = Label(center_x=self.center_x,
            top=self.top - 30, text="0")
        self.add_widget(self.score_label)
        self.over_label = Label(center=self.center, opacity=0,
            text="Game Over")
        self.add_widget(self.over_label)
        self.bird = Bird(pos=(20, self.height / 2))
        self.add_widget(self.bird)
        Clock.schedule_interval(self.update, 1.0/60.0)
        self.game_over = False
        self.score = 0

# update by delta time
# check for game_over
# check for bird collision with ground and change game_over accordingly
# check for bird collision with top and bottom pipe and change game_over accordingly
# if the position of the pipe is behind the player, set score +1 and set scored to true
# set the score label to reflect the string score and play score sound
    def update(self, dt):
        if self.game_over:
            return

        self.background.update()
        self.bird.update()
        self.ground.update()
        self.pipes.update(dt)

        if self.bird.collide_widget(self.ground):
            self.game_over = True

        for pipe in self.pipes.children:
            if pipe.top_image.collide_widget(self.bird):
                self.game_over = True
            elif pipe.bottom_image.collide_widget(self.bird):
                self.game_over = True
            elif not pipe.scored and pipe.right < self.bird.x:
                pipe.scored = True
                self.score += 1
                self.score_label.text = str(self.score)
                sfx_score.play()

# play die sound and change opacity of the over_label to visible
        if self.game_over:
            sfx_die.play()
            self.over_label.opacity = 1
            self.bind(on_touch_down=self._on_touch_down)

# on click down remove the game widget and add the menu widget
    def _on_touch_down(self, *ignore):
        parent = self.parent
        parent.remove_widget(self)
        parent.add_widget(Menu())

# call as the app where the top widget called is the menu with the window size set to it's game size
class GameApp(App):
    def build(self):
        #return Game(size=Window.size)
        #return Game()
        #game = Game()
        top = Widget()
        top.add_widget(Menu())
        Window.size = top.children[0].size
        return top
        #return game

if __name__ == "__main__":
    GameApp().run()