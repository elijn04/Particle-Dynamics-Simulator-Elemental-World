"""
    Filename: Newman_project3part1_sandgame.py

    Description of program: 
    This program simulates a sand world where sand 
    particles can be added and will fall under the influence of gravity.
    Users can interact with the simulation by clicking to add sand particles, 
    which will then settle down in the grid.
    The program uses a graphical library (dudraw) to visualize the sand world 
    and update the display in real-time.

    Author: Eli Newman
    Date: 2025-02-11
    Course: CS 1351 
    Assignment: Project 3 (sand Project) Part 2
    Collaborators: None
    Internet Source: Dudraw documentation
"""

import dudraw
import random
import time

# Particle type constants
EMPTY = 0
SAND = 1
RAIN = 2  
FLOOR = 3
FIRE = 4
EMBER = 5
OIL = 6
SNOW = 7

# Create and initialize the sand world
def create_world(size: int) -> list[list[int]]:
    """
    Creates an empty simulation grid.
    
    Args:
        size: dimension of the square grid
        
    Returns:
        list[list[int]]: 2D list representing empty simulation grid
    """
    return [[EMPTY for _ in range(size)] for _ in range(size)]

# Draw the sand world
def draw_world(world: list[list[int]]) -> None:
    """
    Draws the current state of the simulation.
    
    Args:
        world: 2D list representing the simulation grid
    """
    size = len(world)
    dudraw.clear(dudraw.BLACK)
    for i in range(size):
        for j in range(size):
            if world[i][j] == SAND:
                dudraw.set_pen_color(dudraw.YELLOW)
                dudraw.filled_square(j + 0.5, size - i - 0.5, 0.5)
            elif world[i][j] == RAIN:
                dudraw.set_pen_color(dudraw.BLUE)
                dudraw.filled_square(j + 0.5, size - i - 0.5, 0.5)
            elif world[i][j] == FLOOR:
                dudraw.set_pen_color(dudraw.GRAY)
                dudraw.filled_square(j + 0.5, size - i - 0.5, 0.5)
            elif world[i][j] == FIRE:
                # Main fire
                r = int(random.uniform(0.8, 1.0) * 255)
                g = int(0.4 * 255)
                b = 0
                dudraw.set_pen_color_rgb(r, g, b)
                dudraw.filled_square(j + 0.5, size - i - 0.5, 0.5)
                
                # Side flame particles
                if random.random() < 0.3:
                    flame_colors = [
                        (255, 0, 0),    # Red
                        (255, 178, 0),  # Yellow
                        (255, 128, 0)   # Orange
                    ]
                    color = random.choice(flame_colors)
                    dudraw.set_pen_color_rgb(*color)
                    offset = random.uniform(-0.3, 0.3)
                    dudraw.filled_circle(j + 0.5 + offset, size - i - 0.2, 0.2)
            elif world[i][j] == EMBER:
                # Draw rising embers
                ember_colors = [
                    (255, 100, 0),   # Orange
                    (200, 80, 0),    # Dark orange
                    (150, 150, 150)  # Smoke gray
                ]
                color = random.choice(ember_colors)
                dudraw.set_pen_color_rgb(*color)
                offset_x = random.uniform(-0.2, 0.2)
                dudraw.filled_circle(j + 0.5 + offset_x, size - i - 0.5, 0.15)
            elif world[i][j] == OIL:
                dudraw.set_pen_color_rgb(139, 69, 19)  # Brown color for oil
                dudraw.filled_square(j + 0.5, size - i - 0.5, 0.5)
            elif world[i][j] == SNOW:
                dudraw.set_pen_color(dudraw.WHITE)
                dudraw.filled_square(j + 0.5, size - i - 0.5, 0.5)
    
    dudraw.show()

