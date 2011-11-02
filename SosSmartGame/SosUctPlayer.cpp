//------------------------------------------------------------
/**
@file SosUctPlayer.cpp
UCT based SOS player.
*/
//-------------------------------------------------------------
#include <limits>
#include <vector>
#include "SosPlayer.h"
#include "SosGame.h"
#include "SosUctSearch.h"
#include "SgUctTree.h"
#include "SgUctValue.h"
#include "SgMove.h"

SosUctPlayer::SosUctPlayer(SosGame *game)
		: m_game(game)
{
}

SosUctPlayer::~SosUctPlayer()
{
}

SgMove SosUctPlayer::genMove(SosState *state)
{
	std::vector<SgMove> sequence; 
	SgBlackWhite color;
	double maxTime = numeric_limits<double>::max();
	SgUctValue maxGames = static_cast<SgUctValue>(maxTime);
	
	if (state->isWhiteTurn())
		color = SG_WHITE;
	else
		color = SG_BLACK;
	
	SosUctThreadStateFactory factory(this->game, state, color);
	SgUctSearch *search = new SgUctSearch(&factory, state->size());
	//setings of this->m_search
	search->Search(maxGames, maxTime, sequence);
	
	delete search;
	
	return sequence.at(0);
}