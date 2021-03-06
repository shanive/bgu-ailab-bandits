//----------------------------------------------------------------------------
/** @file SosGame.h */
//----------------------------------------------------------------------------

#ifndef SOS_GAME_H
#define SOS_GAME_H

#include "SosPlayer.h"
#include <vector>
#include "SgBlackWhite.h"
#include "SgMove.h"
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
     @pre state != 0.
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
     @ set next turn to be of the givven color
  */
  void setTurn(SgBlackWhite toplay);
  /**
     play a move.
     @param move The move to play.
     @pre move is in this->avaiableMoves()
     @post move is not in this->avaiableMoves()
     @post move is in this->whiteMoves() or in this->blackMoves()
     (but not in both)
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
     @pre this->play has been called n times.
     @post this->m_played.size() == @pre this->m_played.size() - n
  */
  void undo(int n);

 private:
  /*number of switches*/
  int m_size;
  /*who's turn is it*/
  SgBlackWhite m_turn;
  /*switches*/
  std::vector<MoveColor> m_moves; 
  /*played moves. FILO*/
  std::vector<SgMove> m_played;
  /*return vector of moves with a givem color*/
  std::vector<SgMove> someMoves(MoveColor color);
	
};


class SosGame
{
 public:

  /** switches' values' order */
  typedef enum
  {
    RANDOM,

    ASCENDING,

    DESCENDING, 

    SEMIRANDOM

  } ValuesOrder;

  /**
     constructor.
  */
  explicit SosGame(int size, bool scoreBonus = false, 
                   ValuesOrder order = SEMIRANDOM, 
                   std::vector<int>* values = 0);

  /**
     copy constructor.
  */
  SosGame(const SosGame& game);

  /**
     destructor.
  */
  ~SosGame();

  /**
     @return true iff a given state is the final state of this game.
  */	
  bool isFinalState(SosState state);

  /**
     simulate a game between two given players.
     @param firstplayer A pointer to SosPlayer instance.
     @param seconfplayer A pointer to SosPlayer instance.
     @return the score of the game.
  */
  double twoPlayersGame(SosPlayer *firstplayer, SosPlayer *secondplayer);

  /**
     @param state A final state of this game.
     @pre isFinalState(state) == true.
     @return The score of this game.(score bonus or win-loss.)
  */ 
  double gameScore(SosState state);
	
  /**
     @param state A state of this game.
     @return score bonuse of a given state.
  */ 
  double scoreBonus(SosState state);
	
  /**
     @param state A state of this game.
     @return 1 if white has won and 0 otherwise.
  */ 
  int winLoss(SosState state);

  /**
     @return the game's komi (winning value)
     see Uct article.
  */
  int komi();

  void setKomi(double komi);

 private:

  double m_komi;

  /* The switches' values between 1 to this->m_gameSize */ 
  std::vector<int> m_switchValues;

  /* True iff count score bonus. */
  bool m_scoreBonus;

  /* Number of switches */
  int m_gameSize;

  /* Initialize switches' values according to order */
  void initValues(ValuesOrder order);

  /* return the initial state of this game */
  SosState initialState();

  /* Return the difference between white's score and black's score */
  int difference(SosState state);

  /* receive move index and return it's value */
  int moveValue(SgMove move);

  /* return the sum of values of moves in moves */
  int valuesSum(std::vector<SgMove> moves);

};













//----------------------------------------------------------------------------

#endif // SOS_GAME_H
