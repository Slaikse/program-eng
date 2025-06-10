import pygame
import os

class Audio:
    _sounds = {}
    _music = None
    _initialized = False
    
    @classmethod
    def init(cls):
        if not cls._initialized:
            pygame.mixer.init()
            cls._initialized = True
            
            # Load sound effects
            sound_files = {
                'match': 'match.wav',
                'select': 'select.wav',
                'swap': 'swap.wav',
                'level_complete': 'level_complete.wav'
            }
            
            for name, file in sound_files.items():
                try:
                    sound_path = os.path.join('assets', 'audio', file)
                    if os.path.exists(sound_path):
                        cls._sounds[name] = pygame.mixer.Sound(sound_path)
                except:
                    print(f"Could not load sound: {file}")
    
    @classmethod
    def play_sound(cls, name):
        if name in cls._sounds:
            cls._sounds[name].play()
    
    @classmethod
    def play_music(cls, name):
        try:
            music_path = os.path.join('assets', 'audio', f"{name}.mp3")
            if os.path.exists(music_path):
                pygame.mixer.music.load(music_path)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        except:
            print(f"Could not play music: {name}")
    
    @classmethod
    def stop_music(cls):
        pygame.mixer.music.stop() 