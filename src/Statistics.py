class Statistics:
    # Constructor
    def __init__(self, filePath : str = "./src/Statistics.txt"):
        self._filePath : str = filePath

    def SaveStatistics(self, cardCount : int, clicks : int):
        with open(self._filePath, 'a') as file: # append, so keep existing data
            file.seek(0, 2)  # Move the cursor to the end of the file
            file.write(f"\nCardCount={cardCount} Clicks={clicks} Precision={round((100 * cardCount)/clicks, 2)}")

    def ReadLastStatistics(self) -> dict:
        with open(self._filePath, 'r') as file:
            lines = file.readlines()
            lastLine = lines[-1]

            parts = lastLine.strip().split()
            statDict = {}
            for part in parts:
                key, value = part.split('=')
                statDict[key] = float(value) if '.' in value else int(value)

        return statDict
    
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

                statsList.sort(key=lambda x: x["Clicks"])

        return statsList