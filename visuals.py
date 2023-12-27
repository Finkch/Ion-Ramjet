import numpy as np
import spacecraft as sc
import finkchlib.vector as v

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
        self.line((self.PIXEL_PADDING, self.HEIGHT / 2), (self.WIDTH - self.PIXEL_PADDING, self.HEIGHT / 2), self.GREY4)
        self.line((self.WIDTH / 2, self.PIXEL_PADDING), (self.WIDTH / 2, self.HEIGHT - self.PIXEL_PADDING), self.GREY4)

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
    