class ParticleCreator:
    """
    Handles the creation of different particle types in the simulation.
    """
    
    def create_sand(self, world: list[list[int]], x: int, y: int) -> None:
        """
        Creates sand particles in a small radius around the given position.
        
        Args:
            world: 2D list representing the simulation grid
            x: x-coordinate for particle placement
            y: y-coordinate for particle placement
        """
        size = len(world)
        for _ in range(5):
            # Random spread in both directions
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            nx, ny = x + dx, y + dy
            # Only place in empty spaces
            if (0 <= nx < size and 0 <= ny < size and 
                world[ny][nx] == EMPTY):
                world[ny][nx] = SAND
    
    def create_rain(self, world: list[list[int]], x: int, y: int) -> None:
        """
        Creates rain particles in a wider horizontal spread.
        
        Args:
            world: 2D list representing the simulation grid
            x: x-coordinate for particle placement
            y: y-coordinate for particle placement
        """
        size = len(world)
        for _ in range(5):
            dx = random.randint(-4, 4)
            dy = random.randint(-1, 1)
            nx, ny = x + dx, y + dy
            if (0 <= nx < size and 0 <= ny < size and 
                world[ny][nx] == EMPTY):
                world[ny][nx] = RAIN
    
    def create_fire(self, world: list[list[int]], x: int, y: int, fire_timers: dict) -> None:
        """
        Creates fire particles in a small radius with timing information.
        
        Args:
            world: 2D list representing the simulation grid
            x: x-coordinate for fire placement
            y: y-coordinate for fire placement
            fire_timers: dictionary tracking fire particle lifetimes
        """
        size = len(world)
        for _ in range(3):
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            nx, ny = x + dx, y + dy
            if (0 <= nx < size and 0 <= ny < size and 
                world[ny][nx] == EMPTY):
                world[ny][nx] = FIRE
                fire_timers[(ny,nx)] = time.time()
    
    def create_floor(self, world: list[list[int]], x: int, y: int) -> None:
        """
        Creates a solid 7x3 floor block centered at the given position.
        
        Args:
            world: 2D list representing the simulation grid
            x: x-coordinate for floor center
            y: y-coordinate for floor bottom
        """
        size = len(world)
        for dy in range(3):
            for dx in range(-3, 4):
                nx = x + dx
                ny = y + dy
                if 0 <= nx < size and 0 <= ny < size:
                    world[ny][nx] = FLOOR
    
    def can_place_floor(self, world: list[list[int]], x: int, y: int) -> bool:
        """
        Checks if a 7x3 floor block can be placed without overlapping other particles.
        
        Args:
            world: 2D list representing the simulation grid
            x: x-coordinate for floor center
            y: y-coordinate for floor bottom
        
        Returns:
            bool: True if floor can be placed, False if space is occupied
        """
        size = len(world)
        for dy in range(3):
            for dx in range(-3, 4):
                nx = x + dx
                ny = y + dy
                if (0 <= nx < size and 0 <= ny < size and 
                    world[ny][nx] != EMPTY):
                    return False
        return True
    
    def create_oil(self, world: list[list[int]], x: int, y: int) -> None:
        """
        Creates oil particles in a wide horizontal spread.
        
        Args:
            world: 2D list representing the simulation grid
            x: x-coordinate for oil placement
            y: y-coordinate for oil placement
        """
        size = len(world)
        for _ in range(5):
            dx = random.randint(-3, 3)
            dy = random.randint(-1, 1)
            nx, ny = x + dx, y + dy
            if (0 <= nx < size and 0 <= ny < size and 
                world[ny][nx] == EMPTY):
                world[ny][nx] = OIL
    
    def create_snow(self, world: list[list[int]], x: int, y: int) -> None:
        """
        Creates snow particles in a small radius around the given position.
        
        Args:
            world: 2D list representing the simulation grid
            x: x-coordinate for snow placement
            y: y-coordinate for snow placement
        """
        size = len(world)
        for _ in range(5):
            dx = random.randint(-2, 2)
            dy = random.randint(-2, 2)
            nx, ny = x + dx, y + dy
            if (0 <= nx < size and 0 <= ny < size and 
                world[ny][nx] == EMPTY):
                world[ny][nx] = SNOW

