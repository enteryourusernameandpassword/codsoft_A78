class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.human = 'X'
        self.ai = 'O'
        
    def print_board(self):
        for i in range(0, 9, 3):
            print(f' {self.board[i]} | {self.board[i+1]} | {self.board[i+2]} ')
            if i < 6:
                print('-----------')
                
    def is_winner(self, player):
        # Check rows
        for i in range(0, 9, 3):
            if all(self.board[i+j] == player for j in range(3)):
                return True
        # Check columns
        for i in range(3):
            if all(self.board[i+j*3] == player for j in range(3)):
                return True
        # Check diagonals
        if all(self.board[i] == player for i in [0, 4, 8]):
            return True
        if all(self.board[i] == player for i in [2, 4, 6]):
            return True
        return False
    
    def is_board_full(self):
        return ' ' not in self.board
    
    def get_empty_cells(self):
        return [i for i, cell in enumerate(self.board) if cell == ' ']
    
    def make_move(self, position, player):
        if self.board[position] == ' ':
            self.board[position] = player
            return True
        return False
    
    def minimax(self, depth, is_maximizing, alpha, beta):
        if self.is_winner(self.ai):
            return 1
        if self.is_winner(self.human):
            return -1
        if self.is_board_full():
            return 0
        
        if is_maximizing:
            best_score = float('-inf')
            for move in self.get_empty_cells():
                self.board[move] = self.ai
                score = self.minimax(depth + 1, False, alpha, beta)
                self.board[move] = ' '
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score
        else:
            best_score = float('inf')
            for move in self.get_empty_cells():
                self.board[move] = self.human
                score = self.minimax(depth + 1, True, alpha, beta)
                self.board[move] = ' '
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score
    
    def get_best_move(self):
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        for move in self.get_empty_cells():
            self.board[move] = self.ai
            score = self.minimax(0, False, alpha, beta)
            self.board[move] = ' '
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    
    def play_game(self):
        print("Welcome to Tic-Tac-Toe!")
        print("You are X and the AI is O")
        print("Positions are numbered from 0-8, left to right, top to bottom")
        
        while True:
            self.print_board()
            
            # Human turn
            while True:
                try:
                    position = int(input("Enter your move (0-8): "))
                    if 0 <= position <= 8 and self.make_move(position, self.human):
                        break
                    else:
                        print("Invalid move, try again")
                except ValueError:
                    print("Please enter a number between 0-8")
            
            # Check if human won
            if self.is_winner(self.human):
                self.print_board()
                print("Congratulations! You won!")
                break
            
            # Check if board is full
            if self.is_board_full():
                self.print_board()
                print("It's a tie!")
                break
            
            # AI turn
            print("\nAI is thinking...")
            ai_move = self.get_best_move()
            self.make_move(ai_move, self.ai)
            
            # Check if AI won
            if self.is_winner(self.ai):
                self.print_board()
                print("AI wins! Better luck next time!")
                break
            
            # Check if board is full
            if self.is_board_full():
                self.print_board()
                print("It's a tie!")
                break

if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
