# Online Multiplayer Chess
Description: An online multiplayer chess game. Supports infinite players playing against random opponents on different machines on different networks. This project was created using python 3.7, pygame and the sockets module from python3. It runs on a basic client server system where a server script handles all incoming connections and game management. The clients simply hanlde the UI and game play.


# Required:
- Python 3.x
- pygame


# May 22 Livestream game install instructions:
- Install python 3.x and pygame on your machine (Windows: https://www.youtube.com/watch?v=AdUZArA-kZw , MAC: https://www.youtube.com/watch?v=E-WhAS6qzsU)
- Dowload this repo to your machine
- Run the game.py python file
- Click anywhere in the pygame window to queue for a game
- Wait for a player to join your game and the game will begin
- If you wish to leave just close the window or hit q
- After a game is finished you will be brought back to the main menu where you can queue again


# TO MAKE THIS CODE WORK...
*Ignore this if you are here from the livestream.*
You will need to change the server address from within the following two files:
- client.py
- server.py

You will also need to run server.py on some kind of server. After that you can launch two instances of game from anywhere to play online chess.


# Known Bugs:
- Checkmate does not work, if you loose or win you will need to end the game by hitting "q"
- Very rare bug where a certain move will crash the game
- No Enpesant Pawn Rule


# LICENSE:
*NOT FOR COMMERCIAL USE*
If you intened to use any of my code for commercial use please contact me and get my permission. If you intend to make money using any of my code please ask my permission.
