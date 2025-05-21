import random
from enum import Enum
from ursina import *
# from ursina.prefabs.first_person_controller import FirstPersonController # Or EditorCamera

# --- Game Configuration ---
BOARD_WIDTH = 10
BOARD_HEIGHT = 10
BOARD_DEPTH = 10
GAME_SPEED_INITIAL = 0.20
ORIGINAL_GAME_SPEED = GAME_SPEED_INITIAL # For power-up logic
BOOSTED_GAME_SPEED = ORIGINAL_GAME_SPEED / 2.0
SPEED_BOOST_DURATION = 5.0


# --- Game States ---
class GameState(Enum):
    START_SCREEN = 1
    PLAYING = 2
    GAME_OVER = 3

current_state = GameState.START_SCREEN

# --- Asset Paths & Directions ---
DIRECTIONS = {
    "RIGHT_X": (1, 0, 0), "LEFT_X": (-1, 0, 0),
    "UP_Y": (0, 1, 0), "DOWN_Y": (0, -1, 0),
    "FORWARD_Z": (0, 0, 1), "BACKWARD_Z": (0, 0, -1),
}
SNAKE_HEAD_MODEL = 'assets/models/snake_head.obj'
SNAKE_SEGMENT_MODEL = 'assets/models/snake_segment.obj'
SNAKE_TEXTURE = 'assets/textures/snake_skin.png'
FOOD_MODEL = 'assets/models/food.obj'
FOOD_TEXTURE = 'assets/textures/food_texture.png'
WALL_TEXTURE = 'assets/textures/wall_texture.png'

# --- Audio Assets ---
eat_sound = Audio('assets/sounds/eat_food.wav', autoplay=False, loop=False)
game_over_sound = Audio('assets/sounds/game_over.wav', autoplay=False, loop=False)
powerup_collect_sound = Audio('assets/sounds/powerup_collect.wav', autoplay=False, loop=False)
background_music = Audio('assets/sounds/background_music.ogg', loop=True, autoplay=True, volume=0.5)


# --- Power-up Variables ---
powerup_item_entity = None
is_powerup_item_active = False # Is the power-up item currently spawned
powerup_spawn_timer = 5.0    # Time until next power-up spawn attempt
speed_boost_active = False     # Is the speed boost currently active
speed_boost_timer = 0.0        # Remaining duration of the speed boost


# --- Helper Functions ---
def game_to_ursina_pos(game_pos):
    return (
        game_pos[0] - BOARD_WIDTH / 2 + 0.5,
        game_pos[1] - BOARD_HEIGHT / 2 + 0.5,
        game_pos[2] - BOARD_DEPTH / 2 + 0.5,
    )

def get_random_position_safe(board_width, board_height, board_depth, snake_body, food_pos, current_powerup_pos=None):
    """Gets a random position ensuring it's not on snake, food, or existing powerup."""
    while True:
        pos = get_random_position(board_width, board_height, board_depth)
        if pos not in snake_body and pos != food_pos and (current_powerup_pos is None or pos != current_powerup_pos):
            return pos

def get_random_position(board_width, board_height, board_depth): # Original remains for Food
    x = random.randint(0, board_width - 1)
    y = random.randint(0, board_height - 1)
    z = random.randint(0, board_depth - 1)
    return (x, y, z)

def check_collision_wall(snake_head_position):
    x, y, z = snake_head_position
    return not (0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT and 0 <= z < BOARD_DEPTH)

