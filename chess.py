from env.game import Game

if __name__ == '__main__':
    game = Game()
    winner = game.play()
    print(f"{winner} wins.")
    game.report()
