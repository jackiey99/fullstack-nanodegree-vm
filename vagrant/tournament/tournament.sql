-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- in case you have the tables with the same name defined in the tournament database

-- note the order of dropping tables, match depends on player, so drop match first

DROP  DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;
\c tournament;

CREATE TABLE player (
	pid serial primary key,
	name varchar(50)
);

CREATE TABLE match (
	winner integer references player (pid),
	loser integer references player (pid)
);
