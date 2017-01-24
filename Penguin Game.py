# Jennifer Cho and Leah Hobert
# CS 111 Final Project
# May 8th, 2015

import Tkinter as tk
import animation
import os

WIDTH = 500
HEIGHT = 550

class Enemy(animation.AnimatedObject):
    # Read a gif image file
    def __init__(self,canvas,filename,x,y,speed):
        self.canvas = canvas
        self.photo = tk.PhotoImage(file = filename)
        self.phototag = self.canvas.create_image(x,y, image=self.photo)
        self.photo_width=self.photo.width() # use to prevent enemy from going off screen
        self.delta = speed # speed of enemy
        
    def move(self):
        if self.delta > 0:
            x1, y1 = self.canvas.coords(self.phototag)
            if x1 >= self.canvas.winfo_width()-self.photo_width/2: # bounce back from R wall
                self.delta *= -1 # changes direction of enemy

        elif self.delta < 0:
            x1, y1 = self.canvas.coords(self.phototag)
            if x1 <= self.photo_width/2: # bounce back from L wall
                self.delta *= -1
           
        self.canvas.move(self.phototag,self.delta,0) # move back and forth horizontally
        
class App(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self)

        root.title('ICEWARD BOUND')
        self.myFrame = tk.Frame(root)
        self.myFrame.pack()
        
        # Button panel layout
        self.buttonPanel = tk.Frame(self.myFrame)
        self.buttonPanel.pack()
        
        # Animation canvas
        self.canvas = animation.AnimationCanvas(self.myFrame, width = WIDTH, height = HEIGHT, bg='#3399FF')
        self.canvas.pack()
        
        self.isUserPlayingGame = True # Use later to see if user has finished the game and wants to restart
        self.winGame = True # Default set to true. Change to false if user loses
        self.createWidgets()
        
    def createWidgets(self):
        # Create buttons (Start, Faster, Slower, Quit)
        self.startButton = tk.Button(self.buttonPanel, text="Start", command=self.onStartButtonClick)
        self.startButton.grid(row=1,column=0)
        tk.Button(self.buttonPanel, text="Faster",command=self.canvas.accelerate).grid(row=1, column=1) 
        tk.Button(self.buttonPanel, text="Slower",command=self.canvas.decelerate).grid(row=1, column=2) 
        tk.Button(self.buttonPanel, text="Quit",command=self.onQuitButtonClick).grid(row=1, column=3)
            
        # Title of game on top
        # Seperate words to prevent stretching the column cells
        self.titleLabel = tk.Label(self.buttonPanel,text='Iceward',font='Harrington 40')
        self.titleLabel.grid(row=0,column=1)
        self.titleLabel2 = tk.Label(self.buttonPanel,text=' Bound',font='Harrington 40')
        self.titleLabel2.grid(row=0,column=2)
        
        # Add enemies to canvas. Each starts at different position
        # and have different speeds.
        self.canvas.addItem(Enemy(self.canvas,'narwhal.gif',100,125,25))
        self.canvas.addItem(Enemy(self.canvas,'shark.gif',250,225,20))
        self.canvas.addItem(Enemy(self.canvas,'seal.gif',370,325,15))
        self.canvas.addItem(Enemy(self.canvas,'polarbear.gif',260,425,10))
            
        # Import gif image of user penguin
        # Position at the bottom center
        self.penguin= tk.PhotoImage(file = 'cryingpenguin.gif')
        self.photo_width = self.penguin.width()
        self.penguintag = self.canvas.create_image(WIDTH/2,HEIGHT-self.photo_width/2, image=self.penguin)
            
        # Import gif image of mother penguin
        # Position at the top center
        self.momPenguin = tk.PhotoImage(file = 'mompenguin.gif')
        self.mompenguintag = self.canvas.create_image(WIDTH/2,30, image=self.momPenguin)
        
        # Create instructions text and on top of rectangle which the user first
        # sees when they run the game    
        self.instructions = (self.canvas.create_text(WIDTH/2,HEIGHT/2,text=('\n\n Baby Penguin has lost his mother!\n\n Press start'
        + ' and control Baby\n Penguin using the arrow keys\n and help him reach his mother.\n\n Don\'t get eaten by the enemies!\n\n'),font='Impact 32'))
        self.instructionsRectangle = self.canvas.create_rectangle(self.canvas.bbox(self.instructions),fill='#C2A3FF',outline='')
        self.canvas.tag_lower(self.instructionsRectangle,self.instructions) # Puts text in front of rectangle
        
        self.gameOver() # Recognizes if user has won or lost

    # Arrow keys
    def bindArrowKeys(self):
        self.myFrame.bind('<Left>', self.leftKey)  # When left arrow key is pressed, invoke self.leftKey method
        self.myFrame.bind('<Right>', self.rightKey)  # When right arrow key is pressed, invoke self.rightKey method
        self.myFrame.bind('<Up>', self.upKey)  # When up arrow key is pressed, invoke self.upKey method
        self.myFrame.bind('<Down>', self.downKey)  # When down arrow key is pressed, invoke self.downKey method
        self.myFrame.focus_set() # Must be called so arrow keys are binded
        
    # Disconnects each arrow key
    def unbindArrowKeys(self):
        self.myFrame.unbind('<Left>')
        self.myFrame.unbind('<Right>')
        self.myFrame.unbind('<Up>')
        self.myFrame.unbind('<Down>')
        
    # Set direction of movement for each key
    def leftKey(self, event):
        x0,y0 =  self.canvas.coords(self.penguintag)
        if x0 >= self.photo_width: # Prevent penguin from moving off screen
            self.canvas.move(self.penguintag,-25,0) # Moves 25 pixels left
            
    def rightKey(self, event):
        x0,y0 =  self.canvas.coords(self.penguintag)
        if x0 <= self.canvas.winfo_width()-self.photo_width: 
            self.canvas.move(self.penguintag,25,0)  # Moves 25 pixels right 
                
    def upKey(self, event):
        x0,y0 =  self.canvas.coords(self.penguintag)
        if y0 >= self.photo_width:
            self.canvas.move(self.penguintag,0,-25) # Moves 25 pixels up
        
    def downKey(self, event):
        x0,y0 =  self.canvas.coords(self.penguintag)
        if y0 <= self.canvas.winfo_height()-self.photo_width:
            self.canvas.move(self.penguintag,0,25) # Moves 25 pixels down

    # Detects if the user has won or lost        
    def gameOver(self):
        x1, y1,x2,y2 = self.canvas.bbox(self.penguintag) 
        
        # If penguin runs into enemy
        # find_overlapping returns tuple of ids of objects that overlap with user penguin
        # 1,2,3,4 are the ids of each enemy. If enemy id is in find_overlapping tuple,
        # user has lost
        if self.isUserPlayingGame == True:
            for num in range(1,5):
                if num in self.canvas.find_overlapping(x1,y1,x2,y2):
                    self.unbindArrowKeys()
                    self.loserMessage = self.canvas.create_text(WIDTH/2,HEIGHT/2,text='You\'ve been eaten :(',font='Impact 50')
                    self.canvas.config(bg='red')
                    self.isUserPlayingGame = False # Switch to False because user finished game
                    self.winGame = False # Switch to False since user lost
    
                    self.startButton.config(text='Play again') # Change text to reset button
                    self.canvas.stop() # Stop animation

            # If penguin reaches mother   
            # mother penguin's id is 6. If 6 is in tuple, user has won     
            if self.canvas.find_overlapping(x1,y1,x2,y2) == (5,6):
                self.unbindArrowKeys()
                self.winnerMessage = self.canvas.create_text(WIDTH/2,HEIGHT/2,text='You found your mom!',font='Impact 50')
                self.isUserPlayingGame = False
                self.startButton.config(text='Play again')
                self.canvas.stop()
            
        # So game keeps checking for overlapping ids    
        self.after(animation.DEFAULT_SPEED, self.gameOver)
    
    def movePenguinBackToStart(self):
        # Move user penguin back to original position
        xy = self.canvas.coords(self.penguintag)
        xCoor = xy[0]
        yCoor = xy[1]
        self.canvas.move(self.penguintag,WIDTH/2-xCoor,(HEIGHT-self.photo_width/2)-yCoor)
    
    # Command when Start button is pressed                
    def onStartButtonClick(self):
        self.canvas.start() # Start animation canvas
        self.bindArrowKeys() # Let user start using arrow keys
        
        # Remove instruction text and rectangle
        self.canvas.delete(self.instructions)
        self.canvas.delete(self.instructionsRectangle)

        # Reset command, if user has finished game
        if self.isUserPlayingGame == False:
            self.startButton.config(text='Start')
            self.bindArrowKeys()
            self.canvas.config(bg='#3399FF')
            
            # If user won game, delete winning message that pops up
            # if user lost game, delete losing message
            if self.winGame == True:
                self.canvas.delete(self.winnerMessage)
            else:
                self.winGame = True
                self.canvas.delete(self.loserMessage)
                
            # Move penguin back to start
            self.movePenguinBackToStart()
                       
            # Starts animation again   
            self.canvas.start()
            
            # Switch to True since user is playing again
            self.isUserPlayingGame = True
            
            # If the user chooses to make the enemies move faster or slower:
            # we added a line of code under the 'stop' method of
            # animation.py that resets the the canvas back to default speed
            # when the user starts a new game
            
    # Command when Quit button is pressed
    def onQuitButtonClick(self):
        self.master.destroy() # Exits entire window

root = tk.Tk()
app = App(root)
root.mainloop()    
# For Macs only: Bring root window to the front
os.system('''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')