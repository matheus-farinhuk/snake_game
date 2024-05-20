import tkinter as tk
import numpy as np
from random import randint

class SnakeGame:
    def __init__(self, master, width=30, height=20, rec_size=10): # Config size screen and block
        self.master = master
        self.width = width
        self.height = height
        self.rec_size = rec_size
        self.initial_config()
        
        self.canvas = tk.Canvas(master, width=self.width*self.rec_size, height=self.height*self.rec_size, bg='black')
        self.canvas.pack()
        
        # Configure key
        self.master.bind("<KeyPress>", self.change_direction)
        
        # Start the game
        self.update_game()

    def initial_config(self):
        self.snake = [(10, 10), (10, 11), (10, 12)] # The first three positions
        self.direction = (0, -1)  # The start direction
        self.food = None
        self.spawn_food() 
        self.game_over = False
        self.speed = 100  # Speed in milliseconds

    def reset_game(self):
        self.canvas.delete("all")
        self.initial_config()
        self.update_game()

    def update_game(self):
        if not self.game_over:
            self.move_snake()
            self.check_collisions()
            if not self.game_over:
                self.draw_elements()
                self.master.after(self.speed, self.update_game)
            else:
                self.canvas.create_text(self.width * self.rec_size // 2, self.height * self.rec_size // 2,
                                        text="Game Over!", fill="red", font=('Arial', 24, 'bold'))
                self.master.after(500, self.update_game)
        else:
            # self.reset_game() # Auto-reset after die
            self.master.destroy() # Auto-closed after die
  
    # Spawn the food in the map
    def spawn_food(self):
        while True:
            x, y = randint(1, self.width-1), randint(1, self.height-1)
            if (y, x) not in self.snake:
                self.food = (y, x)
                break

    def change_direction(self, event):
        key = event.keysym
        new_direction = {'Up': (-1, 0), 'Down': (1, 0), 'Left': (0, -1), 'Right': (0, 1)}.get(key)
        print(self.snake)
        # Check if the new direction is not the direct opposite of the current direction
        if key in ('Up', 'Down') and (new_direction[0] + (self.snake[0][0] -self.snake[1][0])) != 0:
            self.direction = new_direction
        elif key in ('Left', 'Right') and (new_direction[1] + (self.snake[0][1] -self.snake[1][1])) != 0:
            self.direction = new_direction

    def move_snake(self):
        head_y, head_x = self.snake[0]
        new_head = (head_y + self.direction[0], head_x + self.direction[1])
        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.spawn_food()
            self.speed = max(50, self.speed - 2)  # Increase speed
        else:
            self.snake.pop()

    def check_collisions(self):
        head_y, head_x = self.snake[0]
        if (head_x < 0 or head_x >= self.width or head_y < 0 or head_y >= self.height or
            self.snake[0] in self.snake[1:]):
            self.game_over = True

    def draw_elements(self):
        self.canvas.delete("all")
        for part in self.snake:
            self.draw_rectangle(part, "green")
        self.draw_rectangle(self.food, "red")

    def draw_rectangle(self, position, color):
        y, x = position
        self.canvas.create_rectangle(x * self.rec_size, y * self.rec_size, (x + 1) * self.rec_size, (y + 1) * self.rec_size, fill=color)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
