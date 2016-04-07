# Tournament Results

In this project, I implement the swiss trounament for an even number of players, where the database stores the player records and match records.


## Usage

- Clone the repo 

```bash
$ git clone https://github.com/jackiey99/fullstack-nanodegree-vm.git
```

- Go the directory ./vagrant/tournament 

- Create the tournament database, connect to it and create two tables -- player and match

```bash
$ psql
$ \i tournament.sql
```
- Exit the psql command line and run the python test script

```bash
$ \q
$ python tournament_test.py
```

## Future work

- Handle odd number of players
- Prevent rematches between players (need to check if the match exist in the match table)