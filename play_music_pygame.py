import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pandas as pd
import random

def main(emotion_num):
    pygame.mixer.init()
    emotion_dict = {'1':'Angry', '2':'Happy', '3':'NeutralOrSad'}
    filename=emotion_dict[emotion_num]+".csv"
    df = pd.read_csv('emotions_file/'+filename)

    df_top = (df.columns)[0]
    count = df[df_top].count()
    
    # Try to load a valid song, skip corrupted files
    max_attempts = 10
    for attempt in range(max_attempts):
        random_index=random.randrange(0, count, 1)
        song_name = df[df_top][random_index]
        path='songs/'+song_name+'.mp3'
        
        try:
            pygame.mixer.music.load(path)
            break
        except pygame.error as e:
            print(f"Skipping corrupted file: {song_name}")
            if attempt == max_attempts - 1:
                print("Could not find a valid song file.")
                return
            continue
    
    print("Playing: ",song_name)
    print("Actions: ")
    print("\tP: pause")
    print("\tR: resume")
    print("\tS: Stop")
    print("\tE: exit")
    print("\tQ: quit")
    
    pygame.mixer.music.play()
    
    # Create a small window for event handling
    screen = pygame.display.set_mode((300, 100))
    pygame.display.set_caption("Music Player Controls")
    clock = pygame.time.Clock()
    
    running = True
    paused = False
    
    while running and pygame.mixer.music.get_busy():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    if not paused:
                        pygame.mixer.music.pause()
                        paused = True
                        print("Paused - Press 'r' to resume")
                elif event.key == pygame.K_r:
                    if paused:
                        pygame.mixer.music.unpause()
                        paused = False
                        print("Resumed")
                elif event.key == pygame.K_s:
                    pygame.mixer.music.stop()
                    print("Stopped")
                elif event.key == pygame.K_e or event.key == pygame.K_q:
                    print("Exiting...")
                    running = False
        
        # Fill screen with a simple background
        screen.fill((50, 50, 50))
        pygame.display.flip()
        clock.tick(30)
    
    pygame.mixer.music.stop()
    pygame.quit()
