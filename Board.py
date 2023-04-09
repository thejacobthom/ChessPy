import os
import Pieces

# config
BOARD_WIDTH = 8
BOARD_HEIGHT = 8
EMPTY_PIECE = '___________'

class ChessBoard():
	def __init__(self):
		self._currentTurnIsWhite = True
		self._board = [[None] * BOARD_WIDTH]*BOARD_HEIGHT
		self._width = BOARD_WIDTH
		self._height = BOARD_HEIGHT
		self._lastMove = None
	
	#beginning of getter and setter methods for internal variables	
	def getLastMove(self):
		return self._lastMove
		
	def setLastMove(self, lastMoveArray):
		self._lastMove = lastMoveArray
	
	def getWidth(self):
		return self._width
	
	def getHeight(self):
		return self._height
	
	def getBoard(self):
		return self._board
		
	def getCurrentTurnIsWhite(self):
		return self._currentTurnIsWhite
	
	def flipCurrentPlayerColour(self):
		self._currentTurnIsWhite = not self._currentTurnIsWhite
	#end of getter and setter method for internal variables
	
	# returns True if requested space is none, false if not
	def isSpaceFree(self,row,col):
		return (True if self._board[row][col] == None else False)
	
	# clears the shell and then prints the board
	def printBoard(self):
		
		
		os.system('cls' if os.name == 'nt' else 'clear')
		
		someIndex = 7;
		for i in range(BOARD_HEIGHT-1, -1,-1):
			print('{} |\t'.format(someIndex), end = '')
			someIndex-=1
			
			row = []
			
			for element in self._board[i]:
				row.append(element.getPieceName() if element != None else EMPTY_PIECE)
				
			print('\t'.join(row), end='\n\n')
		
		print('____________________________________')
		print('  |  0   1   2   3   4   5   6   7 ')

	
	# sets up the board for standard 8*8 play
	def resetBoard(self):
		for i in range(0, self.getHeight()):
			if (i == 0):
				self._board[i] = [Pieces.Rook(True),Pieces.Knight(True),Pieces.Bishop(True),Pieces.Queen(True),Pieces.King(True),Pieces.Bishop(True),Pieces.Knight(True),Pieces.Rook(True)]
			elif (i == 1):
				self._board[i] = [Pieces.Pawn(True),Pieces.Pawn(True),Pieces.Pawn(True),Pieces.Pawn(True),Pieces.Pawn(True),Pieces.Pawn(True),Pieces.Pawn(True),Pieces.Pawn(True)]
			elif (i == 6):
				self._board[i] = [Pieces.Pawn(False),Pieces.Pawn(False),Pieces.Pawn(False),Pieces.Pawn(False),Pieces.Pawn(False),Pieces.Pawn(False),Pieces.Pawn(False),Pieces.Pawn(False)]
			elif (i == 7):
				self._board[i] = [Pieces.Rook(False),Pieces.Knight(False),Pieces.Bishop(False),Pieces.Queen(False),Pieces.King(False),Pieces.Bishop(False),Pieces.Knight(False),Pieces.Rook(False)]
			else:
				self._board[i] = [None]*self.getWidth()
	
			
	# a function to move a piece as long as it is a valid move.
	# takes a length 4 array ordered as [orig_row,orig_column,new_row,new_col]
	def movePiece(self, someArray):
		orig_row = someArray[0]
		orig_col = someArray[1]
		new_row = someArray[2]
		new_col = someArray[3]
		
		# get the type of piece to move
		movedPiece = self._board[orig_row][orig_col]
		
		#check that the current piece is not an empty square
		if (movedPiece != None):
		
			# get the colour of the piece to move
			currentPieceIsWhite = movedPiece.getIsWhite()
			
			# check that the current piece is the same colour as the current turn
			if currentPieceIsWhite == self.getCurrentTurnIsWhite():

				# check if the requested move belongs to the set of moves that piece can move to
				if [new_row, new_col] in self._board[orig_row][orig_col].getMoves(self,orig_row,orig_col,self.getLastMove()):
					
					
					# check to see if this move would place us in check
					if (not self.previewMove(orig_row,orig_col,new_row,new_col)):
					
						# move the current piece into the new space	
						self._board[new_row][new_col] = movedPiece
						self._board[orig_row][orig_col] = None
						
						
						
						
						#pawn promotion check
						if (isinstance(movedPiece, Pieces.Pawn) and (new_row == self.getHeight()-1 or new_row == 0)):
							while True:
								choice = input('What would you like to promote this pawn to? (Rook, Knight, Bishop, Queen):')
								
								if (choice == 'Rook'):
									self._board[new_row][new_col] = Pieces.Rook(currentPieceIsWhite)
									break
								if (choice == 'Knight'):
									self._board[new_row][new_col] = Pieces.Knight(currentPieceIsWhite)
									break
								if (choice == 'Bishop'):
									self._board[new_row][new_col] = Pieces.Bishop(currentPieceIsWhite)
									break
								if (choice == 'Queen'):
									self._board[new_row][new_col] = Pieces.Queen(currentPieceIsWhite)
									break
								else:
									print('That\'s not a valid answer ya mook')			
						
						
						# gets the last move to check if move was en passant, remove piece....
						lastMove = self.getLastMove()
						
						# if current piece and last moved piece are pawns and last moved pawn moved in the same column and the current pawn moved in that column and the current pawn is from another column
						if (isinstance(movedPiece, Pieces.Pawn) and lastMove != None and isinstance(self._board[lastMove[2]][lastMove[3]], Pieces.Pawn) and lastMove[1] == lastMove[3] and new_col == lastMove[3] and orig_col != new_col):
							
							# remove the en-passanted pawn
							self._board[lastMove[2]][lastMove[3]] = None
						
						# change the current turn to the next player
						self.flipCurrentPlayerColour()
						
						# save this move as the last move made (for en passant rule)
						self.setLastMove(someArray)
					
					#beginning of some informative if not slightly alarming messages
					else:
						print('That would either place you or you currently are in check. Try again,')
					
				else:
					print('Invalid move, try doing one of the listed ones!')
			else:
				print('That isn\'t your piece. Cheating is frowned upon <3')
		else:
			print('That... that is an empty square. Where are you planning on moving nothing to?')
			
		return True
	
	# only used internally, returns true if move would place the player in check
	#TODO implement en passant pawn removal and replacement
	def previewMove(self,orig_row,orig_col,new_row,new_col):
	
		returnVal = False
		
		# gets the current piece type and colour
		pieceToMove = self._board[orig_row][orig_col]
		currentColour = pieceToMove.getIsWhite()
		
		# save the original piece and move the new one into it's spot.
		originalPiece = self._board[new_row][new_col] 		
		self._board[new_row][new_col] = pieceToMove
		self._board[orig_row][orig_col] = None
				
		# set return value to be true if this would place or maintain the position of being in check
		if (self.checkIsInCheck(currentColour)):
			returnVal = True	
		
		# reset the board
		self._board[new_row][new_col] = originalPiece		
		self._board[orig_row][orig_col] = pieceToMove
		
		return returnVal

	# runs Piece.getMove() for all pieces on the board	
	def getAllMoves(self, isWhite):
		
		# create an empty dictionary
		moveDictionary = {}
	
		# for every row in the board
		for row in range(0, self.getHeight()):
		
			# for every column in that row
			for col in range(0, self.getWidth()):
			
				# if the space contains a piece and that piece is of the current player's colour
				if (self._board[row][col] != None and self._board[row][col].getIsWhite() == isWhite):
				
					# adds to the dictionary a tuple key (pieceType, row, col) and the array of that piece's possible moves
					moveDictionary[(self._board[row][col].getPieceName(), row,col)] = self._board[row][col].getMoves(self,row,col,self.getLastMove())
	
		return moveDictionary

	# returns True if in check, returns False if not in check
	def checkIsInCheck(self, isWhite):
		
		# create an empty array to store the king's location on the board
		kingLocation = []
		
		# for every row in the board
		for row in range(0, self.getHeight()):
		
			# for every column in the row
			for col in range(0, self.getWidth()):
			
				# if the piece is the current turn's king
				if (not self.isSpaceFree(row,col) and isinstance(self._board[row][col], Pieces.King) and self._board[row][col].getIsWhite() == isWhite):
				
					# save the location
					kingLocation = [row,col]
		
		# get all the moves of the opponenet	
		opponentMoves = self.getAllMoves(not isWhite)
		
		# for every move that the opponent can make
		for moveSet in opponentMoves:
			
			# check if the move would intersect/be on the same square as the king
			if any(i == kingLocation for i in opponentMoves[moveSet]):
				return True
				
		# if no opponent move intersects the king's space, return False
		return False
	
	# returns True if in checkmate, returns False if not
	def checkIsInCheckmate(self, isWhite):
		
		# get all the possible moves that the current player can make
		moveDictionary = self.getAllMoves(isWhite)
		
		# for every move that can be made
		for moveSet in moveDictionary:
		
			for move in moveDictionary[moveSet]:
			
				# check if the move would not place or maintain a state of being in check
				if (self.previewMove(moveSet[1],moveSet[2],move[0],move[1]) == False):
					return False		
		return True
				

					
def main():
	someBoard = ChessBoard()
	someBoard.resetBoard()
	input('hit enter to begin game loop')
	
	while True:

		someBoard.printBoard()
		currentTurnIsWhite = someBoard.getCurrentTurnIsWhite()
		
		
		print('-------------------------\n')
		print('moves for: {}'.format('white' if someBoard.getCurrentTurnIsWhite() else 'black'))
		print('{}'.format('You are in check!' if someBoard.checkIsInCheck(currentTurnIsWhite) else ''))
		
		if (someBoard.checkIsInCheckmate(currentTurnIsWhite)):
			print('{} lost the game! haha, sucker!'.format('white' if someBoard.getCurrentTurnIsWhite() else 'black'))
			return
		
		currentMoves = someBoard.getAllMoves(currentTurnIsWhite)
		for moveSet in currentMoves:
			print ('{} {}'.format(moveSet, currentMoves[moveSet]))
			
		try:
			someArray = list(map(int, input('enter move: ').split(',')))
			someBoard.movePiece(someArray)
			
		except:
			print('that doesn\'t look right. Try again')
				
		input('hit enter to clear')
		

if __name__ == "__main__":
	main() 




