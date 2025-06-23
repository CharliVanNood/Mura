import pygame

class SoundEngine:
    def __init__(self):
        self.music_queue = []
        self.sound_queue = []

        self.sounds = {}
        self.sounds_loaded = []

        self.master_volume = 0.5

        self.loadSound("effects/jump1.wav")
        self.loadSound("effects/jump2.wav")
        self.loadSound("effects/fallHard1.wav")

        self.loadSound("music/intro.wav")
        self.loadSound("music/play_loop.wav")
        self.loadSound("music/eclipse.mp3")
        self.loadSound("music/8up9down.mp3")
    
    def loadSound(self, file):
        self.sounds[file] = len(self.sounds_loaded)
        self.sounds_loaded.append(pygame.mixer.Sound(f"src/sounds/{file}"))
    
    def getSoundIdFromName(self, sound_name):
        return self.sounds[sound_name]
    
    def getSoundFromId(self, sound_id):
        return self.sounds_loaded[sound_id]
    
    def get_volume(self):
        return self.master_volume

    def playSound(self, audio_sample, volume, loops=0):
        if not audio_sample in self.sounds:
            print("Audio file not found!")
            return

        # First get the id of the audio sample, then get the audio reference with that id
        sound = self.getSoundFromId(self.getSoundIdFromName(audio_sample))
        actual_volume = max(0.0, min(1.0, volume * self.master_volume))
        sound.set_volume(actual_volume)
        sound.play(loops = loops)

    def adjust_volume(self, volume_change):
        self.master_volume = max(0.0, min(1.0, self.master_volume + volume_change))

        # change volume of playing music
        pygame.mixer.music.set_volume(self.master_volume)

    def set_volume(self, volume):
        self.master_volume = volume

        # change volume of playing music
        pygame.mixer.music.set_volume(self.master_volume)
    
    def play_music(self, filepath, loops=-1):
        full_path = f"src/sounds/{filepath}"

        pygame.mixer.music.load(full_path)
        pygame.mixer.music.set_volume(self.master_volume)
        pygame.mixer.music.play(loops=loops)
        self.music_path = filepath
    
    def stop_music(self):
        pygame.mixer.music.stop()