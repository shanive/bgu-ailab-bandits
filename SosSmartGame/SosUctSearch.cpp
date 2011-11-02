//----------------------------------------------------------------------------
/** @file SosUctSearch.cpp */
//----------------------------------------------------------------------------
#include <vector>
#include "SosUctSearch.h"
#include "SgBlackWhite.h"
#include "SgUctTree.h"
#include "SgUctValue.h"
#include "SgUctSearch.h"
#include "assert.h"
#include "SosGame.h"
#include <stdlib.h>

SosUctThreadState::SosUctThreadState(unsigned int threadId, SgBlackWhite color, SosGame* game, SosState* state)
    : SgUctThreadState(threadId, state->size()),
      m_game(game),
      m_color(color),
      m_gameState(state)

{
    this->m_isInPlayout = false;
}

SosUctThreadState::~SosUctThreadState()
{
}

SgUctValue SosUctThreadState::Evaluate()
{
	assert(this->m_game->isFinalState(*this->m_gameState));
	return static_cast<SgUctValue>(this->m_game->gameScore(*this->m_gameState));
}

void SosUctThreadState::Execute(SgMove move)
{
    assert(! this->m_isInPlayout);
    this->m_gameState->play(move);
}

void SosUctThreadState::ExecutePlayout(SgMove move)
{
    assert(this->m_isInPlayout);
    this->Execute(move);
}

bool SosUctThreadState::GenerateAllMoves(SgUctValue count, 
                                  std::vector<SgUctMoveInfo>& moves,
                                  SgUctProvenType& provenType)
{
    moves.clear();

    if (this->m_game->isFinalState(*this->m_gameState)){
        if (((this->Evaluate() > this->m_game->komi()) && (this->m_color == SG_WHITE)) 
		|| ((this->Evaluate() < this->m_game->komi()) && (this->m_color == SG_BLACK)))
		provenType = SG_PROVEN_WIN;
	else
		provenType = SG_PROVEN_LOSS;	
	return true;
    }
    else{
	std::vector<SgMove> availableMoves = this->m_gameState->availableMoves();
	std::vector<SgMove>::const_iterator it;
	
	for (it = availableMoves.begin(); it != availableMoves.end(); ++it){
		moves.push_back(SgUctMoveInfo(*it));
    	}
	provenType = SG_NOT_PROVEN; 
    }
    return false; 
}  

SgMove SosUctThreadState::GeneratePlayoutMove(bool& skipRaveUpdate)
{
	std::vector<SgMove> availableMoves = this->m_gameState->availableMoves();

	int index =  rand() % (availableMoves.size() + 1);

	skipRaveUpdate = false;
	return availableMoves.at(index);
}

void SosUctThreadState::GameStart()
{
    this->m_isInPlayout = false;
}

// void SosUctThreadState::StartPlayout()
// {
//    
// }

void SosUctThreadState::StartPlayouts()
{
    this->m_isInPlayout = true;
}

void SosUctThreadState::StartSearch()
{

}

void SosUctThreadState::TakeBackInTree(std::size_t nuMoves)
{
    this->m_gameState->undo(static_cast<int>(nuMoves));
}

void SosUctThreadState::TakeBackPlayout(std::size_t nuMoves)
{
    this->m_gameState->undo(static_cast<int>(nuMoves));
}

//---------------------------------------------------------------------------------------

SosUctThreadStateFactory::SosUctThreadStateFactory(SosGame *game, 
					SgBlackWhite color, 
					SosState *state)
				: m_game(game),
				  m_color(color), 
				  m_state(state)
{
}

SosUctThreadStateFactory::~SosUctThreadStateFactory()
{
}

SgUctThreadState* SosUctThreadStateFactory:: Create(unsigned int threadId,
                                     		const SgUctSearch& search)
{
	return new SosUctThreadState(threadId, this->m_color, this->m_game, 
					 this->m_state);
}

//----------------------------------------------------------------------------

