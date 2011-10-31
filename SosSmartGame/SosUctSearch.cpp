//----------------------------------------------------------------------------
/** @file SosUctSearch.cpp */
//----------------------------------------------------------------------------
#include <vector>
#include "SosUctSearch.h"
#include "SgBlackWhite.h"
#include "SgUctTree.h"
#include "SgUctValue.h"
#include "SgRandom.h"
#include "assert.h"

SosUctThreadState::SosUctThreadState(unsigned int threadId, const SosGame& game, const SgBlackWhite color, const SosState state)
    : SgUctThreadState(threadId, game.size()),,
      m_game(game),
      m_color(color),
      m_gameState(state)

{
    this->m_isInPlayout = false;
}

SgUctValue SosUctThreadState::Evaluate()
{
	SG_ASSERT(this->m_game.isFinalState(this->m_gameState));
	return static_cast<SgUctValue>(this->m_game.ScoreBonus(this->m_gameState));
}

void SosUctThreadState::Execute(SgMove move)
{
    SG_ASSERT(! this->m_isInPlayout);
    this->m_gameState.play(move);
}

void SosUctThreadState::ExecutePlayout(SgMove move)
{
    SG_ASSERT(this->m_isInPlayout);
    this->Execute(move)
}

bool SosUctThreadState::GenerateAllMoves(SgUctValue count, 
                                  std::vector<SgUctMoveInfo>& moves,
                                  SgUctProvenType& provenType)
{
    moves.clear();

    if (this->m_game.isFinalState(this->m_gameState)){
        if (((this->Evaluate() > this->m_game.komi()) && (this->m_color == SG_WHITE)) 
		|| ((this->Evaluate() < this->m_game.komi()) && (this->m_color == SG_BLACK)))
		provenType = SG_PROVEN_WIN;
	else
		provenType = SG_PROVEN_LOSS;	
	return true;
    }
    else{
	std::vector<SgMove> availableMoves = this->m_gameState.availableMoves();
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
	std::vector<SgMove> availableMoves = this->m_gameState.availableMoves();
	SgRandom randomize =  SgRandom();

	index =  randomize.Int(availableMoves.size());

	skipRaveUpdate = false;
	return availableMoves.at(index);
}

void SosUctThreadState::GameStart()
{
    this->m_isInPlayout = false;
}

void SosUctThreadState::StartPlayout()
{
   
}

void SosUctThreadState::StartPlayouts()
{
    this->m_isInPlayout = true;
}

void SosUctThreadState::StartSearch()
{

}

void SosUctThreadState::TakeBackInTree(std::size_t nuMoves)
{
    this->m_gameState.undo(nuMoves);
}

void SosUctThreadState::TakeBackPlayout(std::size_t nuMoves)
{
    this->m_gameState.undo(nuMoves);
}

//----------------------------------------------------------------------------

SosThreadStateFactory::SosThreadStateFactory(SosGame game, 
					SgBlackWhite color, 
					SosState state)
				: m_game(game),
				  m_color(color), 
				  m_state(state)
{
}

SosThreadStateFactory::~SosThreadStateFactory()
{
}

SgUctThreadState* SosThreadStateFactory:: Create(unsigned int threadId,
                                     		const SgUctSearch& search)
{
	return new SosUctThreadState(this->threadId, this->m_game, 
					this->m_color, this->state);
}

//----------------------------------------------------------------------------

