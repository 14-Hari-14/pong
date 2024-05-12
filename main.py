import pygame
import random
import pygame.mixer
pygame.mixer.init()

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('PONG')

# setting up sounds used in the game
paddle_hit_sound = pygame.mixer.Sound("mixkit-ball-bouncing-in-the-ground-2077.wav")
score_sound = pygame.mixer.Sound("8-bit-video-game-points-version-1-145826.mp3")
win_sound = pygame.mixer.Sound("success-fanfare-trumpets-6185.mp3")

# Define colors
WHITE = (255, 255, 255)
BGCOLOR = (0, 0, 50)
BLACK = (0, 0, 0)

# default game state
game_state = "Menu"

# No of players playing the game
player_no = 0

# Setting the height and width of components

pong_rectangle_width, pong_rectangle_height = 400, 150
# Positioning the title of the game
pong_rectangle_x = (screen_width - pong_rectangle_width) // 2
pong_rectangle_y = (screen_height - pong_rectangle_height) // 8


start_rectangle_width, start_rectangle_height = 300, 100
# Positioning the start button of the game
start_rectangle_x = (screen_width - start_rectangle_width) // 2
start_rectangle_y = (screen_height - start_rectangle_height) // 2


credits_rectangle_width, credits_rectangle_height = 400, 100
# Positioning the credits button of the game
credits_rectangle_x = (screen_width - credits_rectangle_width) // 2
credits_rectangle_y = (screen_height - credits_rectangle_height) // 1.3


back_rectangle_width, back_rectangle_height = 180, 90
# Positioning the back button of the game
back_rectangle_x = (screen_width - back_rectangle_width) // 15
back_rectangle_y = (screen_height - back_rectangle_height) // 1.1


# Positioning the 1P mode button of the game
onep_rectangle_x = (screen_width - start_rectangle_width) // 2
onep_rectangle_y = (screen_height - start_rectangle_height) // 4

# Positioning the 2P mode button of the game
twop_rectangle_x = (screen_width - start_rectangle_width) // 2
twop_rectangle_y = (screen_height - start_rectangle_height) // 2

# Positioning the line that will divide the screen in 2 for 2 players
line_thickness = 4
vertical_line_x = screen_width // 2  # X-coordinate of the vertical line
start_point = (vertical_line_x, 0)  # Starting point at the top
end_point = (vertical_line_x, screen_height)  # Ending point at the bottom

# Thickness of the rectangle's border
rectangle_thickness = 10

# The Rect() function is used to define the dimensions and position of the rectangle
rectangle = pygame.Rect(pong_rectangle_x, pong_rectangle_y, pong_rectangle_width, pong_rectangle_height)

rectangle_start = pygame.Rect(start_rectangle_x, start_rectangle_y, start_rectangle_width, start_rectangle_height)
rectangle_credits = pygame.Rect(credits_rectangle_x, credits_rectangle_y, credits_rectangle_width,
                                 credits_rectangle_height)
rectangle_back = pygame.Rect(back_rectangle_x, back_rectangle_y, back_rectangle_width, back_rectangle_height)
rectangle_onep = pygame.Rect(onep_rectangle_x, onep_rectangle_y, start_rectangle_width, start_rectangle_height)
rectangle_twop = pygame.Rect(twop_rectangle_x, twop_rectangle_y, start_rectangle_width, start_rectangle_height)

# Set up font
font = pygame.font.Font("Grand9K Pixel.ttf", 100)  # None means default font, 100 is the font size
font_start = pygame.font.Font("Grand9K Pixel.ttf", 60)
font_back = pygame.font.Font("Grand9K Pixel.ttf", 30)

# Create the text
pong_text = font.render("PONG", True, WHITE)  # Render the text
start_text = font_start.render("START", True, WHITE)
credits_text = font_start.render("CREDITS", True, WHITE)
back_text = font_back.render("BACK", True, WHITE)
onep_text = font_start.render("1P", True, WHITE)
twop_text = font_start.render("2P",True, WHITE)
# Functions for initializing buttons on the screen


