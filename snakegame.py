import curses
import random

# Initialize the screen
stdscr = curses.initscr()
curses.curs_set(0)  # Hides the cursor
sh, sw = stdscr.getmaxyx()  # Get the screen height and width
w = curses.newwin(sh, sw, 0, 0)  # Create a new window
w.keypad(1)  # Enable keypad mode
w.timeout(100)  # Refresh every 100ms

# Initial snake position
snake_x = sw // 4
snake_y = sh // 2
snake = [
    [snake_y, snake_x],
    [snake_y, snake_x - 1],
    [snake_y, snake_x - 2]
]

# Food
food = [sh // 2, sw // 2]
w.addch(food[0], food[1], curses.ACS_BLOCK)
# Initial direction
key = curses.KEY_RIGHT

while True:
    next_key = w.getch()  # Get the next key
    key = key if next_key == -1 else next_key  # If no key is pressed, use previous key

    # Check if the snake has hit the border or itself
    if snake[0][0] in [0, sh] or \
       snake[0][1] in [0, sw] or \
       snake[0] in snake[1:]:
        curses.endwin()  # End the game if the snake hits the wall or itself
        quit()

    # Determine the new head based on the direction
    new_head = [snake[0][0], snake[0][1]]

    if key == curses.KEY_DOWN:
        new_head[0] += 1
    if key == curses.KEY_UP:
        new_head[0] -= 1
    if key == curses.KEY_LEFT:
        new_head[1] -= 1
    if key == curses.KEY_RIGHT:
        new_head[1] += 1

    # Insert the new head at the front of the snake
    snake.insert(0, new_head)

    # Check if snake eats the food
    if snake[0] == food:
        food = None
        while food is None:
            new_food = [
                random.randint(1, sh - 1),
                random.randint(1, sw - 1)
            ]
            food = new_food if new_food not in snake else None
        w.addch(food[0], food[1], curses.ACS_BLOCK)  # Add new food
    else:
        tail = snake.pop()  # Remove the last part of the snake
        w.addch(tail[0], tail[1], ' ')

    # Display the new head of the snake
    w.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)
