import random
import copy

class Game():
    colors = ["red", "blue", "green", "pink", "orange", "cyan", "brown", "purple", "cyan", "aquamarine", "deeppink"]
    def __init__(self, mapSize, playerCnt, vsBot=-1):
        if mapSize == 5 and vsBot:
            self.vsBot = True
        self.mapSize = mapSize
        self.map = [[[0, -1] for i in range(mapSize)] for i in range(mapSize)]
        self.playerCnt = playerCnt
        self.moveOrder = self.colors[:playerCnt]
        random.shuffle(self.moveOrder)
        self.curMove = 0
    
    def end(self):
        playerCellsCnt = [0] * self.playerCnt
        nonZero = 0
        for i in range(self.playerCnt):
            playerCellsCnt[i] = sum(map(lambda x: sum(map(lambda y: 1 if y[1] == i else 0, x)), self.map))
            if playerCellsCnt[i] != 0:
                nonZero += 1
        
        return nonZero == 1
        
    
    def simulateOneStep(self, currentMap):
        fours = []
        newMap = copy.deepcopy(currentMap)
        for i in range(len(currentMap)):
            for j in range(len(currentMap)):
                if currentMap[i][j][0] >= 4:
                    fours.append([i, j])
        
        for x, y in fours:
            cnt = 0
            if x > 0:
                cnt += 1
                newMap[x-1][y][0] += 1
                newMap[x-1][y][1] = newMap[x][y][1]
            if x < len(currentMap) - 1:
                cnt += 1
                newMap[x+1][y][0] += 1
                newMap[x+1][y][1] = newMap[x][y][1]
            if y > 0:
                cnt += 1
                newMap[x][y-1][0] += 1
                newMap[x][y-1][1] = newMap[x][y][1]
            if y < len(currentMap)-1:
                cnt += 1
                newMap[x][y+1][0] += 1
                newMap[x][y+1][1] = newMap[x][y][1]
            newMap[x][y][0] -= cnt
            if newMap[x][y][0] == 0:
                newMap[x][y][1] = -1
        #self.printMap()
        return newMap

    
    def simulateFully(self, Map):
        
        currentMap = copy.deepcopy(Map)
        while (currentMap != self.simulateOneStep(currentMap)):
            currentMap = self.simulateOneStep(currentMap)
        
        return currentMap

    
    def start(self, x, y):
        if not (0 <= x < self.mapSize and 0 <= y < self.mapSize):
            print("Incorrect move")
            return False
        
        if self.map[x][y] != [0, -1]:
            print("This is not yours cell")
            return False

        self.map[x][y] = [3, self.curMove % self.playerCnt]

        self.curMove += 1
        return self.end()


    def next(self, x, y):
        if not (0 <= x < self.mapSize and 0 <= y < self.mapSize):
            print("Incorrect move")
            return False

        if self.map[x][y][1] != self.curMove % self.playerCnt:
            print("This is not yours cell")
            return False
        
        self.map[x][y][0] += 1
        self.map = self.simulateFully(self.map)
        print("next move")
        self.curMove += 1
        return self.end()
    

    def BotStartMove(self):
        opi = 0
        opj = 0
        for i in range(self.mapSize):
            for j in range(self.mapSize):
                if self.map[i][j][1] == 1-self.vsBot:
                    opi = i
                    opj = j
        print(opi, opj)
        possibleMoves = []
        for i, j in [[opi-1, opj-1], [opi-1, opj+1], [opi+1, opj-1], [opi+1, opj+1]]:
            if (0 <= i < self.mapSize and 0 <= j < self.mapSize):
                rate = abs(i-self.mapSize//2)+abs(j-self.mapSize//2)
                possibleMoves.append([i, j, rate])
        print(possibleMoves)
        possibleMoves.sort(key=lambda x: x[2], reverse=True)
        print(possibleMoves[-1][:-1])
        return possibleMoves[-1][:-1]


    def complainer(self, Map, c, depth):
        #print(depth)
        botCells = sum(map(lambda x: sum(map(lambda y: 1 if y[1] == self.vsBot else 0, x)), Map))
        opponentCells = sum(map(lambda x: sum(map(lambda y: 1 if y[1] != self.vsBot else 0, x)), Map))
        botSummary = sum(map(lambda x: sum(map(lambda y: y[0] if y[1] == self.vsBot else 0, x)), Map))
        opponentSummary = sum(map(lambda x: sum(map(lambda y: 1 if y[1] != self.vsBot else 0, x)), Map))

        if (botCells == 0):
            rate = -1000
        elif opponentCells == 0:
            rate = 1000
        else:

            rate = (botCells-2*opponentCells) + botSummary/botCells

        if depth == 0:
            return [-1, -1, rate]
        


        possibleMoves = []

        for i in range(len(Map)):
            for j in range(len(Map)):
                if Map[i][j][1] == c:
                    possibleMoves.append([i, j])
        #print(possibleMoves)
        movesResults = []

        for i, j in possibleMoves:
            newMap = copy.deepcopy(Map)
            newMap[i][j][0] += 1
            newMap = self.simulateFully(newMap)
            res = self.complainer(newMap, 1-c, depth-1)
            #if depth == 1:
            movesResults.append([i, j, res[2]])
            

        movesResults.sort(key=lambda x: x[2])
        #print(movesResults)
        if not movesResults: return [-1, -1, -1000]
        if c == self.vsBot:
            return movesResults[-1]
        return movesResults[0]

    
    def botMove(self):
        res = self.complainer(copy.deepcopy(self.map), self.vsBot, 5)
        print(res)
        self.next(res[0], res[1])
        return self.end()
    

    def printMap(self):
        
        for i in range(self.mapSize):
            for j in range(self.mapSize):
                print(f"\033[3{self.map[i][j][1]+1}m{self.map[i][j][0]}", end=' ')
            print("\n", end='')

        return True


game = Game(5, 2, 1)
game.start(*list(map(int, input().split())))
game.start(*game.BotStartMove())
game.printMap()

while not game.end():
    print(game.curMove, game.curMove % game.playerCnt)
    if game.curMove % game.playerCnt == 1:
        game.botMove()
    else:
        x, y = list(map(int, input().split()))
        game.next(x, y)
    game.printMap()


