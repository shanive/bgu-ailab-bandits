/**
@file SosRavePlayer.h
uses smartgame library.
*/

#include "SosPlayer.h"
#include "SosUctSearch.h"
#include "SgMove.h"

class SosGame;
class SosState;

class SosRavePlayer
: public SosPlayer
{
 public:
  /**
     constructor.
     @param game An SOS game.
     @param maxGames Sampels per state.
     @param raveWeightFinal (see article Study Of UCT In Artifitial Games).
  */
  SosRavePlayer(SosGame *game, SgUctValue maxGames, int raveWeightFinal);

  /**
     destructor.
  */
  ~SosRavePlayer();

  /**
     @param state A state of the game.
     @return next move.
  */
  SgMove genMove(SosState *state);

private:
  SosGame *m_game;
  SgUctValue m_maxGames;
  int m_raveWeightFinal;
};

