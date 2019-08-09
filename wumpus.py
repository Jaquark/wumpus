import argparse




possible_moves = ['R', # turn right 90degrees
                    'L', #turn left 90
                    'F', #move forward
                    'S' #shoot arrow
                 ]

boardwidth = 0
boardheight = 0




'''
    Ever object square that is adjacent to another square
'''
adjacencies = {}

class board_object():
    def __init__(self, x, y, name, facing=''):
        self.position = '{0},{1}'.format(x,y)
        self.obj_type = name
        self.facing = facing

def checkForEndCondition(player,thingsOnTheBoard):
    for thing in thingsOnTheBoard:
        if player.position == thing.position:
            if thing.obj_type == 'Gold':
                return 'found the Gold'
            if thing.obj_type == 'Pit':
                return 'found the Pit'
            if thing.obj_type == 'Wumpus':
                return 'were eaten'
        else:
            return ''

def add_precept(KB, playerObject, boardObjects):

    squareValue = ['','','']

    print(adjacencies[playerObject.position])
    
    for adjSquare in adjacencies[playerObject.position]:
        for obj in boardObjects:
            if obj.position == adjSquare:
                print(obj.position)
                if obj.obj_type == 'Wumpus':
                    squareValue[0] = 'Stench'
                if obj.obj_type == 'Pit':
                    squareValue[1] = 'Breeze'
            if obj.obj_type == 'Gold' and obj.position == playerObject.position :
                squareValue[2] = 'Glitter'
    KB.update( { playerObject.position : squareValue })        
    return KB

def calculateAdjacenies(x,y,n):
    adjacentSquares = []

    #check north
    if y + 1 <= n:
        adjacentSquares.append('{0},{1}'.format(x,y+1))
    #check south
    if y - 1 >= 1:
        adjacentSquares.append('{0},{1}'.format(x,y-1))
    #check east
    if x + 1 <= n:
        adjacentSquares.append('{0},{1}'.format(x+1,y))
    #check west
    if x - 1 >= 1:
        adjacentSquares.append('{0},{1}'.format(x-1,y))
    return adjacentSquares

def main():
    #import game state
    parser = argparse.ArgumentParser("wumpus")
    parser.add_argument("board", help="The file that contains the default board in an n*n state", type=str)
    args = parser.parse_args()

    gameState = []

    boardObjects = []

    with open(args.board) as gamestate:
        gameState = [line.replace('\n','').split(",") for line in gamestate]

    boardwidth = len(gameState)
    boardheight = len(gameState[0]) 

    #print(gameState)
    gameState.reverse()
    #print(gameState)

    '''
    Knowledge base will be of the form 'pos_x,pos_y' : ['Stench','Pit','Gold'] 
    
    '''
    KB = {}

    #first we need to populate the entire knowledge base with Socrates definition of true knowledge
    for x in range(0,len(gameState)) :
        for y in range(0,len(gameState[x])):
                coordinatesAsString = '{0},{1}'.format(y+1, x+1)
                if( gameState[x][y] == 'W'):
                    boardObjects.append( board_object(y+1, x+1,'Wumpus') )
                    print('wumpus at {0},{1}'.format(y+1, x+1))
                elif(gameState[x][y] == 'P'):
                    boardObjects.append( board_object(y+1, x+1,'Pit') )
                    print('pit at {0},{1}'.format(y+1, x+1))
                elif(gameState[x][y] == 'G'):
                    boardObjects.append( board_object(y+1, x+1,'Gold') )
                    print('gold at {0},{1}'.format(y+1, x+1))
                adjacencies.update ( { coordinatesAsString : calculateAdjacenies(y+1, x+1, len(gameState)) } )
    
    #Then we want to add the person to the game, at position 1,1
    #playerObject = board_object(1,1,'Player','East')

    #playerObject = board_object(1,2,'Player','East') #- KB 1,2 == 2
    #playerObject = board_object(2,1,'Player','East')#- KB 2,1 == 1
    playerObject = board_object(2,3,'Player','East')#- KB 2,3 == 7 

    endGameVerbage = ''

    #while(endGameVerbage == ''):
        
    #    endGameVerbage = checkForEndCondition(playerObject,boardObjects)
    #    KB = add_precept(KB, playerObject, boardObjects)
    
    #KB = add_precept(KB, playerObject, boardObjects)

    #print(KB)


    

main()