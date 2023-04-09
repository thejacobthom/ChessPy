
SIGN_LIST = [1,-1]

class Piece:
	def __init__(self, isWhite):
		self._isWhite = isWhite
		self._pieceType = 'Undeclared'
	
	# begin getter and setter methods
	def getIsWhite(self):
		return self._isWhite
		
	def getPieceType(self):
		return self._pieceType
		
	def printPiece(self):
		print (self.getPieceName())
		
	# end getter and setter methods
	
	# formats and prints piece name
	def getPieceName(self):
		return ('White {}'.format(self._pieceType) if self._isWhite else 'Black {}'.format(self._pieceType))
	
	# gets the possible non-diagonal moves from the current position
	def getNonDiagonalMoves(self, currentBoard, row, col, isWhite):
		moves = []
		
		# to check up and down
		for sign in SIGN_LIST:
		
			# to begin the row adjustment
			i = 1*sign
			
			#check for first hit in that direction
			isFirstHit = True
			
			# first check if within board constraints, then if 'piece' is empty or is an enemy piece, and finally that we haven't hit anything yet
			while (0 <= row+i < currentBoard.getWidth() and (currentBoard.getBoard()[row+i][col] == None or currentBoard.getBoard()[row+i][col].getIsWhite() != isWhite) and isFirstHit == True):
				
				# if first hit of enemy, record it so we do not progress further
				if (currentBoard.getBoard()[row+i][col] != None):
					isFirstHit = False

				moves.append([row+i, col])
				
				i += 1*sign # add one, uses sign to maintain flip between left/right or infront/behind
			
		# to check left and right
		for sign in SIGN_LIST:
		
			# to begin the column adjustment
			i = 1*sign
			
			#check for first hit in that direction
			isFirstHit = True
			
			# first check if within board constraints, then if 'piece' is empty or is an enemy piece, and finally that we haven't hit anything yet
			while (0 <= col+i < currentBoard.getHeight() and (currentBoard.getBoard()[row][col+i] == None or currentBoard.getBoard()[row][col+i].getIsWhite() != isWhite) and isFirstHit):

				# if first hit of enemy, record it so we do not progress further
				if (currentBoard.getBoard()[row][col+i] != None):
					isFirstHit = False
				
				moves.append([row, col+i])
				
				i += 1*sign # add one, uses sign to maintain flip between left/right or infront/behind
		
		return moves
	
	# gets the possible diagonal moves from the current position
	def getDiagonalMoves(self, currentBoard, row, col, isWhite):
		moves = []
		
		# to check positive slope and negative slopes
		moveMultipliers = [[1,1],[-1,1]]
		
		# to check both directions from origin for both slopes
		for sign in SIGN_LIST:
		
			# for each slope
			for moveMultiplier in moveMultipliers:

				# get additions to use for this direction of the slope
				moveAddition = [moveMultiplier[0]*sign,moveMultiplier[1]*sign]
				
				# set the initial step count in X direction
				i = 1
				
				#check for first hit in that direction
				isFirstHit = True
				
				# get the values for the new space to check, using the slope direction and the current step
				newRow = row + (moveAddition[0]*i)
				newCol = col + (moveAddition[1]*i)
				
				
				# while within the boundries of the board and the new space is empty or of the opponent colour and is the first hit
				while (0 <= newRow < currentBoard.getWidth() and 0 <= newCol < currentBoard.getHeight() and (currentBoard.getBoard()[newRow][newCol] == None or currentBoard.getBoard()[newRow][newCol].getIsWhite() != isWhite) and isFirstHit):
					
					
					# if first hit of enemy, record it so we do not progress further
					if (currentBoard.getBoard()[newRow][newCol] != None):
						isFirstHit = False
					
					# record the move in the list
					moves.append([newRow, newCol])
					
					# get thew next row and column
					i+=1
					newRow = row + (moveAddition[0]*i)
					newCol = col + (moveAddition[1]*i)
		return moves
		
	
	def getMovesFromArray(self, currentBoard, row, col, isWhite, moveArray):
		moves = []
		
		# for every move addition in the given array
		for possibleMoveAdditions in moveArray:
		
			# get the new row and column using that addition
			newRow = row + possibleMoveAdditions[0]
			newCol = col + possibleMoveAdditions[1]
			
			
			# if the move is within bounds and the space is free or of opponenent colour
			if (0<= newRow < currentBoard.getWidth() and 0<= newCol < currentBoard.getHeight() and (currentBoard.isSpaceFree(newRow,newCol) or currentBoard.getBoard()[newRow][newCol].getIsWhite() != self._isWhite)):
				
				# record the move in the list
				moves.append([newRow, newCol])
				
		return moves
		
	
	def getPawnMoves(self, currentBoard, row, col, isWhite, lastMove):
		moves = []
		sign = 1 if isWhite else -1	# determining which way to move
		
		# can move in front to empty space
		if (0 <= row+1 < currentBoard.getHeight() and currentBoard.getBoard()[row+sign][col] == None):
			moves.append([row+sign,col])
	
		# can move to the col on the right if occupied by opponent
		if (0 <= row+1 < currentBoard.getHeight() and col+1 < currentBoard.getWidth() and currentBoard.getBoard()[row+sign][col+1] != None and currentBoard.getBoard()[row+sign][col+1].getIsWhite() != self._isWhite):
			moves.append([row+sign,col+1])
		
		# can move to the col on the left if occupied by opponent
		if (0 <= row+1 < currentBoard.getHeight() and col-1 < currentBoard.getWidth() and currentBoard.getBoard()[row+sign][col-1] != None and currentBoard.getBoard()[row+sign][col-1].getIsWhite() != self._isWhite):
			moves.append([row+sign,col-1])
			
			
		# en-passant logic:
		# check if piece is a pawn and moved in the same columnm 
		if (lastMove != None and isinstance(currentBoard.getBoard()[lastMove[2]][lastMove[3]], Pawn) and lastMove[1] == lastMove[3]):
			
			#check right
			if (lastMove[3] == col+1):
				moves.append([row+sign,col+1])
		
			#check left
			if (lastMove[3] == col-1):
				moves.append([row+sign,col-1])
		
		return moves
		
	def getMoves(self, board, row, col, lastMove = None):
		print('Not yet implemented')
		return []

