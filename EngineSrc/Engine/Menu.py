class Menu(object):

    def __init__(self, data, screen):

        self.menuTexture = data.GetArtFile("data/art/interface/MainMenuBack.art").Image().Texture()
        self.menuPosition = screen.CalculateCenterPosition(self.menuTexture.get_size())

        # Text positioning locations
        self.menuStartLocationCenterX = self.menuPosition[0] + 412
        self.menuStartLocationY = self.menuPosition[1] + 148
        self.menuLocationOffsetY = 48

        menuMes = data.GetMesFile("data/mes/MainMenu.mes")
        fontArt = data.GetArtFile("data/art/interface/Morph30Font.art")

        # Load start text
        startSentencesText = menuMes.lines[10: 10 + 5]

        self.startSentences = map(lambda sentences: fontArt.Sentence(sentences), startSentencesText)

    def AddRender(self, screen, sentences):

        screen.AddRender(self.menuTexture, self.menuPosition)

        locationY = self.menuStartLocationY

        for sentence in sentences:

            locationX = self.menuStartLocationCenterX - (sentence.get_size()[0] / 2)

            screen.AddRender(sentence, (locationX, locationY))

            locationY += self.menuLocationOffsetY
