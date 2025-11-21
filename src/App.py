import pygame
import ctypes
from GameTable import GameTable
from Statistics import Statistics


width = 1200
height = 800
cardCount : int = 8

pygame.init()
clock = pygame.time.Clock()

gameTable = GameTable(width, height, cardCount)
gameTable.Show()

statistics = gameTable.ReadStatistics("./src/Statistics.txt", cardCount)
MessageBox = ctypes.windll.user32.MessageBoxW
messageBox = MessageBox(None, f"Best result for CardCount: {cardCount} is ClickCount: {statistics[0]["Clicks"]} / Precision: {statistics[0]["Precision"]}%", "Previous Best Result", 0)

# main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            gameTable.OnClick(mouse_x, mouse_y) 

            running = not gameTable.IsSolved()
            if not running:
                print(f"Game Over")
                #statistics = gameTable.GetStatistics()
                statistics = Statistics()
                lastStatistics = statistics.ReadLastStatistics()
                
                MessageBox = ctypes.windll.user32.MessageBoxW
                messageBox = MessageBox(None, f"Click count: {lastStatistics["Clicks"]}, Precision: {lastStatistics["Precision"]}%", "Game Over - You Won!", 0)

                pygame.time.delay(1000)  # Pause for a moment to show the board

    pygame.display.flip()
    clock.tick(30)