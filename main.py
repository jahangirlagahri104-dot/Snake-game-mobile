import tkinter as tk
import random

# Settings
WIDTH = 400
HEIGHT = 400
SPEED = 150
SPACE_SIZE = 20
SNAKE_COLOR = "#00FF88"
FOOD_COLOR = "#FF4757"
BG_COLOR = "#0F0F23"

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Mobile Snake Game")
        self.window.configure(bg=BG_COLOR)

        self.score = 0
        self.direction = 'right'

        # Score
        self.label = tk.Label(self.window, text="Score: 0", font=('Arial', 15), fg="white", bg=BG_COLOR)
        self.label.pack()

        # Canvas (Game Screen)
        self.canvas = tk.Canvas(self.window, bg=BG_COLOR, height=HEIGHT, width=WIDTH, highlightthickness=1, highlightbackground="white")
        self.canvas.pack(pady=10)

        # --- MOBILE CONTROLS (Buttons) ---
        self.btn_frame = tk.Frame(self.window, bg=BG_COLOR)
        self.btn_frame.pack(pady=10)

        # Direction Buttons
        tk.Button(self.btn_frame, text="▲", width=5, height=2, command=lambda: self.change_direction('up')).grid(row=0, column=1)
        tk.Button(self.btn_frame, text="◀", width=5, height=2, command=lambda: self.change_direction('left')).grid(row=1, column=0)
        tk.Button(self.btn_frame, text="▶", width=5, height=2, command=lambda: self.change_direction('right')).grid(row=1, column=2)
        tk.Button(self.btn_frame, text="▼", width=5, height=2, command=lambda: self.change_direction('down')).grid(row=2, column=1)

        # Initial Snake & Food
        self.snake_coords = [[100, 100], [80, 100], [60, 100]]
        self.squares = []
        for x, y in self.snake_coords:
            square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
            self.squares.append(square)

        self.food_coords = [0, 0]
        self.create_food()
        self.next_turn()

        self.window.mainloop()

    def create_food(self):
        x = random.randint(0, (WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.food_coords = [x, y]
        self.canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

    def next_turn(self):
        x, y = self.snake_coords[0]
        if self.direction == "up": y -= SPACE_SIZE
        elif self.direction == "down": y += SPACE_SIZE
        elif self.direction == "left": x -= SPACE_SIZE
        elif self.direction == "right": x += SPACE_SIZE

        self.snake_coords.insert(0, [x, y])
        square = self.canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        self.squares.insert(0, square)

        if x == self.food_coords[0] and y == self.food_coords[1]:
            self.score += 10
            self.label.config(text=f"Score: {self.score}")
            self.canvas.delete("food")
            self.create_food()
        else:
            del self.snake_coords[-1]
            self.canvas.delete(self.squares[-1])
            del self.squares[-1]

        if self.check_collisions():
            self.game_over()
        else:
            self.window.after(SPEED, self.next_turn)

    def change_direction(self, new_dir):
        if new_dir == 'left' and self.direction != 'right': self.direction = new_dir
        elif new_dir == 'right' and self.direction != 'left': self.direction = new_dir
        elif new_dir == 'up' and self.direction != 'down': self.direction = new_dir
        elif new_dir == 'down' and self.direction != 'up': self.direction = new_dir

    def check_collisions(self):
        x, y = self.snake_coords[0]
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT: return True
        for part in self.snake_coords[1:]:
            if x == part[0] and y == part[1]: return True
        return False

    def game_over(self):
        self.canvas.delete(tk.ALL)
        self.canvas.create_text(WIDTH/2, HEIGHT/2, font=('Arial', 30), text="GAME OVER", fill="red")

if __name__ == "__main__":
    SnakeGame()