# --- Game Object Classes ---
class Snake: # (No changes to Snake class for this feature)
    def __init__(self, start_pos, start_length=3, initial_direction_vector=(1,0,0)):
        self.start_pos_init = start_pos
        self.start_length_init = start_length
        self.initial_direction_vector_init = initial_direction_vector
        self.normal_segment_scale = Vec3(1,1,1)
        self.entities = []
        self.reset() 

    def reset(self):
        self.destroy_entities() 
        self.body = [self.start_pos_init]
        self.direction = self.initial_direction_vector_init
        self._should_grow = False
        
        current_x, current_y, current_z = self.start_pos_init
        inv_dx, inv_dy, inv_dz = -self.direction[0], -self.direction[1], -self.direction[2]
        for i in range(1, self.start_length_init):
            self.body.append((current_x + inv_dx * i, current_y + inv_dy * i, current_z + inv_dz * i))
        
        for i, segment_pos in enumerate(self.body):
            model_path = SNAKE_HEAD_MODEL if i == 0 else SNAKE_SEGMENT_MODEL
            entity = Entity(
                model=model_path, texture=SNAKE_TEXTURE,
                scale=self.normal_segment_scale,
                position=game_to_ursina_pos(segment_pos),
                collider='box', enabled=False 
            )
            self.entities.append(entity)

    def move(self):
        global game_speed 
        head_x, head_y, head_z = self.body[0]
        dx, dy, dz = self.direction
        new_head_pos = (head_x + dx, head_y + dy, head_z + dz)
        self.body.insert(0, new_head_pos)
        
        if self._should_grow:
            new_head_entity = Entity(
                model=SNAKE_HEAD_MODEL, texture=SNAKE_TEXTURE,
                scale=Vec3(0,0,0), position=game_to_ursina_pos(new_head_pos),
                enabled=self.entities[0].enabled if self.entities else True 
            )
            new_head_entity.animate_scale(self.normal_segment_scale, duration=game_speed * 2)
            self.entities.insert(0, new_head_entity)
            self._should_grow = False
        else:
            if self.entities:
                tail_entity = self.entities.pop()
                destroy(tail_entity)
            self.body.pop()

        for i, segment_pos in enumerate(self.body):
            if i < len(self.entities): 
                 self.entities[i].animate_position(game_to_ursina_pos(segment_pos), duration=game_speed * 0.9)

    def grow(self): self._should_grow = True
    def change_direction(self, new_direction_vector):
        if not (new_direction_vector[0] == -self.direction[0] and \
                new_direction_vector[1] == -self.direction[1] and \
                new_direction_vector[2] == -self.direction[2]):
            self.direction = new_direction_vector
    def check_collision_self(self):
        if not self.body: return False
        return self.body[0] in self.body[1:]
    def destroy_entities(self):
        for entity in self.entities: destroy(entity)
        self.entities = []
    def set_visibility(self, visible):
        for entity in self.entities: entity.enabled = visible

class Food: # (No changes to Food class for this feature, except using get_random_position_safe if needed)
    def __init__(self, board_width, board_height, board_depth, snake_body_initial):
        self.board_width = board_width
        self.board_height = board_height
        self.board_depth = board_depth
        self.original_scale = Vec3(1,1,1)
        self.entity = Entity(model=FOOD_MODEL, texture=FOOD_TEXTURE, scale=self.original_scale, enabled=False)
        self.spawn(snake_body_initial) 

    def spawn(self, snake_body):
        # Food can spawn where a powerup is, that's fine.
        new_pos = get_random_position(self.board_width, self.board_height, self.board_depth)
        while new_pos in snake_body: # Ensure not on snake
            new_pos = get_random_position(self.board_width, self.board_height, self.board_depth)
        self.position = new_pos
        self.entity.position = game_to_ursina_pos(self.position)

    def reset(self, snake_body): 
        self.spawn(snake_body)
    def destroy_entity(self):
        if self.entity: destroy(self.entity)
    def set_visibility(self, visible):
        self.entity.enabled = visible

# --- UI Elements & Game Variables (largely unchanged) ---
app = Ursina(title='3D Snake Game - Power Ups!')
start_screen_ui, game_play_ui, game_over_ui = [], [], []
title_text = Text(text='3D SNAKE!', origin=(0,0), scale=3, y=0.2, enabled=False); start_screen_ui.append(title_text)
instructions_text = Text(text='Use Arrows for X/Y, W/S for Z\n\nPress Enter to Start', origin=(0,0), y=-0.1, scale=2, enabled=False, textAlign='center'); start_screen_ui.append(instructions_text)
score_text = Text(text='Score: 0', position=(-0.65, 0.45), scale=1.5, origin=(0,0), enabled=False); game_play_ui.append(score_text)
game_over_title_text = Text(text='GAME OVER', origin=(0,0), scale=4, y=0.2, color=color.red, enabled=False); game_over_ui.append(game_over_title_text)
final_score_text = Text(text='Final Score: 0', origin=(0,0), scale=2, y=0, enabled=False); game_over_ui.append(final_score_text)
restart_instructions_text = Text(text='Press R to Restart', origin=(0,0), y=-0.2, scale=2, enabled=False); game_over_ui.append(restart_instructions_text)

