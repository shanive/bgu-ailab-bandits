
//----------------------------------------------------------------------------
/** @file SosUctSearch.h
    Class SosUctSearch and helper classes. */
//----------------------------------------------------------------------------

#ifndef SOS_UCTSEARCH_H
#define SOS_UCTSEARCH_H

#include "SgUctSearch.h"
#include "SosGame.h"
#include "SgBlackWhite.h"
#include <string>
#include <vector>

using namespace std;

class SosUctThreadState
	: public SgUctThreadState
{
public:
   
    /** Constructor.
	@param threadId The number of the thread. Needed for passing to
	constructor of SgUctThreadState.
	@param game An SOS game.
	@param color The color of the corrent player.
	@param state The current state of game.
    */
    SosUctThreadState(unsigned int threadId, SgBlackWhite color, SosGame* game, SosState *state);

    virtual ~SosUctThreadState();

    /** @name Pure virtual functions of SgUctThreadState*/
    // @{

    /** Evaluate end-of-game position.
        Will only be called if GenerateAllMoves() or GeneratePlayoutMove()
        returns no moves. Should return larger values if position is better
        for the player to move. 
	@pre this.game.isFinalState(this.state)
    */
    SgUctValue Evaluate();

    /** Execute a move.
        @param move The move
	@pre move in this->state.availableMoves()
	@post moves isn't in this->state.availableMoves()
    */
    void Execute(SgMove move);

    /** Execute a move in the playout phase.
        For optimization if the subclass uses uses a different game state
        representation in the playout phase. Otherwise the function can be
        implemented in the subclass by simply calling Execute().
        @param move The move 
	@pre move in this->state.availableMoves()
	@post moves isn't in this->state.availableMoves()
    */
    void ExecutePlayout(SgMove move);

    /** Generate moves.
        Moves will be explored in the order of the returned list.
        If return is true, trees under children will be deleted.
        @param count Number of times node has been visited. For knowledge-
        based computations.
        @param[out] moves The generated moves or empty list at end of game
        @param[out] provenType */
    bool GenerateAllMoves(SgUctValue count, 
                                  std::vector<SgUctMoveInfo>& moves,
                                  SgUctProvenType& provenType);

    /** Generate random move.
        Generate a random move in the play-out phase (outside the UCT tree).
        @param[out] skipRaveUpdate This value should be set to true, if the
        move should be excluded from RAVE updates. Otherwise it can be
        ignored.
        @return The move or SG_NULLMOVE at the end of the game. */
    virtual SgMove GeneratePlayoutMove(bool& skipRaveUpdate);

    /** Start search.
        This function should do any necessary preparations for playing games
        in the thread, like initializing the thread's copy of the game state
        from the global game state. The function does not have to be
        thread-safe. */
    virtual void StartSearch();

    /** Take back moves played in the in-tree phase. 
	@pre already played nuMoves moves.
	@post game played moves = @pre game played moves - nuMoves */
    virtual void TakeBackInTree(std::size_t nuMoves);

    /** Take back moves played in the playout phase.
        The search engine does not assume that the moves are really taken back
        after this function is called. If the subclass implements the playout
        in s separate state, which is initialized in StartPlayout() and does
        not support undo, the implementation of this function can be left
        empty in the subclass.
	@pre already played nuMoves moves.
	@post game played moves = @pre game played moves - nuMoves */
    virtual void TakeBackPlayout(std::size_t nuMoves);

    // @} // name

// 
//     /** @name Virtual functions */
//     // @{
// 
    /** Function that will be called by PlayGame() before the game.
        Default implementation does nothing. */
    virtual void GameStart();
// 
    /** Function that will be called at the beginning of the playout phase.
        Will be called only once (not once per playout!). Can be used for
        example to save some state of the current position for more efficient
        implementation of TakeBackPlayout().
        Default implementation does nothing. */
    virtual void StartPlayouts();
// 
//     /** Function that will be called at the beginning of each playout.
//         Default implementation does nothing. */
//     virtual void StartPlayout();
// 
//     /** Function that will be called after each playout.
//         Default implementation does nothing. */
//     virtual void EndPlayout();
// */
private:
	
	bool m_isInPlayout;

	SosGame *m_game;
	/*the color of the current player*/ 
	SgBlackWhite m_color;

	SosState *m_gameState;

    // @} // name
};


//----------------------------------------------------------------------------

class SgUctSearch;

/** Create game specific thread state.
    @see SgUctThreadState
    @ingroup sguctgroup */
class SosUctThreadStateFactory: public SgUctThreadStateFactory
{
public:
    /**
    constructor.
    @param game An Sos game.
    @param color The color of the player.
    @param state An SOS game state.
    */
    SosUctThreadStateFactory(SosGame *game, SgBlackWhite color, 
				SosState *state);

    /**
    destructor.
    */
    ~SosUctThreadStateFactory();

    /**
    create an SosUctThreadState instance.
    @param threadId see SosUctThreadState()
    @param search see SosUctThreadState()
    @return The new created instance.
    */
    SgUctThreadState* Create(unsigned int threadId,
                                     const SgUctSearch& search);

private:

    SosGame* m_game;

    SosState* m_state;

    SgBlackWhite m_color;

};

//----------------------------------------------------------------------------

class SosUctSearch : public SgUctSearch
{
 public:
  /**
     constructor.
     @param threadStateFactory Specific Thread State Creator.
     @param moveRange move range of Sos Game.
     @param provenWinRate The lower bound value of a proven win path in the 
     search tree. If A certain final state's value grater than 
     provenWinRate, then all the nodes in the path lead to it are set to 
     provenWin. Added to SgUctSearch by David & Vered in order to continue 
     the search until reaching maxGames.
     @param provenLossRate The upper bound value of a proven loss path in 
     the search tree. If A certain final state's value lower than 
     provenLossRate, then all the nodes in the path lead to it are set to 
     provenLoss. Added to SgUctSearch by David & Vered in order to continue 
     the search until reaching maxGames.
  */
  SosUctSearch(SosUctThreadStateFactory *threadStateFactory, int moveRange,
               SgUctValue provenWinRate = static_cast<SgUctValue>(1), 
               SgUctValue provenLossRate = static_cast<SgUctValue>(0));

  /**
     destructor.
  */
  virtual ~SosUctSearch();

  /** @SgUctSearch Pure Virtual functions */
  
  /**
     Convert move to string.
     needs To be thread State.
  */
  std::string MoveString(SgMove move) const;

  /**
     Evaluate value to use if evaluation is unknown.
     Will be used if games are aborted because they exceed
     the maximum game length.
     Needs to be thread safe.
  */
  SgUctValue UnknownEval() const;
  
};

#endif // SOS_UCTSEARCH_H

