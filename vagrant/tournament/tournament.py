#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM match;")

    conn.commit()
    conn.close()



def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    c = conn.cursor()
    c.execute("DELETE FROM player;")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""

    conn = connect()
    c = conn.cursor()

    # count the number of rows in the player table
    c.execute("SELECT COUNT(*) FROM player;")
    conn.commit()
    result = c.fetchone()
    conn.close()
    return result[0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """

    conn = connect()
    c = conn.cursor()

    # insert this player into the player table
    c.execute("INSERT INTO player (name) VALUES (%s);", (name,) )
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """

    conn = connect()
    c = conn.cursor()

    # I get the standings by a rather single long sql query, here is the steps:
    # 1. from the match table, count the players' winning mathces, call it a winTable, similarly get a loseTable
    # 2. full join the winTable and loseTable, order by winning coounts and call it matchStat
    # 3. right join the matchStat with player table, and get the standings table
    long_sql = ("SELECT player.pid, player.name, COALESCE(matchStat.wins, 0) as wins, COALESCE(matchStat.wins + matchStat.losts, 0) as matches from " 
                " (SELECT COALESCE(winTable.pid,loseTable.pid) as pid, COALESCE(winTable.wins,0) as wins, COALESCE(loseTable.losts,0) as losts FROM "
                " (SELECT winner as pid, COUNT(winner) as wins from match GROUP BY winner) AS winTable FULL JOIN "
                " (SELECT loser as pid, COUNT(loser) as losts from match GROUP BY loser) AS loseTable ON winTable.pid = loseTable.pid ORDER BY winTable.wins DESC)"
                " AS matchStat RIGHT JOIN player On matchStat.pid = player.pid;"
               )
    c.execute(long_sql)

    conn.commit()
    result = c.fetchall()
    conn.close()
    return result



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn = connect()
    c = conn.cursor()

    # add this match to the match table
    c.execute("INSERT INTO match VALUES (%s, %s);", (winner, loser))

    conn.commit()
    conn.close()
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    # get the players' standings and pair every two players in the standings

    standings = playerStandings()
    result = []

    for i in xrange(0, len(standings), 2):
        player1 = standings[i]
        player2 = standings[i + 1]
        id1, name1 = player1[0], player2[1]
        id2, name2 = player2[0], player2[1]
        result.append((id1, name1, id2, name2))

    return result