class ParticleMovement:
    """
    Handles movement mechanics for all particle types.
    """
    
    def apply_gravity(self, world: list[list[int]], i: int, j: int, particle_type: int) -> bool:
        """
        Applies gravity to a particle, making it fall if possible.
        
        Args:
            world: 2D list representing the simulation grid
            i: current row index
            j: current column index
            particle_type: type of particle to move
            
        Returns:
            bool: True if particle moved down, False otherwise
        """
        size = len(world)
        if i < size-1 and world[i+1][j] == EMPTY:
            world[i][j] = EMPTY
            world[i+1][j] = particle_type
            return True
        return False
    
    def move_sideways(self, world: list[list[int]], i: int, j: int, particle_type: int) -> bool:
        """
        Attempts to move a particle diagonally down-left or down-right.
        
        Args:
            world: 2D list representing the simulation grid
            i: current row index
            j: current column index
            particle_type: type of particle to move
            
        Returns:
            bool: True if particle moved diagonally, False otherwise
        """
        size = len(world)
        direction = random.choice([-1, 1])
        if (j + direction >= 0 and j + direction < size and 
            world[i + 1][j + direction] == EMPTY):
            world[i][j] = EMPTY
            world[i + 1][j + direction] = particle_type
            return True
        return False
    
    def move_ember(self, world: list[list[int]], i: int, j: int) -> None:
        size = len(world)
        if random.random() < 0.3:
            new_j = j + random.choice([-1, 1]) if random.random() < 0.2 else j
            if (i > 0 and 0 <= new_j < size and 
                world[i-1][new_j] == EMPTY):
                world[i][j] = EMPTY
                world[i-1][new_j] = EMBER
            elif (i == 0 or world[i-1][j] != EMPTY):
                world[i][j] = EMPTY
    
    def float_up(self, world: list[list[int]], i: int, j: int, particle_type: int) -> bool:
        """Makes particles float up through specific materials"""
        size = len(world)
        # Check if particle can float up through water
        if i > 0 and world[i-1][j] == RAIN:
            world[i][j] = RAIN
            world[i-1][j] = particle_type
            return True
        return False
    
    def flow_to_lowest_point(self, world: list[list[int]], i: int, j: int, particle_type: int) -> bool:
        """
        Makes liquid particles flow towards the lowest available point.
        
        Args:
            world: 2D list representing the simulation grid
            i: current row index
            j: current column index
            particle_type: type of particle to move
            
        Returns:
            bool: True if particle moved, False otherwise
        """
        size = len(world)
        moved = False
        
        # Try to move straight down first
        if i < size-1 and world[i+1][j] == EMPTY:
            world[i][j] = EMPTY
            world[i+1][j] = particle_type
            return True
            
        # If can't move down, try diagonal movement
        for dx in [-1, 1]:  # Check both left and right
            if (i < size-1 and 0 <= j + dx < size and 
                world[i+1][j+dx] == EMPTY):
                world[i][j] = EMPTY
                world[i+1][j+dx] = particle_type
                return True
        
        # If can't move down or diagonal, try horizontal spread
        for dx in [-1, 1]:
            if (0 <= j + dx < size and 
                world[i][j+dx] == EMPTY):
                world[i][j] = EMPTY
                world[i][j+dx] = particle_type
                return True
                
        return False

