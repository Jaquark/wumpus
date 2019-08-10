import argparse




possible_moves = ['R', # turn right 90degrees
                    'L', #turn left 90
                    'F', #move forward
                    'S' #shoot arrow
                 ]


directions_f = { 'East' : '1,0',
                  'North' : '0,1',
                  'South' : '0,-1',
                  'West' : '-1,0'}

directions_rotate = { 'R' : {'East' : 'South',
                  'North' : 'East',
                  'South' : 'West',
                  'West' : 'North'},
                  'L' : {'East' : 'North',
                  'North' : 'west',
                  'South' : 'East',
                  'West' : 'South'}}

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
                return 'fell into an endless pit. Some say you are still falling to this day. Better luck next time'
            if thing.obj_type == 'Wumpus':
                return 'were eaten alive.'
    return ''
def add_precept(KB, playerObject, boardObjects):

    squareValue = ['','','','visited']
    
    for adjSquare in adjacencies[playerObject.position]:
        for obj in boardObjects:
            if obj.position == adjSquare:
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

def displayPlayerDetails(player):
    print('You are in room [{0}] of the cave, facing {1}'.format(player.position, player.facing))
    print('what would you like to do? Please enter a command {0}'.format(possible_moves))


def applyMove(player,move, n):
    #check if move is bounded
    if move == 'F':
        valueToAdd = directions_f[player.facing].split(',')
        currentPos = player.position.split(',')
        newPotential = [int(valueToAdd[0]) + int(currentPos[0]), int(valueToAdd[1]) + int(currentPos[1])]
        if ( n >= newPotential[0] >= 1 and n >= newPotential[1] >= 1):
            newPosition = '{0},{1}'.format(newPotential[0],newPotential[1])
            player.position = newPosition
        else:
            print("Bump!! You hit a wall")

    if move == 'R' or move == 'L':
        player.facing = directions_rotate[move][player.facing]
    if move == 'S':
        print('You shot the arrow, but because this is lazy at the moment, it does nothing.')
    
    return player

def provideHint(KB, player):
    #get things you experience in this room:
    for verb in KB[player.position]:
        #get adjacent squares that have not been visited
        if verb == 'Glitter':
            print('You are right on top of the gold')
        if verb == 'Stench': #yeah, I know    
            print('Be careful, it smells like a high protein diet primarily made of spelunkers, that means the Wumpus is nearby, hiding in LIST_OF_PLACES_THE_WUMPUS_MAY_BE')
        if verb == 'Breeze':
            print('It\'s breezy in here; there may be a pit in LIST_OF_PLACES_THE_PIT_MAY_BE')    



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
                elif(gameState[x][y] == 'P'):
                    boardObjects.append( board_object(y+1, x+1,'Pit') )
                elif(gameState[x][y] == 'G'):
                    boardObjects.append( board_object(y+1, x+1,'Gold') )
                adjacencies.update ( { coordinatesAsString : calculateAdjacenies(y+1, x+1, len(gameState)) } )
    
    #Then we want to add the person to the game, at position 1,1
    playerObject = board_object(1,1,'Player','East')

    #playerObject = board_object(1,2,'Player','East')
    #playerObject = board_object(2,1,'Player','East')
    #playerObject = board_object(2,3,'Player','East')

    endGameVerbage = ''

    while(endGameVerbage == ''):
        displayPlayerDetails(playerObject)
        move = raw_input()
        playerObject = applyMove(playerObject, move, boardwidth)
        endGameVerbage = checkForEndCondition(playerObject,boardObjects)
        KB = add_precept(KB, playerObject, boardObjects)
        provideHint(KB,playerObject)

        #print(KB)
    
    print('You {0}'.format(endGameVerbage))
    #KB = add_precept(KB, playerObject, boardObjects)

    #print(KB)


    

main()