score = 0
game_speed = GAME_SPEED_INITIAL # This will be modified by power-up
time_since_last_step = 0
snake_start_pos_init = (BOARD_WIDTH // 2, BOARD_HEIGHT // 2, BOARD_DEPTH // 2)
snake = Snake(start_pos=snake_start_pos_init, start_length=3)
food = Food(BOARD_WIDTH, BOARD_HEIGHT, BOARD_DEPTH, snake.body)

# --- Power-up Function ---
def spawn_powerup():
    global powerup_item_entity, is_powerup_item_active, snake, food
    if powerup_item_entity:
        destroy(powerup_item_entity)
    
    # Use get_random_position_safe to avoid snake and food
    spawn_pos_logical = get_random_position_safe(BOARD_WIDTH, BOARD_HEIGHT, BOARD_DEPTH, snake.body, food.position)
    
    powerup_item_entity = Entity(
        model='sphere', # Simple sphere for power-up
        color=color.azure,
        position=game_to_ursina_pos(spawn_pos_logical),
        scale=food.original_scale # Same scale as food
    )
    is_powerup_item_active = True

# --- Game Logic Functions ---
def reset_game():
    global score, snake, food, time_since_last_step, game_speed
    global powerup_item_entity, is_powerup_item_active, speed_boost_active, powerup_spawn_timer, speed_boost_timer

    score = 0
    score_text.text = f'Score: {score}'
    time_since_last_step = 0
    game_speed = ORIGINAL_GAME_SPEED # Reset game speed
    
    start_length = 3
    initial_direction_vec = DIRECTIONS["RIGHT_X"]
    min_coord_vals = [(start_length - 1) * abs(d_val) for d_val in initial_direction_vec]
    start_x = max(min_coord_vals[0], BOARD_WIDTH // 2) 
    start_y = max(min_coord_vals[1], BOARD_HEIGHT // 2)
    start_z = max(min_coord_vals[2], BOARD_DEPTH // 2)
    
    snake.start_pos_init = (start_x, start_y, start_z)
    snake.start_length_init = start_length
    snake.initial_direction_vector_init = initial_direction_vec
    snake.reset() 
    food.reset(snake.body) 

    # Reset power-up state
    if powerup_item_entity:
        destroy(powerup_item_entity)
        powerup_item_entity = None
    is_powerup_item_active = False
    speed_boost_active = False
    powerup_spawn_timer = 5.0 # Initial delay for first power-up
    speed_boost_timer = 0.0


def set_game_state(new_state):
    global current_state, score, powerup_item_entity, is_powerup_item_active, speed_boost_active
    
    for ui_element in start_screen_ui + game_play_ui + game_over_ui:
        ui_element.enabled = False

    current_state = new_state

    if new_state == GameState.START_SCREEN:
        for ui_element in start_screen_ui: ui_element.enabled = True
        snake.set_visibility(False)
        food.set_visibility(False)
        if powerup_item_entity: powerup_item_entity.enabled = False
    elif new_state == GameState.PLAYING:
        reset_game() # This handles power-up reset too
        for ui_element in game_play_ui: ui_element.enabled = True
        snake.set_visibility(True)
        food.set_visibility(True)
        # Power-up entity will be spawned by its timer logic in update
    elif new_state == GameState.GAME_OVER:
        final_score_text.text = f'Final Score: {score}'
        for ui_element in game_over_ui: ui_element.enabled = True
        snake.set_visibility(False)
        food.set_visibility(False)
        if powerup_item_entity: powerup_item_entity.enabled = False # Hide active powerup
        # Reset active speed boost effect immediately
        is_powerup_item_active = False # Ensure no new powerups spawn
        speed_boost_active = False
        global game_speed
        game_speed = ORIGINAL_GAME_SPEED


def trigger_game_over_animations(): # (Unchanged)
    global snake
    for segment_entity in snake.entities:
        segment_entity.animate_color(color.red, duration=0.3)
        segment_entity.animate_scale(segment_entity.scale * 1.2, duration=0.3) 
        segment_entity.animate_color(color.clear, duration=0.5, delay=0.6)

def update():
    global current_state, time_since_last_step, snake, food, score, game_speed
    global eat_sound, game_over_sound, powerup_collect_sound
    global powerup_item_entity, is_powerup_item_active, powerup_spawn_timer
    global speed_boost_active, speed_boost_timer, BOOSTED_GAME_SPEED, ORIGINAL_GAME_SPEED, SPEED_BOOST_DURATION

    if current_state == GameState.PLAYING:
        time_since_last_step += time.dt

        # Handle movement input (unchanged)
        if held_keys['left arrow'] or held_keys['a']: snake.change_direction(DIRECTIONS["LEFT_X"])
        elif held_keys['right arrow'] or held_keys['d']: snake.change_direction(DIRECTIONS["RIGHT_X"])
        # ... (other movement inputs) ...
        elif held_keys['up arrow'] or held_keys['space']: snake.change_direction(DIRECTIONS["UP_Y"])
        elif held_keys['down arrow'] or held_keys['control']: snake.change_direction(DIRECTIONS["DOWN_Y"])
        elif held_keys['w']: snake.change_direction(DIRECTIONS["FORWARD_Z"])
        elif held_keys['s']: snake.change_direction(DIRECTIONS["BACKWARD_Z"])

        # Power-up Spawning Logic
        if not is_powerup_item_active and not speed_boost_active:
            powerup_spawn_timer -= time.dt
            if powerup_spawn_timer <= 0:
                spawn_powerup()
                powerup_spawn_timer = random.uniform(10, 20) # Reset for next potential spawn

        # Power-up Collection Logic
        if is_powerup_item_active and powerup_item_entity and len(snake.entities) > 0:
            # Using Ursina's distance function and entity world_position
            if distance(snake.entities[0].world_position, powerup_item_entity.world_position) < snake.normal_segment_scale.x:
                powerup_collect_sound.play()
                destroy(powerup_item_entity)
                powerup_item_entity = None
                is_powerup_item_active = False
                
                speed_boost_active = True
                speed_boost_timer = SPEED_BOOST_DURATION
                game_speed = BOOSTED_GAME_SPEED
                # powerup_spawn_timer = random.uniform(10, 20) # Reset spawn timer for next powerup after this one is used

        # Speed Boost Active Timer
        if speed_boost_active:
            speed_boost_timer -= time.dt
            if speed_boost_timer <= 0:
                speed_boost_active = False
                game_speed = ORIGINAL_GAME_SPEED
                # Spawn timer for next powerup starts counting down AFTER boost ends.
                powerup_spawn_timer = random.uniform(5,10) 


        # Game Tick Logic
        if time_since_last_step >= game_speed:
            time_since_last_step = 0
            snake.move() 

            if snake.body[0] == food.position:
                eat_sound.play()
                food.entity.animate_scale(Vec3(0,0,0), duration=game_speed * 0.5) # Use current game_speed
                snake.grow()
                food.spawn(snake.body) 
                food.entity.animate_scale(food.original_scale, duration=game_speed * 0.5, delay=game_speed * 0.5)
                score += 1
                score_text.text = f'Score: {score}'
            
            collision_detected = False
            if check_collision_wall(snake.body[0]):
                collision_detected = True
            elif snake.check_collision_self():
                collision_detected = True
            
            if collision_detected:
                game_over_sound.play()
                trigger_game_over_animations()
                set_game_state(GameState.GAME_OVER)

def input(key): # (Unchanged)
    global current_state
    if current_state == GameState.START_SCREEN:
        if key == 'enter' or key == 'return': set_game_state(GameState.PLAYING)
    elif current_state == GameState.GAME_OVER:
        if key == 'r': set_game_state(GameState.PLAYING)

# --- Environment and Initial Setup (Unchanged) ---
DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 0))
AmbientLight(color=color.rgba(100, 100, 100, 0.2))
camera.orthographic = True; camera.position = (BOARD_WIDTH /2, BOARD_HEIGHT*1.5, -BOARD_DEPTH*1.5); camera.rotation_x = 30; camera.fov = 20 
Entity(model='quad', texture=WALL_TEXTURE, scale=(BOARD_WIDTH, BOARD_DEPTH), position=(0, -BOARD_HEIGHT/2, 0), rotation_x=-90)
Entity(model='quad', texture=WALL_TEXTURE, scale=(BOARD_WIDTH, BOARD_DEPTH), position=(0, BOARD_HEIGHT/2, 0), rotation_x=90)
Entity(model='quad', texture=WALL_TEXTURE, scale=(BOARD_DEPTH, BOARD_HEIGHT), position=(-BOARD_WIDTH/2, 0, 0), rotation_y=-90)
Entity(model='quad', texture=WALL_TEXTURE, scale=(BOARD_DEPTH, BOARD_HEIGHT), position=(BOARD_WIDTH/2, 0, 0), rotation_y=90)
Entity(model='quad', texture=WALL_TEXTURE, scale=(BOARD_WIDTH, BOARD_HEIGHT), position=(0, 0, BOARD_DEPTH/2), rotation_y=0)
Entity(model='quad', texture=WALL_TEXTURE, scale=(BOARD_WIDTH, BOARD_HEIGHT), position=(0, 0, -BOARD_DEPTH/2), rotation_y=180)

set_game_state(GameState.START_SCREEN) 
app.run()
