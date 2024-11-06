import tkinter as tk
import random
from PIL import Image, ImageTk

# Set up the main game window
root = tk.Tk()
root.title("Find the Suitcase")
root.geometry("600x800")

# Global variables
lives = 3
time_left = 100
target_suitcase = None
chosen_images = []

# Load suitcase images
images = [Image.open(f"IMG_{i}.PNG") for i in range(1, 26)]
image_labels = []

# Resize images for display (you may adjust size based on image dimensions)
resized_images = [img.resize((120, 120)) for img in images]  # Increased size for better visibility
tk_images = [ImageTk.PhotoImage(img) for img in resized_images]

# Functions
def start_game():
    global target_suitcase, chosen_images, lives, time_left
    lives = 3
    time_left = 100
    lives_label.config(text="❤️❤️❤️")
    play_again_button.place_forget()  # Hide the play again button at the start
    message_label.place_forget()      # Hide any messages at the start
    
    # Randomly select a target suitcase and display it
    target_suitcase = random.choice(images)
    target_index = images.index(target_suitcase)
    target_image_display = ImageTk.PhotoImage(target_suitcase.resize((150, 150)))
    target_label.config(image=target_image_display)
    target_label.image = target_image_display
    
    # Select 8 other random images and shuffle
    chosen_images = random.sample([i for i in range(25) if i != target_index], 8) + [target_index]
    random.shuffle(chosen_images)
    
    # Display suitcase options
    for i in range(9):
        img_label = image_labels[i]
        img_label.config(image=tk_images[chosen_images[i]])
        img_label.image = tk_images[chosen_images[i]]
        img_label.bind("<Button-1>", lambda e, idx=chosen_images[i]: check_choice(idx))

    # Start the timer
    countdown()

def check_choice(index):
    global lives
    if images[index] == target_suitcase:
        # Display congratulatory message and show play again button in the center of the screen
        message_label.config(text="Congratulations!")
        message_label.place(relx=0.5, rely=0.4, anchor="center")
        play_again_button.place(relx=0.5, rely=0.5, anchor="center")  # Center the button
    else:
        lives -= 1
        lives_label.config(text="❤️" * lives)
        if lives == 0:
            # Display game over message and show play again button
            message_label.config(text="Out of lives! Try again.")
            message_label.place(relx=0.5, rely=0.4, anchor="center")
            play_again_button.place(relx=0.5, rely=0.5, anchor="center")  # Center the button

def countdown():
    global time_left
    if time_left > 0:
        time_left -= 1
        timer_label.config(text=f"Time Left: {time_left} sec")
        root.after(1000, countdown)  # 1000 ms delay for accurate 1-second decrement
    else:
        # If time runs out, show the game over message and play again button
        message_label.config(text="Time's up! Try again.")
        message_label.place(relx=0.5, rely=0.4, anchor="center")
        play_again_button.place(relx=0.5, rely=0.5, anchor="center")  # Center the button

# GUI Layout
# Target suitcase display
tk.Label(root, text="Please help the passenger find his suitcase.").pack(pady=10)
target_label = tk.Label(root)
target_label.pack(pady=10)

# Timer and lives
timer_label = tk.Label(root, text=f"Time Left: {time_left} sec", font=("Arial", 14))
timer_label.pack(pady=5)

lives_label = tk.Label(root, text="❤️❤️❤️", font=("Arial", 14))
lives_label.pack(pady=5)

# Suitcase options grid
options_frame = tk.Frame(root)
options_frame.pack()

for i in range(3):
    for j in range(3):
        img_label = tk.Label(options_frame, image=tk_images[0], borderwidth=2, relief="solid", width=120, height=120)
        img_label.grid(row=i, column=j, padx=10, pady=10)
        image_labels.append(img_label)

# Message label (for "Congratulations!" or "Out of lives!")
message_label = tk.Label(root, text="", font=("Arial", 16))

# Play again button (centered overlay button)
play_again_button = tk.Button(root, text="Play Again", command=start_game, font=("Arial", 16), width=15, height=2)
# Initially hidden, shown only when player finds correct suitcase or loses

# Start game
start_game()
root.mainloop()
