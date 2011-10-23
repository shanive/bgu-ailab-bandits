//----------------------------------------------------------------------------
/** @file SosGame.h */
//----------------------------------------------------------------------------

#ifndef SOS_GAME_H
#define SOS_GAME_H

#include <vector>
#include "SgWhiteBlack.h"

/** move's color. */
typedef enum 
{
    /** Available move */
    GREY,
    
    /** move played by white player */
    WHITE,

    /** move played by black player */
    BLACK

} MoveColor;



/**
Simulation of SOS game's state.
*/
class SosState
{
public:
	/**
	constructor.
	@param size Number of switches.
	*/
	SosState(int size);

	/**
	copy constructor.
	@param state The instance to copy.
	*/
 	SosState(const SosState& state);

	/**
	Destructor.
	*/
	~SosState();
	
	/**
	@return vector of available moves.
	*/
	std::vector<SgMove> availableMoves();

	/**
	@return true if it's white's turn.
	*/
	bool isWhiteTurn();

	/**
	play a move.
	@param move The move to play.
	*/
	void play(SgMove move);
	
	/**
	@return vector of moves played by white player.
	*/
	std::vector<SgMove> whiteMoves();

	/**
	@return vector of moves played by black player.
	*/
	std::vector<SgMove> blackMoves();

	/**
	@return number of switches.
	*/
	int size();

	/**
	undo a given number of moves played.
	*/
	void undo(int n);

private:
	/*number of switches*/
	int m_size;
	/*who's turn is it*/
	SgWhiteBlack m_turn;
	/*switches*/
	std::vector<MoveColor> m_moves; 
	/*played moves. FILO*/
	std::vector<SgMove> m_played;
	/*return vector of moves with a givem color*/
	std::vector<SgMove> someMoves(MovesColor color);
	
};


class SosGame
{


};












//----------------------------------------------------------------------------

#endif // SOS_GAME_H