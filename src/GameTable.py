import pygame
import math
import random
import Card
import Statistics

class GameTable:
    CARD_BACK_COLOR = (0, 0, 0)
    TABLE_BACKGROUND_COLOR = (255, 255, 255)
    BORDER_SIZE = 20

    # Constructor
    def __init__(self, width : int, height : int, cardCount : int):
        self._width : int = width
        self._height : int = height
        self._cardCount : int = self.GetNormalizedCardCount(cardCount)
        self._borderSize : int = GameTable.BORDER_SIZE
        self._backgroundColor = GameTable.TABLE_BACKGROUND_COLOR
        self._cardColors = self.DefineCardColors(self._cardCount)
        rowsColumns = self.CalculateRowsColumns(self._cardCount)
        self._rows : int = rowsColumns[0]
        self._columns : int = rowsColumns[1]
        self._clicks : int = 0
        self._idxsUncovered = []
        self._idxsSolved = []
        self._solved : bool = False

        self._cards = []
        self.CreateCards(self._rows, self._columns)

    # Get correct card count (even number between 2 and 40)
    # If the given number does not meet the conditions, it will be adjusted
    # In the subsequent logic, this value should be used instead of the uncheced input
    def GetNormalizedCardCount(self, cardCount : int):
        if(cardCount % 2 != 0):
            cardCount -= 1 # make it the smaller even
        
        if(cardCount < 2):
            cardCount = 2 # minimum
        elif(cardCount > 40):
            cardCount = 40 # maximum

        return cardCount

    # Create card objects and position them on the table
    # by calculating their upper left coordinates and their width and height
    # Colors are randomly generated and assigned to the cards
    def CreateCards(self, rows, columns):
        cardWidth = (self._width - (columns + 1) * self._borderSize) // columns
        cardHeight = (self._height - (rows + 1) * self._borderSize) // rows
        randomColors = self.GetRandomColors(self._cardColors)

        cardIdx = 0
        for row in range(self._rows):
            for column in range(self._columns):
                x = self._borderSize + column * (cardWidth + self._borderSize)
                y = self._borderSize + row * (cardHeight + self._borderSize)
                card = Card.Card(x, y, cardWidth, cardHeight, randomColors[cardIdx], GameTable.CARD_BACK_COLOR)
                self._cards.append(card)
                cardIdx += 1

    # Displays the game table and all cards (telling each card to Show itself)
    def Show(self):
        self._screen = pygame.display.set_mode((self._width, self._height)) # why method name set_mode
        self._screen.fill(self._backgroundColor)

        statistics = self.ReadStatistics("./src/Statistics.txt", self._cardCount) 

        for card in self._cards:
            card.Show(self._screen)

        pygame.display.flip() # what is the role of this method?

    # Calculates the optimal distribution of rows and columns for the given card count
    # expecting that the screen height is smaller than the width, so less rows than columns
    def CalculateRowsColumns(self, cardCount):
        rows = int(math.sqrt(cardCount)) # start with the integer square root
        while cardCount % rows != 0:
            rows -= 1 # decrement till rows * columns == cardCount
        columns = cardCount // rows

        return rows, columns
    
    # For simplicity, we define a fixed set of 20 colors
    def DefineCardColors(self, cardCount : int) -> list:
        # ToDo: optional, calculate them dynamically based on _cardCunt/2, within the RGB range 55-200
        cardColors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), 
                  (255, 255, 0), (255, 0, 255), (0, 255, 255),
                  (128, 0, 0), (0, 128, 0), (0, 0, 128), 
                  (128, 128, 0), (128, 0, 128), (0, 128, 128), 
                  (192, 192, 192), (128, 128, 128),
                  (255, 165, 0), (255, 20, 147), (75, 0, 130), (34, 139, 34),
                  (70, 130, 180), (218, 112, 214)]
        
        return cardColors[:cardCount//2] # select the first cardCount/2 colors
        # : is Slicing operatior, form start:end:step, any of them can be ommitted
        # must use as / always returns float, so need integer division, although we know the cardCount is even
    
    # Generates a shuffled list of colors based on the given colors 
    # The count is expected to be cardCount/2, so takes them twice (shuffled each time)
    def GetRandomColors(self, colors):
        colors1 = colors.copy() # to avoid modifying the original list
        random.shuffle(colors1)

        colors2 = colors.copy()
        random.shuffle(colors2)

        return colors1 + colors2
    
    # When the table is clicked, use the Mouse coordinates to determine which card was clicked (if any)
    # and delegate the Mouse event to that card
    # Counts clicks for statistics
    # Checks for matches, keeping the matching cards uncovered. Turns down the non-matching cards
    def OnClick(self, xMouse : int, yMouse : int):
        self._clicks += 1
        correctClick = False

        for idx in range(len(self._cards)):
            card = self._cards[idx]

            if card.GetRectangle().collidepoint(xMouse, yMouse):
                print(f"Card {idx} clicked")

                if idx in self._idxsUncovered:
                    print("Card already uncovered, ignoring click")
                    break

                if idx in self._idxsSolved:
                    print("Card already solved, ignoring click")
                    break

                correctClick = True
                card.OnClick(self._screen)
                self._idxsUncovered.append(idx)
                
                break
        
        if not correctClick:
            print("Click not on any card or on an already uncovered/solved card, ignoring click")
            return
        
        if len(self._idxsUncovered) == 2:
            pygame.display.flip()
            idx1 = self._idxsUncovered[0]
            idx2 = self._idxsUncovered[1]

            card1 = self._cards[idx1]
            card2 = self._cards[idx2]

            if card1.GetColor() == card2.GetColor():
                print("It's a Match")
                self._idxsSolved.append(idx1)
                self._idxsSolved.append(idx2)
            else:
                print("Not a Match")
                pygame.time.delay(300)  # Pause for a moment to show the cards

                card1.OnClick(self._screen)
                card2.OnClick(self._screen)

            self._idxsUncovered = []

            if(len(self._idxsSolved) == self._cardCount):
                print(f"Game Over, You Won! Total Clicks: {self._clicks}")
                self._solved = True
                statistics = Statistics.Statistics()
                statistics.SaveStatistics(self._cardCount, self._clicks)

    def IsSolved(self) -> bool:
        return self._solved
    
    def GetStatistics(self) -> dict:
        stats = {
                    "Clicks": self._clicks,
                    "Precision": round((100 * self._cardCount)/self._clicks, 2)
                }

        return stats

    def SaveStatistics(self, filename : str):
        statistics = self.GetStatistics()

        with open(filename, 'a') as file:
            file.seek(0, 2)  # Move the cursor to the end of the file
            file.write(f"\nCardCount={self._cardCount} Clicks={statistics["Clicks"]} Precision={statistics["Precision"]}")

    def ReadStatistics(self, filename : str, cardCount : int) -> list:
        statsList = []
        lineStartPattern = f"CardCount={cardCount}"

        with open(filename, 'r') as file:
            lines = file.readlines()
            lines.append(f"CardCount={cardCount} Clicks={10*cardCount} Precision=10.0")  # to avoid missing the last line if no newline at the end
            for line in lines:
                if(line.startswith(lineStartPattern) == False):
                    continue

                parts = line.strip().split()
                statDict = {}
                for part in parts:
                    key, value = part.split('=')
                    statDict[key] = float(value) if '.' in value else int(value)
                statsList.append(statDict)

                statsList.sort(key=lambda x: x["Precision"], reverse=True)

        return statsList