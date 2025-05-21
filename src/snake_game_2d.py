import random
import time

# Global variables/constants for the game board
BOARD_WIDTH = 20
BOARD_HEIGHT = 20

# Helper functions
def get_random_position(board_width, board_height):
    """Returns a random (x,y) within board limits."""
    x = random.randint(0, board_width - 1)
    y = random.randint(0, board_height - 1)
    return (x, y)

def check_collision_wall(snake_head_position):
    """Takes the snake's head position (x,y) and returns True if it's outside
    BOARD_WIDTH or BOARD_HEIGHT, False otherwise."""
    x, y = snake_head_position
    if x < 0 or x >= BOARD_WIDTH or y < 0 or y >= BOARD_HEIGHT:
        return True
    return False

class Snake:
    def __init__(self, start_pos, start_length=3):
        """Initializes body segments (list of tuples (x, y)), initial direction."""
        self.body = [start_pos]  # Head is the first segment
        self.direction = "RIGHT"  # Initial direction
        self._should_grow = False # Flag for growth

        # Add initial segments to the left of the head, consistent with "RIGHT" initial direction
        # E.g. if start_pos=(2,0), length=3, body becomes [(2,0), (1,0), (0,0)]
        current_x, current_y = start_pos
        for i in range(1, start_length):
            self.body.append((current_x - i, current_y))

    def move(self):
        """Updates segment positions. The head moves one step in the current direction.
        Each subsequent segment takes the previous position of the segment in front of it."""
        head_x, head_y = self.body[0]
        
        if self.direction == "RIGHT":
            new_head_pos = (head_x + 1, head_y)
        elif self.direction == "LEFT":
            new_head_pos = (head_x - 1, head_y)
        elif self.direction == "UP": # (0,0) is top-left
            new_head_pos = (head_x, head_y - 1) 
        elif self.direction == "DOWN": # (0,0) is top-left
            new_head_pos = (head_x, head_y + 1)
        else: 
            new_head_pos = self.body[0] # Fallback, should ideally not happen

        # Insert new head
        self.body.insert(0, new_head_pos)

        # Remove tail if not growing
        if self._should_grow:
            self._should_grow = False  # Reset flag
        else:
            self.body.pop()

    def grow(self):
        """Sets a flag to make the snake grow on the next move."""
        self._should_grow = True

    def change_direction(self, new_direction):
        """Updates the snake's direction, preventing it from immediately reversing."""
        if new_direction == "RIGHT" and self.direction != "LEFT":
            self.direction = new_direction
        elif new_direction == "LEFT" and self.direction != "RIGHT":
            self.direction = new_direction
        elif new_direction == "UP" and self.direction != "DOWN":
            self.direction = new_direction
        elif new_direction == "DOWN" and self.direction != "UP":
            self.direction = new_direction

    def check_collision_self(self):
        """Returns True if the snake's head collides with its body, False otherwise."""
        if not self.body: 
            return False
        head = self.body[0]
        return head in self.body[1:]


class Food:
    def __init__(self, board_width, board_height, snake_body):
        """Initializes food at a random (x, y) position, ensuring it's not
        on the snake's body or outside board boundaries."""
        self.position = None 
        self.spawn(board_width, board_height, snake_body)

    def spawn(self, board_width, board_height, snake_body):
        """Respawns food at a new random valid location."""
        while True:
            new_pos = get_random_position(board_width, board_height)
            if new_pos not in snake_body: # Ensure food is not on snake
                self.position = new_pos
                break

if __name__ == '__main__':
    # Initialize Snake
    start_length = 3
    # Ensure start_pos allows for initial length without immediate out of bounds
    # Snake body is (start_x, y), (start_x-1, y), ..., (start_x - (length-1), y)
    # So, start_x - (length-1) must be >= 0.  start_x >= length - 1
    min_start_x = start_length - 1
    
    # Place snake somewhat centrally but ensure it fits
    start_x = max(min_start_x, BOARD_WIDTH // 4) 
    start_y = BOARD_HEIGHT // 2
    
    snake = Snake(start_pos=(start_x, start_y), start_length=start_length)

    # Initialize Food
    food = Food(BOARD_WIDTH, BOARD_HEIGHT, snake.body)

    print(f"Initial Snake: {snake.body} (Head: {snake.body[0]})")
    print(f"Initial Food: {food.position}")
    print(f"Board Size: {BOARD_WIDTH}x{BOARD_HEIGHT}")
    print("Starting game loop... (Ctrl+C to stop if it runs too long or reaches max_turns)")
    print("---")

    game_running = True
    turn_count = 0
    max_turns = 100 # Safety break for the loop in this basic console environment

    while game_running and turn_count < max_turns:
        turn_count += 1
        
        # (Placeholder) Get user input to change snake direction
        # Simple automatic turning logic for testing:
        # Try to make snake circle around near the edges for more comprehensive testing
        head_x, head_y = snake.body[0]
        if snake.direction == "RIGHT" and head_x >= BOARD_WIDTH - 2:
            snake.change_direction("DOWN")
        elif snake.direction == "DOWN" and head_y >= BOARD_HEIGHT - 2:
            snake.change_direction("LEFT")
        elif snake.direction == "LEFT" and head_x <= 1: # Allow reaching 0 before turning
            snake.change_direction("UP")
        elif snake.direction == "UP" and head_y <= 1: # Allow reaching 0 before turning
            snake.change_direction("RIGHT")
        # Fallback: Periodically change direction if no edge is hit, to ensure movement changes
        elif turn_count % 15 == 0: 
            dirs = ["RIGHT", "DOWN", "LEFT", "UP"]
            current_dir_index = dirs.index(snake.direction)
            # Try to turn right relative to current direction
            snake.change_direction(dirs[(current_dir_index + 1) % 4])


        # Call snake.move()
        snake.move()

        # Check if snake head is at food position
        if snake.body[0] == food.position:
            print(f"Turn {turn_count}: Food eaten at {food.position}!")
            snake.grow()
            food.spawn(BOARD_WIDTH, BOARD_HEIGHT, snake.body)
            print(f"Turn {turn_count}: New Food at: {food.position}. Snake length: {len(snake.body)}")

        # Check for wall collision
        if check_collision_wall(snake.body[0]):
            print(f"Turn {turn_count}: Game Over - Wall Collision")
            print(f"Snake hit wall at: {snake.body[0]}")
            game_running = False
        
        # Check for self-collision (only if game still running)
        if game_running and snake.check_collision_self():
            print(f"Turn {turn_count}: Game Over - Self Collision")
            print(f"Snake collided with itself. Head: {snake.body[0]}, Body: {snake.body}")
            game_running = False
            
        if game_running:
            # (Placeholder) Print the game state
            # Print only head and food for brevity in logs, unless snake is very short
            snake_display = snake.body if len(snake.body) < 5 else f"{snake.body[0]}...{snake.body[-1]}"
            print(f"Turn {turn_count}: Head: {snake.body[0]} (L:{len(snake.body)},D:{snake.direction}) Food: {food.position}")
            # print(f"Turn {turn_count}: Snake: {snake_display} (Dir: {snake.direction}) Food: {food.position}")
            # print("---") # Reduce noise
        
        # Add a small delay
        time.sleep(0.1) # Slightly faster for testing, 0.2 is also fine
    
    print("---")
    print("Game Ended.")
    if turn_count >= max_turns:
        print(f"Reached max turns ({max_turns}).")
    print(f"Final Snake: {snake.body}")
    print(f"Final Food: {food.position}")
    print(f"Final Snake Length: {len(snake.body)}")