class ParticleInteraction:
    """
    Handles interactions between different particle types.
    """
    
    def __init__(self):
        self.movement = ParticleMovement()
    
    def handle_sand(self, world: list[list[int]], i: int, j: int) -> None:
        """
        Handles sand particle movement and interactions.
        
        Args:
            world: 2D list representing the simulation grid
            i: current row index
            j: current column index
        """
        if not self.movement.apply_gravity(world, i, j, SAND):
            if world[i + 1][j] == RAIN:
                world[i][j] = EMPTY
                world[i + 1][j] = SAND
            else:
                self.movement.move_sideways(world, i, j, SAND)
    
    def handle_rain(self, world: list[list[int]], i: int, j: int) -> None:
        """
        Handles rain particle movement and interactions.
        
        Args:
            world: 2D list representing the simulation grid
            i: current row index
            j: current column index
        """
        size = len(world)
        if i + 1 < size:
            # If water hits fire, extinguish it and continue flowing
            if world[i + 1][j] == FIRE:
                world[i][j] = EMPTY
                world[i + 1][j] = RAIN
                return
            
            if world[i + 1][j] == EMPTY:
                world[i][j] = EMPTY
                world[i + 1][j] = RAIN
            elif world[i + 1][j] == RAIN or world[i + 1][j] == SAND:
                for direction in [-1, 1]:
                    if (0 <= j + direction < size and 
                        world[i][j + direction] == EMPTY):
                        world[i][j] = EMPTY
                        world[i][j + direction] = RAIN
                        break
    
    def handle_oil(self, world: list[list[int]], i: int, j: int) -> None:
        size = len(world)
        
        # Check oil layer limit (max 2)
        if i < size-1 and world[i+1][j] == OIL:
            if i < size-2 and world[i+2][j] == OIL:
                world[i][j] = EMPTY
                return
        
        # Float on water
        if self.movement.float_up(world, i, j, OIL):
            return
            
        # Flow to lowest point
        self.movement.flow_to_lowest_point(world, i, j, OIL)
    
    def spread_fire_through_oil(self, world: list[list[int]], i: int, j: int, fire_timers: dict) -> None:
        """Recursively spread fire through connected oil particles"""
        size = len(world)
        current_time = time.time()
        
        # Check all adjacent cells for oil
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if (0 <= ni < size and 0 <= nj < size and 
                    world[ni][nj] == OIL):
                    world[ni][nj] = FIRE
                    fire_timers[(ni,nj)] = current_time
                    # Recursively spread to connected oil
                    self.spread_fire_through_oil(world, ni, nj, fire_timers)
    
    def check_fire_interactions(self, world: list[list[int]], i: int, j: int, fire_timers: dict) -> bool:
        """
        Checks and handles fire interactions with water and oil.
        
        Args:
            world: 2D list representing the simulation grid
            i: current row index
            j: current column index
            fire_timers: dictionary tracking fire particle lifetimes
            
        Returns:
            bool: True if fire was extinguished or spread, False otherwise
        """
        size = len(world)
        
        # Check all adjacent cells for water or oil
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if 0 <= ni < size and 0 <= nj < size:
                    # If water is touching fire, extinguish fire
                    if world[ni][nj] == RAIN:
                        world[i][j] = EMPTY
                        del fire_timers[(i,j)]
                        return True
                    # If oil is touching fire, convert oil to fire
                    elif world[ni][nj] == OIL:
                        world[ni][nj] = FIRE
                        fire_timers[(ni,nj)] = time.time()
                        self.spread_fire_through_oil(world, ni, nj, fire_timers)
        return False

    def handle_fire(self, world: list[list[int]], i: int, j: int, fire_timers: dict) -> None:
        """
        Handles fire particle behavior, timing, and interactions.
        
        Args:
            world: 2D list representing the simulation grid
            i: current row index
            j: current column index
            fire_timers: dictionary tracking fire particle lifetimes
        """
        size = len(world)
        current_time = time.time()
        
        if (i,j) not in fire_timers:
            fire_timers[(i,j)] = current_time
        
        # Check for water/oil interactions first
        if self.check_fire_interactions(world, i, j, fire_timers):
            return
        
        # Normal fire behavior
        if current_time - fire_timers[(i,j)] > 6:
            world[i][j] = EMPTY
            del fire_timers[(i,j)]
            return
        
        if random.random() < 0.02 and i > 0 and world[i-1][j] == EMPTY:
            world[i-1][j] = EMBER
        
        if i >= size - 1:
            return
            
        if world[i + 1][j] == EMPTY:
            world[i][j] = EMPTY
            world[i + 1][j] = FIRE
            fire_timers[(i+1,j)] = fire_timers.pop((i,j))
        else:
            self.movement.move_sideways(world, i, j, FIRE)
    
    def handle_snow(self, world: list[list[int]], i: int, j: int, snow_timers: dict) -> None:
        """
        Handles snow particle movement, melting, and interactions.
        
        Args:
            world: 2D list representing the simulation grid
            i: current row index
            j: current column index
            snow_timers: dictionary tracking snow melting times
        """
        size = len(world)
        current_time = time.time()
        
        if (i,j) not in snow_timers:
            snow_timers[(i,j)] = current_time
        
        # Check for nearby fire
        melt_speed = 1.0
        for di in [-1, 0, 1]:
            for dj in [-1, 0, 1]:
                ni, nj = i + di, j + dj
                if (0 <= ni < size and 0 <= nj < size and 
                    world[ni][nj] == FIRE):
                    melt_speed = 5.0
                    break
        
        # Melt snow into water
        if current_time - snow_timers[(i,j)] > (5.0 / melt_speed):
            world[i][j] = RAIN
            del snow_timers[(i,j)]
            return
            
        # Move through liquids or fall
        if i < size-1:
            if world[i+1][j] == EMPTY:
                world[i][j] = EMPTY
                world[i+1][j] = SNOW
            elif world[i+1][j] in [RAIN, OIL]:
                # Store the liquid type
                liquid = world[i+1][j]
                # Swap positions
                world[i+1][j] = SNOW
                world[i][j] = liquid
            else:
                self.movement.move_sideways(world, i, j, SNOW)

def update_particles(world: list[list[int]], fire_timers: dict, snow_timers: dict) -> None:
    """
    Updates all particles in the simulation for one time step.
    
    Args:
        world: 2D list representing the simulation grid
        fire_timers: dictionary tracking fire particle lifetimes
        snow_timers: dictionary tracking snow particle melting times
    """
    size = len(world)
    movement = ParticleMovement()
    interaction = ParticleInteraction()
    
    # Update embers
    for i in range(size-1):
        for j in range(size):
            if world[i][j] == EMBER:
                movement.move_ember(world, i, j)
    
    # Update from bottom to top for proper particle movement
    for i in range(size-2, -1, -1):
        for j in range(size-1, -1, -1):
            # Handle each particle type
            if world[i][j] == SAND:
                interaction.handle_sand(world, i, j)
            elif world[i][j] == RAIN:
                interaction.handle_rain(world, i, j)
            elif world[i][j] == FIRE:
                interaction.handle_fire(world, i, j, fire_timers)
            elif world[i][j] == OIL:
                interaction.handle_oil(world, i, j)
            elif world[i][j] == SNOW:
                interaction.handle_snow(world, i, j, snow_timers)

