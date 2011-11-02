//------------------------------------------------------
/**
@file SosUctPlayer.h
uses smartgame library.
*/

#include "SosPlayer.h"
#include "SosUctSearch.h"

class SosGame;
class SosState;
class SgMove;

class SosUctPlayer
	: public SosPlayer
{
public:
	/**
	constructor.
	@param game
	*/
	SosUctPlayer(SosGame *game);

	/**
	destructor
	*/
	~SosUctPlayer();
	
	/**
	@param state current state of a game.
	@return next move.
	*/
	SgMove genMove(SosState *state);

private:
	SosGame *m_game;
	
	SosUctSearch *m_search;
};

