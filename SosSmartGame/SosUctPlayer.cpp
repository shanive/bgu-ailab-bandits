//------------------------------------------------------------
/**
@file SosUctPlayer.cpp
UCT based SOS player.
*/
//-------------------------------------------------------------

#include "SosPlayer.h"
#include "SosGame.h"
#include "SosUctSearch.h"

SosUctPlayer::SosUctPlayer(SosGame *game)
		: m_game(game),
		  m_search(0)
{
}

SosUctPlayer::~SosUctPlayer()
{
}

SosUctPlayer::genMove(SosState *state)
{
	SgBlackWhite color;
	if (state->isWhiteTurn())
		color = SG_WHITE;
	else
		color = SG_BLACK;
	
	SosUctThreadStateFactory factory(this->game, state, color);
	
	this->m_search = new SgUctSearch(&factory, state->size());



}