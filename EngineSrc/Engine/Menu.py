import pyglet


class Menu(object):

    def __init__(self, data, window):

        menuImage = data.GetArtFile("data/art/interface/MainMenuBack.art").Image()
        menuPosition = window.CalculateCenterPosition(menuImage.info.size)
        self.menuTexture = pyglet.sprite.Sprite(menuImage.Texture(), menuPosition[0], menuPosition[1])

        # Text positioning locations
        self.menuStartLocationCenterX = menuPosition[0] + 412
        self.menuStartLocationY = menuPosition[1] + 600 - 148
        self.menuLocationOffsetY = -48

        menuMes = data.GetMesFile("data/mes/MainMenu.mes")
        self.fontArt = data.GetArtFile("data/art/interface/Morph30Font.art")

        # Load start text
        startSentencesText = menuMes.lines[10: 10 + 5]

        self.sprites = []
        self.textBatch = self.GenerateTextBatch(startSentencesText)

    def GenerateTextBatch(self, sentences):

        textBatch = pyglet.graphics.Batch()

        locationY = self.menuStartLocationY

        for sentence in sentences:

            locationX = self.menuStartLocationCenterX

            self.sprites.append(self.fontArt.GenerateSentence(textBatch, [locationX, locationY], sentence))

            locationY += self.menuLocationOffsetY

        return textBatch

    def Render(self, window):

        window.clear()

        self.menuTexture.draw()
        self.textBatch.draw()
