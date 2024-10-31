import pygame 
import string
import random
from wordlist import words

pygame.init()

# Window dimensions and setup
winHeight = 600
winWidth = 700
window = pygame.display.set_mode((winWidth, winHeight))
pygame.display.set_caption("Hangman Game! BY Alaa Yasser")

# Colors and background
bg_color = (255, 127, 80)  # ORANGE
button_color = (0, 0, 0)   # BLACK
hover_color = (100, 100, 100)  # DARK GRAY for hover
click_color = (200, 0, 0)   # RED for clicked button
text_color = (255, 255, 255)  # WHITE

# Game variables
answer = random.choice(words).upper()
guessed = set()
wrong_guesses = 0
alphabet_buttons = []

# Initialize fonts
font = pygame.font.Font(None, 30)
large_font = pygame.font.Font(None, 50)

# Alphabet button settings
button_width = 30
button_height = 30
padding = 10
x_start = 100
y_start = 400

# Draw buttons for each letter and store them in a list
def setup_buttons():
    for i, letter in enumerate(string.ascii_uppercase):
        x = x_start + (i % 13) * (button_width + padding)
        y = y_start + (i // 13) * (button_height + padding)
        rect = pygame.Rect(x, y, button_width, button_height)
        alphabet_buttons.append((rect, letter, False))  # False for not clicked

# Display the hangman image based on wrong guesses
def display_image(wrong_guesses):
    hangman_art = {
        0: "E:\\CodeAlpha_Task1_Hangman\\images\\hangman0.PNG",
        1: "E:\\CodeAlpha_Task1_Hangman\\images\\hangman1.PNG",
        2: "E:\\CodeAlpha_Task1_Hangman\\images\\hangman2.PNG",
        3: "E:\\CodeAlpha_Task1_Hangman\\images\\hangman3.PNG",
        4: "E:\\CodeAlpha_Task1_Hangman\\images\\hangman4.PNG",
        5: "E:\\CodeAlpha_Task1_Hangman\\images\\hangman5.PNG",
        6: "E:\\CodeAlpha_Task1_Hangman\\images\\hangman6.PNG"
    }
    image = pygame.image.load(hangman_art[wrong_guesses]).convert()
    image = pygame.transform.scale(image, (200, 200))
    window.blit(image, (240, 100))

# Display the current word state (guessed letters or underscores)
def display_word():
    display_text = ""
    for letter in answer:
        display_text += letter + " " if letter in guessed else "_ "
    text_surface = large_font.render(display_text.strip(), True, text_color)
    window.blit(text_surface, (winWidth // 2 - text_surface.get_width() // 2, 300))

# Draw alphabet buttons on the screen
def draw_buttons():
    for rect, letter, clicked in alphabet_buttons:
        color = click_color if clicked else hover_color if rect.collidepoint(pygame.mouse.get_pos()) else button_color
        pygame.draw.rect(window, color, rect)
        text = font.render(letter, True, text_color)
        text_rect = text.get_rect(center=(rect.x + button_width // 2, rect.y + button_height // 2))
        window.blit(text, text_rect)

# Handle guessed letter and update game state
def check_the_guess(letter):
    global wrong_guesses
    if letter in answer:
        guessed.add(letter)
    else:
        wrong_guesses += 1
        
# Reset the game variables to start a new game
# Reset the game variables to start a new game
def reset_game():
    global guessed, wrong_guesses, answer, alphabet_buttons
    guessed = set()                # Clear guessed letters
    wrong_guesses = 0               # Reset wrong guess count
    answer = random.choice(words).upper()  # Get a new random word
    alphabet_buttons.clear()        # Clear and recreate alphabet buttons
    setup_buttons()                 # Set up buttons for the new game state


def check_win_lose():
    global wrong_guesses, guessed, answer, alphabet_buttons

    if wrong_guesses >= 6:
        display_end_message(f"You Lose! The word was: {answer}")
        reset_game()  # Reset the game after showing the message
    elif all(letter in guessed for letter in answer):
        display_end_message("You Win!")
        reset_game()
        
def display_end_message(message):
    font_large = pygame.font.Font(None, 60)
    window.fill(bg_color)  # Clear the screen before displaying the end message
    
    # Display the end message
    text_surface = font_large.render(message, True, text_color)
    window.blit(text_surface, (winWidth // 2 - text_surface.get_width() // 2, 200))

    # Display the number of wrong guesses
    guesses_text = f"Wrong guesses: {wrong_guesses}"
    guesses_surface = font_large.render(guesses_text, True, text_color)
    window.blit(guesses_surface, (winWidth // 2 - guesses_surface.get_width() // 2, 260))
    
    pygame.display.flip()  # Update the display so the message appears
    pygame.time.delay(3000)  # Pause for 3 seconds to show the message


def main_game_loop():
    global running
    running = True
    setup_buttons()
    while running:
        window.fill(bg_color)
        display_image(wrong_guesses)
        draw_buttons()
        display_word()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for i, (rect, letter, clicked) in enumerate(alphabet_buttons):
                    if rect.collidepoint(mouse_pos) and not clicked:
                        alphabet_buttons[i] = (rect, letter, True)  # Mark as clicked
                        check_the_guess(letter)
                        print(f"Button {letter} clicked")  # Handle letter click here
                        check_win_lose()  # Check for win/loss after each guess

# Run the game
main_game_loop()
pygame.quit()