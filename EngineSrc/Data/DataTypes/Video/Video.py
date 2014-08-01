import pygame


class Video(object):

    def __init__(self, video, audio):

        self.video = video
        self.audioPath = audio

    def Render(self, screen):

        position = screen.CalculateCenterPosition(self.video.get_size())

        screen.StartRender()

        self.video.set_display(screen.screen, position)
        pygame.mixer.music.load(self.audioPath)

        self.video.play()
        pygame.mixer.music.play()

        while self.video.get_busy():

            event = pygame.event.poll()

            if event.type == pygame.MOUSEBUTTONUP or event.type == pygame.KEYUP:
                if self.video.get_busy():
                    self.video.stop()
                    pygame.mixer.music.stop()

def Read(inputFilePath):

    video = pygame.movie.Movie(inputFilePath)
    video.set_volume(0)

    return Video(video, inputFilePath)

