//------------------------------------------------------
/**
@file SosUctPlayer.h
uses smartgame library.
*/

#include "SosPlayer.h"
#include "SosUctSearch.h"
#include "SgMove.h"
class SosGame;
class SosState;


class SosUctPlayer
	: public SosPlayer
{
public:
	/**
	constructor.
	@param game SOS game.
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
};

