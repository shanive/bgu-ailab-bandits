#include "SosPlayer.h"
#include "SosGame.h"

SosPlayer::~SosPlayer(){
}

SosRandomPlayer ::SosRandomPlayer(SosGame *game)
				: m_game(game)
{
}

SosRandomPlayer::~SosRandomPlayer()
{
}

SgMove SosRandomPlayer::genMove(SosState *state)
{
	std::vector<SgMove> availableMoves = state->availableMoves();

	int index =  rand() % availableMoves.size();

	return availableMoves.at(index);
}

SosLeftPlayer::SosLeftPlayer(SosGame *game)
				: m_game(game)
{
}

SosLeftPlayer::~SosLeftPlayer()
{
}

SgMove SosLeftPlayer::genMove(SosState *state)
{
	std::vector<SgMove> availableMoves = state->availableMoves();
	return availableMoves.at(0);
}
