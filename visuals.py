import pygame
import numpy as np
import spacecraft as sc
import finkchlib.vector as v

# This class is the screen to draw onto
class Draw:
    def __init__(self, width, height):

        # Adds constants to help draw
        self.MIN_SIZE = 0
        self.MIN_RADIUS = 2
        self.PADDING = 1.2
        self.PIXEL_PADDING = 10
        self.STRING_PADDING = 18
        self.TYPE_FACE = 'courier'
        self.GREY4 = (255 // 4, 255 // 4, 255 // 4)
        self.GREY2 = (255 // 2, 255 // 2, 255 // 2)

        # Screen dimensions
        self.WIDTH = width
        self.HEIGHT = height

        # Initialises pygame, used to draw
        pygame.init()

        # Adds a few fonts
        self.fonts = {}
        self.add_font('smaller', 12)
        self.add_font('small', 14)
        self.add_font('medium', 16)

        # Obtains the screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))



    # Draws to screen
    def __call__(self, clock, zoom, actors, kwargs):

        # Clears screen to black
        self.screen.fill("black")

        # Adds some useful information
        self.draw_time(clock)
        self.draw_performance(clock)

        self.draw(clock, zoom, actors, kwargs)

        # Draws
        pygame.display.flip()



    # Puts the things onto the screen.
    # OVERLOAD THIS FUNCTION
    def draw(self, timer, zoom, actors, kwargs):
        pass




    # Adds a font to the class' library
    def add_font(self, name, font_size, type_face = None):
        
        # Gets the default for the typeface
        if not type_face:
            type_face = self.TYPE_FACE

        # Adds a font to the class' library
        self.fonts[name] = pygame.font.SysFont(type_face, font_size)


    # Checks if the position is within the screen
    def onscreen(self, position, offset = 0):
        
        # Gets the padded bounds
        x_bounds = [self.WIDTH * (1 - self.PADDING), self.WIDTH * self.PADDING]
        y_bounds = [self.HEIGHT * (1 - self.PADDING), self.HEIGHT * self.PADDING]

        # Checks the bounds and the offset
        if offset != 0:
            return (
                    self.in_bounds(position[0], x_bounds) and self.in_bounds(position[1], y_bounds)
                ) or (
                    self.in_bounds(position[0], x_bounds, offset) and self.in_bounds(position[1], y_bounds, offset)
                )
        
        # Checks just the bounds
        return self.in_bounds(position[0], x_bounds) and self.in_bounds(position[1], y_bounds)
    
    # Checks for one axis whether it is within the specified bounds
    def in_bounds(self, position, bounds, offset = 0):
        return position + offset > bounds[0] and position - offset < bounds[1]
    


    # Methods to add simple objects

    # Draws a circle
    def circle(self, position, radius, colour = 'white'):
        if self.onscreen(position, radius):
            pygame.draw.circle(self.screen, colour, position, radius)

    # Draws a line
    def line(self, start, stop, colour = 'white', width = 1):
        if self.onscreen(start) or self.onscreen(stop):
            pygame.draw.line(self.screen, colour, start, stop, width = width)

    # Renders a single bit of text
    def text(self, string, position, pad = True, type_face = 'medium', colour = 'white', antialias = True, left = True):

        # Don't draw if the text is offscreen
        if not self.onscreen(position):
            return

        # 'Fixes' scientific notation
        string = string.replace("e+", "e")

        # Obtains the font object
        text = self.fonts[type_face].render(string, antialias, colour)
        text_shape = text.get_rect()

        # Gets the correct amount of padding
        padding = self.PIXEL_PADDING
        if not pad:
            padding = 0

        # Places the text
        if left:
            text_shape.topleft = (padding + position[0], padding + position[1])
        else:
            text_shape.topright = (padding + position[0], padding + position[1])

        # Renders the text
        self.screen.blit(text, text_shape)
            

    # Renders a column of text in rows as specified by strings
    def text_column(self, strings, position, pad = True, down = True, left = True):

        if not strings:
            return

        # Gets the correct amount of padding
        padding = self.PIXEL_PADDING
        if not pad:
            padding = 0

        # Iterates over all strings
        draw_at = [None, None]
        for i in range(len(strings)):

            # Obtains the position to draw them at
            draw_at[0] = padding + position[0]
            if down:
                draw_at[1] = padding + position[1] + i * self.STRING_PADDING
            else:
                draw_at[1] = position[1] - padding - (len(strings) - i) * self.STRING_PADDING

            # Renders the text row
            self.text(self.screen, strings[i], draw_at, pad = False, left = left)


    # Adds a time readout
    def draw_time(self, clock):

        # Renders timer readout
        self.text_column(self.screen, clock.get_printout(), [0, 0])

    # Adds some performance metrics
    def draw_performance(self, clock):

        strings = [
            f'{1000 / clock.real_time.get_average_difs():.3f} fps',
            f'{1000 / clock.timer.get_average_difs():.0f} sps'
        ]

        self.text_column(self.screen, strings, [self.WIDTH - self.STRING_PADDING, 0], left = False)



# The draw class for this simulation
class IonRamjetDraw(Draw):
    def __init__(self, width, height):
        super().__init__(width, height)

    # Draws everything
    #   focus is the actor at the centre of the display
    def draw(self, timer, zoom, actors, kwargs):
        
        # Grabs the star of the show
        craft = kwargs['craft']


        # Finds the maximum distance between the crafts and the PoR.
        # This distance is used to scale everything to fit on screen.
        # Extra factor of two is for half the screen
        scale = (self.WIDTH - self.PIXEL_PADDING) / (zoom.zoom()) / 2

        # Draws the reference axis and ticks
        self.draw_axis()
        self.draw_scale(zoom, scale)

        # Draws the actors to screen
        self.draw_actors(zoom, actors, scale)

        # Draws some craft informatiom
        self.draw_focus_readout(zoom.focus)

        # How full the tanks are
        self.draw_craft_tanks(craft)

        # How fast things are being produces
        self.draw_craft_generators(craft)


    # Draws two orthogonal lines for the axis
    def draw_axis(self):
        self.line(self.screen, (self.PIXEL_PADDING, self.HEIGHT / 2), (self.WIDTH - self.PIXEL_PADDING, self.HEIGHT / 2), self.GREY4)
        self.line(self.screen, (self.WIDTH / 2, self.PIXEL_PADDING), (self.WIDTH / 2, self.HEIGHT - self.PIXEL_PADDING), self.GREY4)

    def draw_scale(self, zoom, scale):

        log_scale = int(np.log10(float(zoom.zoom())))
        
        # Iterates over both the current order and within one order
        for order in range(log_scale - 1, log_scale + 1):

            # Iterate over 0 - 10 inclusive
            for i in range(1, 11):

                # Gets the position on the screen offset from the centre
                distance = i * 10 ** order
                x_pos = distance * scale

                # Stop drawing if the x_pos is too large
                if x_pos > self.WIDTH / 2:
                    break

                # Draws the tick
                self.draw_tick(i, x_pos, distance)
        

        # Caps each axis with a line
        self.line((self.WIDTH - self.PIXEL_PADDING, self.HEIGHT / 2 + 16), (self.WIDTH - self.PIXEL_PADDING, self.HEIGHT / 2 - 16), self.GREY2)
        self.line((self.WIDTH / 2 + 16, self.PIXEL_PADDING), (self.WIDTH / 2 - 16, self.PIXEL_PADDING), self.GREY2)

        # Prints the current scale
        self.text(f'{zoom.zoom():.2e}', (self.WIDTH - self.PIXEL_PADDING, self.HEIGHT / 2 - 32), False, type_face = 'small', left = False)


    # Draws ticks on the axes
    def draw_tick(self, i, x_pos, distance):

        # Gets parameters of the line
        height = 4
        col = self.GREY2
        text_col = "white"

        cutoff = 0.05
        fade_start = 0.3

        # The multiplier of how solid and large the ticks are
        solid = (x_pos / self.WIDTH * 2 - cutoff) / fade_start
        
        # Don't draw anything below the cutoff or beyond the edge of the axis
        if solid < 0 or x_pos > self.WIDTH / 2 - self.PIXEL_PADDING:
            return
        
        # Fades the attributes
        if solid < 1:
            
            # Obtains the faded text colour
            text_col = 255 * solid
            text_col = (text_col, text_col, text_col)

            # Fades the tick to the axis colour
            #   GREY2 -> GREY4
            col = 127 - 64 * (1 - solid)
            col = (col, col, col)

            # Scales the height of the tick
            height *= solid


        # Offsets the tick towards the centre
        x_pos += self.WIDTH / 2

        # Draws the major ticks
        if i == 10:
            height *= 3
            self.text(f'{distance:.0e}', (x_pos - 16, self.HEIGHT / 2 + height + 4), False, type_face = "smaller", colour = text_col)

        # Draws the minor ticks
        self.line((x_pos, self.HEIGHT / 2 + height), (x_pos, self.HEIGHT / 2 - height), col)

        # Draws the ticks on the y-axis
        #   NOTE! Only works if the screen is a square
        self.line((self.HEIGHT / 2 + height, self.HEIGHT - x_pos), (self.HEIGHT / 2 - height, self.HEIGHT - x_pos), col)


    # Draws the actors
    def draw_actors(self, zoom, actors, scale):
        # Draws each actor
        for actor in actors:

            # Gets the actor's radius
            radius = actor.radius * scale

            # If the radius is too small to see, scale it to the minimum size
            if radius < self.MIN_RADIUS:
                radius = self.MIN_RADIUS


            # Draws the shape
            pixel_position = (((actor.pos() - zoom.focus.pos()) * scale) + v.Vector(self.WIDTH / 2, self.HEIGHT / 2, 0)).plane()
            self.circle(pixel_position, radius)

            # Draws labels on each actor
            self.draw_labels(actor, pixel_position, radius)

            # Draws craft's orientation
            if isinstance(actor, sc.Spacecraft):

                # Gets the position of the orientation indicator
                distance = 2
                indicator = (
                        pixel_position[0] + (radius * 3 / 2 + distance) * np.cos(actor.apos().phi), 
                        pixel_position[1] + (radius * 3 / 2 + distance) * np.sin(actor.apos().phi)
                    )

                self.circle(indicator, radius / 2)


    # Labels an actor
    def draw_labels(self, actor, pixel_position, radius):

        # Special angle in a triangle for π/4 radians
        radius_scaled = radius * np.sqrt(1/2) + 2
        
        # The length of the line
        distance = 6

        # Renders the name of the actor
        self.text(actor.name, (pixel_position[0] + radius_scaled + distance, pixel_position[1] + radius_scaled + distance), False, type_face = "small")

        # Draws a line from the text to the actor
        self.line((pixel_position[0] + radius_scaled, pixel_position[1] + radius_scaled), (pixel_position[0] + radius_scaled + distance, pixel_position[1] + radius_scaled + distance))

    

    # Adds some of craft information readout
    def draw_focus_readout(self, focus):

        # Renders the text into a column
        self.text_column(focus.get_printout(), [0, self.HEIGHT], down = False, pad = True)


    # Renders the ship's internal data
    def draw_craft_tanks(self, craft):
        self.text_column(craft.get_printout_regulators(), [self.WIDTH - self.STRING_PADDING, self.HEIGHT], down = False, left = False)

    def draw_craft_generators(self, craft):
        self.text_column(craft.get_printout_generators(), [self.WIDTH - self.STRING_PADDING, self.HEIGHT - (len(craft.get_printout_regulators()) + 1) * self.STRING_PADDING], down = False, left = False)
    