import tkinter as tk, random as r ,  os 

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 0
SIZE = 35
BODY_SIZE = 2
SNAKE_COLOUR = "#2905F3"
FOOD_COLOUR = "#FFFFFF"
score = 0
direction ,gameover_image= "right",[]
E1=None
E2=None
scores={"easy":[] , "moderate":[] , "difficult":[]}

class Snake():
    def __init__(self):
        self.bodysize = BODY_SIZE
        self.coordinates = []
        self.squares = []
        for i in range(BODY_SIZE):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = can.create_rectangle(x,y, x + SIZE, y + SIZE,fill=SNAKE_COLOUR)
            self.squares.append(square)
       
class Food():
    def __init__(self, snake):
        while True:
            x = r.randint(0, (GAME_WIDTH // SIZE) - 1) * SIZE
            y = r.randint(0, (GAME_HEIGHT // SIZE) - 1) * SIZE
            if [x, y] not in snake.coordinates:
                self.coordinates = [x, y]
                self.food = can.create_oval(x, y, x + SIZE, y + SIZE, fill=FOOD_COLOUR)
                break
            
def mode_selection():
    can.delete("all")
    
    can.create_text(can.winfo_width()/2 , 100 , text="select mode" ,  font="arial 30 bold" , fill="white" )
    b1=tk.Button(root , text="EASY" , command=lambda:game_mode("easy")  , height=3 , width=10 ,  bg="grey" , fg="black")
    can.create_window(can.winfo_width()/2 , 200 , window=b1)

    b2=tk.Button(root , text="MODERATE" , command=lambda:game_mode("moderate") , bg="grey" , fg="black" , height=3 , width=10 )
    can.create_window(can.winfo_width()/2 , 300 , window=b2)

    b3=tk.Button(root , text="DIFFICULT" , command=lambda:game_mode("difficult") , bg="grey" , fg="black" , height=3 , width=10 )
    can.create_window(can.winfo_width()/2 , 400 , window=b3)

def game_mode(mode):
    global SPEED
    can.delete("all")
    
    if mode=="easy":
        SPEED=200
    elif mode=="moderate":
        SPEED=100
    elif mode=="difficult":
        SPEED=50

    snake=Snake()
    food=Food(snake)
    next_turn(snake, food)
            
def next_turn(snake, food):
    global direction,score,E1,E2 
    x, y = snake.coordinates[0]
    
    if direction == "left":
        x -= SIZE
    elif direction == "right":
        x += SIZE
    elif direction == "up":
        y -= SIZE
    elif direction == "down":
        y += SIZE
        
    snake.coordinates.insert(0, [x, y])
    square = can.create_rectangle(x, y, x + SIZE, y + SIZE, fill=SNAKE_COLOUR)
    snake.squares.insert(0, square)
    
    if E1:
        can.delete(E1)
    if E2:
        can.delete(E2)
    E1=can.create_rectangle(x+20 , y+10, x+25 , y+15,fill="black", tag="eye1")
    E2=can.create_rectangle(x+20 , y+20, x+25 , y+25,fill="black", tag="eye2" )

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        l.config(text=f"score: {score}")
        can.delete(food.food)
        food = Food(snake)
    else:
        del snake.coordinates[-1]
        can.delete(snake.squares[-1])
        del snake.squares[-1]
    if check_collision(snake):
        game_over()
    else:
        root.after(SPEED, next_turn, snake, food)

def check_collision(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:
        print("GAME OVER")
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        print("GAME OVER")
        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            print("GAME OVER")
            return True
    return False

def change_dir(new_direction):
    global direction

    if new_direction == "left":
        if direction != "right":
            direction = new_direction

    if new_direction == "right":
        if direction != "left":
            direction = new_direction

    if new_direction == "up":
        if direction != "down":
            direction = new_direction

    if new_direction == "down":
        if direction != "up":
            direction = new_direction

def retry():
    global direction, score
    root.update()
    direction="right"
    can.delete("all")
    a = Snake()
    b = Food(a)
    l.config(text=f"score: {score}")
    mode_selection()
    
def game_over():
    global scores,SPEED,score,gameover_image

    if SPEED==50:
        scores["difficult"].append(score)
    elif SPEED==100:
        scores["moderate"].append(score)
    elif SPEED==200:
        scores["easy"].append(score)

    score=0
    can.delete("all")
    can.create_text(can.winfo_width()/2, can.winfo_height()/2, text="GAME OVER", font="arial 45 bold",  fill="red")
    b1=tk.Button(root,text="RETRY", command=retry, width = 10, bg="grey", fg="black" , font="arial 35 bold" )
    can.create_window(can.winfo_width()/2 , can.winfo_height()/2 + 75 ,  window=b1)
    
root = tk.Tk()
root.title("MAKE SNAKE BIGGER AGAIN")
l = tk.Label(root,text="score: 0 ", bg="grey", fg="black", font="arial 25 italic")
l.pack(anchor="w",side="top")

can = tk.Canvas(root, bg="black", width=GAME_WIDTH, height=GAME_HEIGHT)
can.pack()

root.update()
root_width = root.winfo_width()
root_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
a = int((screen_width - root_width) / 2)
b = int((screen_height - root_height) / 2)
root.geometry(f"{root_width}x{root_height}+{a}+{b}")
root.bind("<Left>" , lambda event: change_dir("left"))
root.bind("<Right>" , lambda event: change_dir("right"))
root.bind("<Up>" , lambda event: change_dir("up"))
root.bind("<Down>" , lambda event: change_dir("down"))

mode_selection()

root.mainloop()


for i in scores:
    a=os.path.dirname(__file__)
    path=os.path.join(a , f"highscore_SNEK_{i}")
    with open (path,"a+") as f:
        f.seek(0)
        A=f.readlines()
        if not A:
            f.write("THE HIGH SCORE IS 0")
        f.seek(0)
        q=f.readlines()
        b=q[len(q)-1]
        c=b.split()
        d=int(c[len(c)-1])
        for j in scores[i]:
            if j>d:
                f.write(f"\nTHE HIGH SCORE IS {j}")