def draw_button(mode: int) -> None:
    """
    Draws the mode selection and clear buttons.
    
    Args:
        mode: Current particle type selected
    """
    # Draw mode button background
    dudraw.set_pen_color(dudraw.GRAY)
    dudraw.filled_rectangle(10, 95, 8, 3)
    
    # Draw mode button text
    dudraw.set_pen_color(dudraw.WHITE)
    if mode == SAND:
        dudraw.text(10, 95, "Mode: SAND")
    elif mode == RAIN:
        dudraw.text(10, 95, "Mode: RAIN")
    elif mode == FLOOR:
        dudraw.text(10, 95, "Mode: FLOOR")
    elif mode == FIRE:
        dudraw.text(10, 95, "Mode: FIRE")
    elif mode == OIL:
        dudraw.text(10, 95, "Mode: OIL")
    elif mode == SNOW:
        dudraw.text(10, 95, "Mode: SNOW")
    
    # Draw clear button in top right
    dudraw.set_pen_color(dudraw.RED)
    dudraw.filled_rectangle(95, 95, 4, 2)
    dudraw.set_pen_color(dudraw.WHITE)
    dudraw.text(95, 95, "Clear")

def is_button_clicked(mouse_x: float, mouse_y: float) -> tuple[bool, bool]:
    """
    Checks if mode or clear buttons were clicked.
    
    Args:
        mouse_x: x-coordinate of mouse click
        mouse_y: y-coordinate of mouse click
        
    Returns:
        tuple[bool, bool]: (mode_clicked, clear_clicked)
    """
    mode_clicked = (2 <= mouse_x <= 18 and 92 <= mouse_y <= 98)
    clear_clicked = (91 <= mouse_x <= 99 and 93 <= mouse_y <= 97)  # Updated clear button hitbox
    return (mode_clicked, clear_clicked)

def main():
    """
    Main function that runs the simulation loop.
    Handles:
    - Window setup
    - User input
    - Particle updates
    - Drawing
    """
    size = 100
    world = create_world(size)
    dudraw.set_canvas_size(500, 500)
    dudraw.set_x_scale(0, size)
    dudraw.set_y_scale(0, size)
    
    # Initialize state variables
    current_mode = SAND
    fire_timers = {}
    snow_timers = {}
    creator = ParticleCreator()
    
    # Main game loop
    while True:
        time.sleep(0.02)  # Control simulation speed
        
        # Handle user input
        if dudraw.mouse_is_pressed():
            mouse_x = dudraw.mouse_x()
            mouse_y = dudraw.mouse_y()
            
            mode_clicked, clear_clicked = is_button_clicked(mouse_x, mouse_y)
            
            # Handle button clicks
            if mode_clicked:
                # Cycle through particle types
                if current_mode == SAND:
                    current_mode = RAIN
                elif current_mode == RAIN:
                    current_mode = FLOOR
                elif current_mode == FLOOR:
                    current_mode = FIRE
                elif current_mode == FIRE:
                    current_mode = OIL
                elif current_mode == OIL:
                    current_mode = SNOW
                else:
                    current_mode = SAND
                time.sleep(0.2)
            elif clear_clicked:
                world = create_world(size)
                fire_timers.clear()
                snow_timers.clear()
                time.sleep(0.2)
            else:
                x = int(mouse_x)
                y = size - int(mouse_y)
                
                if current_mode == FLOOR:
                    if creator.can_place_floor(world, x, y):
                        creator.create_floor(world, x, y)
                elif current_mode == FIRE:
                    creator.create_fire(world, x, y, fire_timers)
                elif current_mode == RAIN:
                    creator.create_rain(world, x, y)
                elif current_mode == OIL:
                    creator.create_oil(world, x, y)
                elif current_mode == SNOW:
                    creator.create_snow(world, x, y)
                else:  # SAND
                    creator.create_sand(world, x, y)
        
        if dudraw.has_next_key_typed():
            if dudraw.next_key_typed() == 'q':
                break
        
        update_particles(world, fire_timers, snow_timers)
        draw_world(world)
        draw_button(current_mode)
        dudraw.show()

if __name__ == "__main__":
    main()