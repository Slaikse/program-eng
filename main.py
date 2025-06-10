import pygame
import sys
from application import Application
from helpers.audio import Audio

def main():
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Initialize the audio
    Audio.init()
    
    # Create and run the application
    app = Application()
    app.run()

if __name__ == "__main__":
    main() 