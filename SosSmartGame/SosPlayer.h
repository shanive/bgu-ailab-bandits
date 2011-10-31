//------------------------------------------------------
/** @file SosPlayer.h
Interface of a simple SOS player.
*/
//------------------------------------------------------


#ifndef SOS_PLAYER_H
#define SOS_PLAYER_H

#include "/users/studs/bsc/2011/shanive/freespace/bgu-ailab-bandits/fuego-1.1/smartgame/SgMove.h"

class SosGame;
class SosState;

class SosPlayer
{
public:
	
	virtual ~SosPlayer();
	/**
	@param state The current state of the game.
	@return The next move to execute.
	*/
	virtual SgMove genMove(SosState *state) = 0;

};

//--------------------------------------------
/** Plain Random Sos Player for tests */

class SosRandomPlayer
	: public SosPlayer
{

public:
	SosRandomPlayer(SosGame *game);

	virtual ~SosRandomPlayer();

	SgMove genMove(SosState *state);

private:

	SosGame *m_game;

};


//------------------------------------------------
/** Plain Random Sos Player for tests */

class SosLeftPlayer
	: public SosPlayer
{

public:
	SosLeftPlayer(SosGame *game);

	virtual ~SosLeftPlayer();

	SgMove genMove(SosState *state);

private:

	SosGame *m_game;

};


#endif // SOS_PLAYER_H
