# OverFit-Game
OverFit Game is a fun arcade game, partly based on the PS3 game [Critter Crunch](http://www.capybaragames.com/critter-crunch-psn/)

## Requirements
- Python 3.5+
- PyGame 1.9.6
- PyZmq 18.0.1
- SQLAlchemy 1.2.12
- SQLite

## Installation
Simply clone the repository to your desired destination.
```bash
git clone git@github.com:samuelmovi/overfit-game.git
```

## Usage
### Welcome Screen
It has three buttons:

- Single Player: takes you straight to the game screen in single-player mode
- Online: takes you to to online settings screen
- Settings: takes you to the settings screen


### Settings screen
Here there are 2 fields to fill-up:

- Online Host: server's IP address
- Player Name: this text will appear as the player name in its own game screen, and as the opponent's name in the opponent's game screen in online-play mode.

The return key must be pressed for the input to be taken in by the program.


### Online Setting Screen
It has the same input fields as the normal settings screen, and an extra button. The return key doesn't need to be pressed in this case.

The button under the fields stars the online broker, which connects to the server, authenticates, and searches for available players [AP]. If one is found the will connect and the game will be started for both. If, otherwise, no AP is found, the client will enter a wait mode, until another client challenges the AP.

During these operations, a wait-screen with different text will be shown to the client, informing them of their state.

### Game Screen
It's composed of mainly 2 sections: the information column on the left of the screen, and the rest of the screen where the action takes place [the board].

The information column is divided into 2 equal sections:

- Top section: shows the local player's name on top and, below, the information about that player's state: score, total number of figures in screen, longest column. 
- Bottom section: it has the same elements but displaying information about the opponent.

In cases of single-player games, that bottom half remains blank.


### Confirmation screens
From any screen in the game, if you press ESC key, a confirmation screen will pop-up asking you to confirm an action. Doing this in the welcome screen would prompt a question about leaving the game. In any other screen, it would ask about returning to the main screen.

Underneath the question will be 2 buttons, one for YES and one for NO. Click accordingly.

Pressing ESC while on the confirmation screen should be interpreted as clicking NO.

## Gameplay
### The Board
For lack of a better word, I'll use this word to refer to the part of the game screen where the playing happens. We could divide this board into 2 main sections:

- Taking the top 80% of the board is a series of seven columns, delimited by white vertical lines, which is where Figures are places.
- The bottom section, free of any lines, is where the player's character moves.

### The Figures
There are 5 types of figures:

- Dots: small white circle.
- Triangles: they have a small circle-shaped hole in them.
- Squares: they have a small circle-shaped hole in them.
- Triangle-holes: squares with triangle-shaped hole in them.
- Square-holes: squares with square-shaped hole in them.

You can fit dots into triangles and squares.
You can fit triangles in triangle-holes.
You can fit squares in square-holes.

If a figure's hole is full when it tries to be fitted with another one, this will cause an "OverFit", which will cause the involved figures to explode. If the exploding overfit figure is placed above, below, to the right or left, of a figure of the same kind this one will explode as well, no matter its state.

### The Player

The player is represented by a big white circle.
It moves left and right, in the bottom of the screen, below the columns [using arrow keys]. 
It has as many positions as there are columns.
It has one action button [space bar] which does one of 2 things:

- If the player is empty it will shoot a ray to capture the lowest figure in the column right above it, removing it from said column, and changing its pown state to full (represented by a small orange circle inside the player).
- If the player is full it will shoot its ray to return the figure to the column above the player (whichever onw it is). If column is full the player will be unable to do so.


## But, what's the game really about?
The purpose of the game is to score as many points as possible as efficiently as possible.

The scoring works by awarding points based on the figures destroyed:

- Dots: 1 point
- Squares/Triangles: 2 points
- Square-hole/Triangle-holes: 3 points

When figures are fitted, its score will include the value of the fitted figure as well.

To balance things out, and so it's fun, a new row of figures is added to a player's board under certain conditions:

- If the total figure count on a player's board is less than 15
- For every 15 moves the player does
- If playing online, for every 20 points your opponent makes

## Online Multiplayer
The online gaming protocol is built using ZeroMQ (through PyZmq), for the transport layer and for authentication, using ZMQ's custom ED22519 certificates.

### Server
The server script binds to 2 ports:

- Port 5555: PULL 
- Port 5556: PUB

Server receives messages from a PULL, processes them, and publishes them.

### Client
The client connects to 2 ports:

- Port 5555: PUSH
- Port 5556: SUB

### Protocol

- CLIENT clicks button `Find match` on landing page screen and sends SERVER a message with command `FIND`
- Upon receipt SERVER checks `available_players`:
    - If none are found it adds player ID to `available_players` and responds to CLIENT with `WAIT`
    - If an available player is found SERVER send both of them a `READY` message.
- Both CLIENTS must respond (could be time sensitive failover) with `READY` client status
- SERVER responds to both after last client has acknowledged with command `PLAY`
- CLIENTS will set their status as `PLAYING` and start their match


### Packets

There are client messages, and server messages.

All of them have 3 parts.

#### Client message 

Sent by client to communicate with server:

- Sender: player ID (unique 10-character random string)
- Info (json): 
    - client status: WELCOME, AVAILABLE, READY, START, PLAYING, OVER, QUIT 
    - recipient: `SERVER` or player ID
- Payload (json): match and player data

#### Server message 

Published by server:

- Recipient: player ID 
- Info (json): 
    - sender: `SERVER` or player ID
    - command: WELCOME, WAIT, READY, PLAY, WINNER
- Payload (json): forwarded payload 


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GPLv2](https://choosealicense.com/licenses/gpl-2.0/)