class Queen(Piece):
	def __init__(self, isWhite):
		self._isWhite = isWhite
		self._pieceType = 'Queen'
	
	def getMoves(self, board, row, col, lastMove = None):
		moves = self.getNonDiagonalMoves(board, row, col, self.getIsWhite())
		moves += self.getDiagonalMoves(board, row, col, self.getIsWhite())
		return moves
	
class King(Piece):
	def __init__(self, isWhite):
		self._isWhite = isWhite
		self._pieceType = 'King'
		
	def getMoves(self, board, row, col, lastMove = None):
		moveArray = [[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]] # possible moves for a king, all adjacent areas
		
		return self.getMovesFromArray(board,row, col, self.getIsWhite(), moveArray)


class Bishop(Piece):
	def __init__(self, isWhite):
		self._isWhite = isWhite
		self._pieceType = 'Bishop'
	def getMoves(self, board, row, col, lastMove = None):
		return self.getDiagonalMoves(board, row, col, self.getIsWhite())

class Knight(Piece):
	def __init__(self, isWhite):
		self._isWhite = isWhite
		self._pieceType = 'Knight'
		
	def getMoves(self, board, row, col, lastMove = None):
		moveArray = [[2,1],[2,-1],[-2,1],[-2,-1],[1,2],[1,-2],[-1,2],[-1,-2]] # possible moves for a knight, all possible L movements
		
		return self.getMovesFromArray(board,row, col, self.getIsWhite(), moveArray)

class Rook(Piece):
	def __init__(self, isWhite):
		self._isWhite = isWhite
		self._pieceType = 'Rook'
		
	def getMoves(self, board, row, col, lastMove = None):
		return self.getNonDiagonalMoves(board, row, col, self.getIsWhite())


class Pawn(Piece):
	def __init__(self, isWhite):
		self._isWhite = isWhite
		self._pieceType = 'Pawn'
	def getMoves(self, board, row, col, lastMove = None):
		return self.getPawnMoves(board, row, col, self.getIsWhite(), lastMove)







