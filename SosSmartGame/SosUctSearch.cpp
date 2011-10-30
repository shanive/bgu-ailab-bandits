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
    m_isInPlayout = false;
}

SgUctValue SosUctThreadState::Evaluate()
{
	SG_ASSERT(m_game.endOfGame(m_gameState));
	return static_cast<SgUctValue>(m_game.score(m_gameState));
}

void SosUctThreadState::Execute(SgMove move)
{
    SG_ASSERT(! m_isInPlayout);
    SG_ASSERT(move == SG_PASS);
    m_gameState.play(move);
}

void SosUctThreadState::ExecutePlayout(SgMove move)
{
    SG_ASSERT(m_isInPlayout);
    Execute(move)
}

bool SosUctThreadState::GenerateAllMoves(SgUctValue count, 
                                  std::vector<SgUctMoveInfo>& moves,
                                  SgUctProvenType& provenType)
{
    moves.clear();

    if (m_game.endOfGame(m_gameState)){
        if (((Evaluate() == 1) && (m_color == SG_WHITE)) 
		|| ((Evaluate() == 0) && (m_color == SG_BLACK)))
		provenType = SG_PROVEN_WIN;
	else
		provenType = SG_PROVEN_LOSS;
    }
    else{
	std::vector<SgMove> availableMoves = m_gameState.availableMoves()
	std::vector<SgMove>::const_iterator it;
	
	for (it = availableMoves.begin(); it != availableMoves.end(); ++it){
		moves.push_back(SgUctMoveInfo(*it));
    	}
	provenType = SG_NOT_PROVEN; 
    }
    return false; ///Todo
}  

SgMove SosUctThreadState::GeneratePlayoutMove(bool& skipRaveUpdate)
{
	std::vector<SgMove> availableMoves = m_gameState.availableMoves();
	SgRandom randomize =  SgRandom();

	index =  randomize.Int(availableMoves.size());

	skipRaveUpdate = false;
	return availableMoves.at(index);
}

void SosUctThreadState::GameStart()
{
    m_isInPlayout = false;
}

void SosUctThreadState::StartPlayout()
{
   
}

void SosUctThreadState::StartPlayouts()
{
    m_isInPlayout = true;
}

void SosUctThreadState::StartSearch()
{

}

void SosUctThreadState::TakeBackInTree(std::size_t nuMoves)
{
    m_gameState.undo(nuMoves);
}

void SosUctThreadState::TakeBackPlayout(std::size_t nuMoves)
{
    m_gameState.undo(nuMoves);
}
