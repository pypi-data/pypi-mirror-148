# cl_games

This package can be used for building basic video games using the command line.

## Usage

For creating a game, extend the clase "Game" and use "Game.run"

`import cl_games

class MainGame(cl_games.Game):

    """docstring for MainGame."""

    def __init__(self):

        super(MainGame, self).__init__()

        self.title = "My New Game"

    def update(self):

        #This is run every frame


game = MainGame()

game.run()
`
To add a sprite, extend class sprite

`class Player(cl_games.sprites.Sprite):

    def __init__(self, game):

        super(Player, self).__init__(game)

        self.image = [

            "  ^  ",

            " / \ ",

            "/___\\"

        ]

        self.posX, self.posY = 18, 17

        self.setLengthToImage()

    def update(self):

        #Also run every frame

game.addSprite(Player(game))

`



To stop the game, just set the running variable to false on game

`game.running = false`