def back_button_init():
    pygame.draw.rect(screen, WHITE, rectangle_back, rectangle_thickness)
    text_rect_back = back_text.get_rect(center=rectangle_back.center)
    screen.blit(back_text, text_rect_back)


def start_button_init():
    pygame.draw.rect(screen, WHITE, rectangle_start, rectangle_thickness)
    text_start_rect = start_text.get_rect(center=rectangle_start.center)
    screen.blit(start_text, text_start_rect)


def credits_button_init():
    pygame.draw.rect(screen, WHITE, rectangle_credits, rectangle_thickness)
    text_credits_rect = credits_text.get_rect(center=rectangle_credits.center)
    screen.blit(credits_text, text_credits_rect)


def single_player_mode_button_init():
    pygame.draw.rect(screen, WHITE, rectangle_onep, rectangle_thickness)
    text_onep_rect = onep_text.get_rect(center=rectangle_onep.center)
    screen.blit(onep_text, text_onep_rect)

def two_player_mode_button_init():
    pygame.draw.rect(screen, WHITE, rectangle_twop, rectangle_thickness)
    text_twop_rect = twop_text.get_rect(center=rectangle_twop.center)
    screen.blit(twop_text, text_twop_rect)

def reset_game():
    global scoreL, scoreR, left_paddle, right_paddle, puck, puck_speed_x, puck_speed_y

    # Reset scores
    scoreL = 0
    scoreR = 0

    # Reset paddle positions
    left_paddle.x = 50
    left_paddle.y = (screen_height - paddle_height) // 2

    right_paddle.x = screen_width - 50 - paddle_width
    right_paddle.y = (screen_height - paddle_height) // 2

    # Reset puck position and speed
    puck.x = (screen_width // 2) - 15
    puck.y = screen_height // 2
    puck_speed_x = 5
    puck_speed_y = 4


# Paddle properties
paddle_width, paddle_height = 20, 100
paddle_speed = 5

# Paddle positions
left_paddle_x, left_paddle_y = 50, (screen_height - paddle_height) // 2
right_paddle_x, right_paddle_y = screen_width - 50 - paddle_width, (screen_height - paddle_height) // 2

# Puck properties
puck_speed_x = 5
puck_speed_y = 4

# Puck positions
puck_x = (screen_width // 2) - 15
puck_y = screen_height // 2

# Initialize clock for controlling the frame rate
clock = pygame.time.Clock()

# Initialize the direction of puck to move in
direction = random.choice([0, 1])

# Score variables
scoreL, scoreR = 0, 0

# Initialize paddles and puck
left_paddle = pygame.Rect(left_paddle_x, left_paddle_y, paddle_width, paddle_height)
right_paddle = pygame.Rect(right_paddle_x, right_paddle_y, paddle_width, paddle_height)
puck = pygame.Rect(puck_x, puck_y, 30, 30)

# Time variables
time_since_collision = 0
speed_time_increment = 1000


# Slider properties
'''
slider_width, slider_height = 200, 20
slider_x, slider_y = 200, 90
slider_rect = pygame.Rect(slider_x, slider_y, slider_width, slider_height)
slider_dragging = False  # To keep track of whether the slider is being dragged
slider_value = 0  # Initial value of the slider
min_value, max_value = 0, 255  # Minimum and maximum values for the slider


def draw_slider():  # Function to draw the slider
    pygame.draw.rect(screen, BLACK, slider_rect)
    pygame.draw.circle(screen, WHITE, (slider_rect.x + slider_value * 2, slider_y + slider_height // 2), 12)
'''


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the left mouse button is clicked within the start or credits button area
            if game_state == "Menu":
                if rectangle_start.collidepoint(event.pos):
                    print("Start Button Clicked!")  # Perform actions when the start button is clicked
                    game_state = "GameMode"
                elif rectangle_credits.collidepoint(event.pos):
                    print("credits Button Clicked!")
                    game_state = "credits"

            elif game_state == "credits":
                if rectangle_back.collidepoint(event.pos):
                    print("Back Button Clicked")
                    game_state = "Menu"

            elif game_state == "GameMode":
                if rectangle_onep.collidepoint(event.pos):
                    player_no=1
                    print("1P Button Clicked")
                    game_state = "Gameplay"
                if rectangle_twop.collidepoint(event.pos):
                    player_no=2
                    print("2P Button Clicked")
                    game_state = "Gameplay"
                elif rectangle_back.collidepoint(event.pos):
                    print("Back Button Clicked")
                    game_state = "Menu"
            elif game_state == "Victory":
                if rectangle_back.collidepoint(event.pos):
                    print("Back Button Clicked")
                    game_state = "Menu"

    # Fill the background with the background color
    screen.fill(BGCOLOR)

    if game_state == "Menu":

        # Draw an empty rectangle on the screen
        pygame.draw.rect(screen, WHITE, rectangle, rectangle_thickness)
        start_button_init()
        credits_button_init()

        # Get the rectangle for the rendered text
        text_rect = pong_text.get_rect(center=rectangle.center)

        # Blit the text onto the screen
        screen.blit(pong_text, text_rect)

    elif game_state == "GameMode":
        single_player_mode_button_init()
        two_player_mode_button_init()
        back_button_init()

    elif game_state == "credits":
        # Developer text
        developer_text1 = font_start.render("Developer: Hari", True, WHITE)
        developer_text2 = font_back.render("Yeah that's it, a solo project", True, WHITE)

        # Positioning the developer text
        developer_text1_x = (screen_width - developer_text1.get_width()) // 2
        developer_text1_y = screen_height // 3
        developer_text2_x = (screen_width - developer_text2.get_width()) // 2
        developer_text2_y = developer_text1_y + developer_text1.get_height()

        # Blitting the developer text onto the screen
        screen.blit(developer_text1, (developer_text1_x, developer_text1_y))
        screen.blit(developer_text2, (developer_text2_x, developer_text2_y))

        '''
        red_text = font_start.render("R: ", True, WHITE)
        green_text = font_start.render("G: ", True, WHITE)
        blue_text = font_start.render("B: ", True, WHITE)
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and slider_rect.collidepoint(event.pos):
                    slider_dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    slider_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if slider_dragging:
                    mouse_x, _ = event.pos
                    # Update slider value based on mouse position
                    slider_value = (mouse_x - slider_x) // 2  # Adjusting value to fit within the slider width
                    # Keep slider value within the limits
                    slider_value = max(min_value, min(max_value, slider_value))

        # Draw the slider
        draw_slider()
        '''

        back_button_init()

        # Update the display
        pygame.display.flip()

    elif game_state == "Gameplay":
        for y in range(0, screen_height, 10):
            pygame.draw.line(screen, WHITE, (vertical_line_x, y), (vertical_line_x, y + 1), line_thickness)

        font_score = pygame.font.Font("Grand9K Pixel.ttf", 60)

        score_text_offset = 50  # Distance from the top of the screen for the score labels
        score_text_center_offset = 20  # Offset for centering the score labels around the vertical line

        scoreR_text = font_score.render(str(scoreR), True, WHITE)
        rectangle_scoreR = pygame.Rect(vertical_line_x + score_text_center_offset, score_text_offset, 80,
                                       back_rectangle_height)

        pygame.draw.rect(screen, BGCOLOR, rectangle_scoreR, rectangle_thickness)
        text_rect_scoreR = scoreR_text.get_rect(center=rectangle_scoreR.center)

        scoreL_text = font_score.render(str(scoreL), True, WHITE)
        rectangle_scoreL = pygame.Rect(vertical_line_x - score_text_center_offset - 80, score_text_offset, 80,
                                       back_rectangle_height)

        pygame.draw.rect(screen, BGCOLOR, rectangle_scoreL, rectangle_thickness)
        text_rect_scoreL = scoreL_text.get_rect(center=rectangle_scoreL.center)

        screen.blit(scoreR_text, text_rect_scoreR)
        screen.blit(scoreL_text, text_rect_scoreL)

        keys = pygame.key.get_pressed()

        # Inside the game loop, after checking for events and before updating the display
        if player_no == 1:
            # Calculate the center position of the computer-controlled paddle
            comp_paddle_center_y = left_paddle.y + paddle_height // 2

            # Calculate the center position of the puck
            puck_center_y = puck.y + 15  # Assuming the puck is a 30x30 square

            # Determine the direction in which the paddle should move
            if comp_paddle_center_y < puck_center_y:
                left_paddle_y += paddle_speed  # Move paddle down
            elif comp_paddle_center_y > puck_center_y:
                left_paddle_y -= paddle_speed  # Move paddle up

            # Ensure that the paddle stays within the screen boundariess
            if left_paddle_y < 0:
                left_paddle_y = 0
            elif left_paddle_y > screen_height - paddle_height:
                left_paddle_y = screen_height - paddle_height

        # Update the position of the computer-controlled paddle
        left_paddle.y = left_paddle_y

        if player_no == 2:
            if keys[pygame.K_w] and left_paddle_y > 0:
                left_paddle_y -= paddle_speed
            if keys[pygame.K_s] and left_paddle_y < screen_height - paddle_height:
                left_paddle_y += paddle_speed
       
       
        if keys[pygame.K_UP] and right_paddle_y > 0:
            right_paddle_y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle_y < screen_height - paddle_height:
            right_paddle_y += paddle_speed

        # Update the positions of the paddles and the puck
        left_paddle.y = left_paddle_y
        right_paddle.y = right_paddle_y
        puck.x += puck_speed_x
        puck.y += puck_speed_y

        # Detect collision with top or bottom of the screen
        if puck.y <= 0 or puck.y >= screen_height - 30:  # Assuming the puck is a 30x30 square
            puck_speed_y = -puck_speed_y  # Reverse the puck's vertical direction on collision

        # Detect collision with left or right side of the screen
        if puck.x <= 0 or puck.x >= screen_width - 30:  # Assuming the puck is a 30x30 square
            puck.x = screen_width // 2 - 15  # Reset puck to the center horizontally
            puck.y = screen_height // 2  # Reset puck to the center vertically
            puck_speed_x = -puck_speed_x  # Reverse the puck's horizontal direction on collision
            puck_speed_y = 4
            score_sound.play()
            if puck_speed_x > 0:
                scoreR += 1
                # puck.x = puck.x * random.choice([-2, 2])
                # puck.y = puck.y * random.choice([-2, 2])
            else:
                scoreL += 1
                # puck.x = puck.x * random.choice([-2, 2])
                # puck.y = puck.y * random.choice([-2, 2])

            time_since_collision = 0
            puck_speed_x = random.choice([-5, 5])
            puck_speed_y = random.choice([-4, 4])
        if scoreL == 5 or scoreR == 5:
            game_state = "Victory"
            win_sound.play()

        # Check for collisions between the puck and paddles
        if puck.colliderect(left_paddle) or puck.colliderect(right_paddle):
            puck_speed_x = -puck_speed_x  # Reverse the puck's horizontal direction on collision
            paddle_hit_sound.play()

        time_since_collision += clock.get_rawtime()

        if time_since_collision >= speed_time_increment:
            puck_speed_x *= 1.1  # Increase puck's horizontal speed by 10%
            puck_speed_y *= 1.1  # Increase puck's vertical speed by 10%
            # print("Speed increased")
            time_since_collision = 0  # Reset the timer

        # Drawing the paddles and puck
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.rect(screen, WHITE, puck)

        # Update the display
        pygame.display.flip()

        # Frame rate
        clock.tick(60)

    elif game_state == "Victory":
        rectangle_win = pygame.Rect(0, 0, screen_width, screen_height)
        if scoreR == 5:
            #print("R:",scoreR)
            win1_text = font_start.render("PLAYER 1 WINS", True, WHITE)  # Render the text
            win_text = win1_text
            
        elif scoreL == 5:
            #print("L:",scoreL)
            win2_text = font_start.render("PLAYER 2 WINS", True, WHITE)  # Render the text
            win_text = win2_text

        pygame.draw.rect(screen, BGCOLOR, rectangle_win, rectangle_thickness)
        text_win_rect = win_text.get_rect(center=rectangle.center)
        screen.blit(win_text, text_win_rect)

        back_button_init()
        reset_game()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
