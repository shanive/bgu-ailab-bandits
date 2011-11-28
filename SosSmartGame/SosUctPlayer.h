//------------------------------------------------------
/**
@file SosUctPlayer.h
uses smartgame library.
*/

#include "SosPlayer.h"
#include "SosUctSearch.h"
#include "SgMove.h"
#include "SgUctValue.h"
class SosGame;
class SosState;


class SosUctPlayer
	: public SosPlayer
{
public:
	/**
	constructor.
	@param game SOS game.
        @maxGames Number Of games Per State.
	*/
  SosUctPlayer(SosGame *game , SgUctValue maxGames );

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
        SgUctValue m_maxGames;
};

