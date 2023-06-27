# 9-mens-morris

## Game Instructions and Brief

Nine Men's Morris is a strategic board game that dates back to ancient times. It is played on a grid board with three concentric squares connected by lines, forming a total of 24 intersection points. The goal of the game is to form "mills," which are lines of three connected pieces.

At the start, each player has nine pieces of a specific color. Players take turns placing their pieces on the intersection points of the board. Once all pieces are placed, players can then move their pieces along the lines to adjacent points in an attempt to form mills. Whenever a mill is formed, the player who made it can remove one of their opponent's pieces from the board, except if the opponent's piece is part of another mill.

The game continues until one player has only two pieces left, making them unable to form a mill. At this point, the player with two pieces loses the game. However, if a player is left with only three pieces, they are allowed to "fly" and move their pieces to any vacant point on the board.

In the developed game, two game modes are available. The first mode is Player versus Player (PvP), where two human players take turns playing against each other. They can strategize, place their pieces, and make moves to outwit their opponent. The second mode is Player versus Computer, where a single player can play against an AI-controlled opponent. 

Both game modes offer the opportunity to test strategic thinking, planning, and decision-making skills. Players aim to create mills, block their opponent's moves, and strategically position their pieces to gain an advantage. The game combines positioning, tactics, and anticipation elements to create an engaging and competitive experience.

## Instructions to run the game

*cd into the `project/` directory*

*run the game by running the excecutables from the dist folder according to the operating system you are using by using the following command:*

**`./dist/application-{operating-system}`**

------------------------------------------------------------------------------------
If you have a mac with an intel chip or cannot get the excecutable to run, try the following steps:

    **run the following command to download dependencies**
    *it is reccomened that you activate a virtual enviroment first*

       pip3 install -r requirements.txt

    ## MAKE SURE YOU ARE IN THE PROJECT DIRECTORY

    **to run the game run the game use the command**
        python3 ./src/application.py
