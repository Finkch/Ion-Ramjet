import pygame

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
            self.text(strings[i], draw_at, pad = False, left = left)


    # Adds a time readout
    def draw_time(self, clock):

        # Renders timer readout
        self.text_column(clock.get_printout(), [0, 0])

    # Adds some performance metrics
    def draw_performance(self, clock):

        strings = [
            f'{1000 / clock.real_time.get_average_difs():.3f} fps',
            f'{1000 / clock.timer.get_average_difs():.0f} sps'
        ]

        self.text_column(strings, [self.WIDTH - self.STRING_PADDING, 0], left = False)

