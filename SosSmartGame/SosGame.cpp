#include "SosGame.h"
#include <numeric> // for accumulate
#include <assert.h>
#include <algorithm> // for shuffle
/**
	constructor.
	@param size Number of switches.
	*/
	SosState::SosState(int size)
		: m_size(size),
		  m_turn(SG_WHITE),
		  m_moves(size, GREY)					
	{
	
	}

	/**
	copy constructor.
	@param state The instance to copy.
	*/
 	SosState::SosState(const SosState& state)
	{
		this->m_size = state.m_size;
		this->m_turn = state.m_turn;
		this->m_moves = state.m_moves;
		this->m_played = state.m_played;
	}

	SosState::~SosState()
	{
		this->m_moves.clear();
	}

	/**
	@return vector of available moves.
	*/
	std::vector<SgMove> SosState::availableMoves()
	{
		return someMoves(GREY);
	}

	/**
	@return true if it's white's turn.
	*/
	bool SosState::isWhiteTurn()
	{
		return (this->m_turn == SG_WHITE);
	}

	/**
	play a move.
	@param move The move to play.
	*/
	void SosState::play(SgMove move){
		int index = static_cast<int>(move);
		assert(this->m_moves.at(index) == GREY);
		if (this->m_turn == SG_WHITE){
			this->m_moves.at(index) = WHITE;
			this->m_turn = SG_BLACK;
		}
		else{
			this->m_moves.at(index) = BLACK;
			this->m_turn = SG_WHITE;
		}
		this->m_played.push_back(move);
		assert(this->m_moves.at(index) == WHITE || 
			this->m_moves.at(index) == BLACK);
	}	
				
	
	/**
	@return vector of moves played by white player.
	*/
	std::vector<SgMove> SosState::whiteMoves()
	{
		return someMoves(WHITE);
	} 	

	/**
	@return vector of moves played by black player.
	*/
	std::vector<SgMove> SosState::blackMoves()
	{
		return someMoves(BLACK);
	}

	/**
	@return number of switches.
	*/
	int SosState::size(){
		return this->m_size;
	}

	int SosGame::komi()
	{
		return (this.m_size / 2);
	}

	void SosState::undo(int n)
	{
		int nuPlayed = this->m_played.size();
		assert(nuPlayed >= n);
		for (int i = 0; i < n; i++)
		{
			SgMove move = this->m_played.back();
			this->m_played.pop_back();
			this->m_moves.at(static_cast<int>(move)) = GREY;
		}
		if ((n % 2) != 0){
			if  (this->m_turn == SG_WHITE)
				this->m_turn = SG_BLACK;
			else
				this->m_turn = SG_WHITE;
		}
		assert(this->m_played.size() == nuPlayed - n);
	}

	std::vector<SgMove> SosState::someMoves(MoveColor color){
		std::vector<SgMove> moves;
		for (int index = 0; index <  this->m_moves.size(); index++){
			if (this->m_moves.at(index) == color)
				moves.push_back(static_cast<SgMove>(index));
		}	
		return moves;
	}
 

	SosGame::SosGame(int size, bool scoreBonus /*= false */, 
		ValuesOrder order /*= RANDOM */,
		std::vector<int>* values /*= 0 */)
		: m_gameSize(size),
		  m_scoreBonus(scoreBonus)
	{
		if (values)
			this->m_switchValues = (*values); //copy
		else
			this->initValues(order);
	}

	SosGame::SosGame(const SosGame& game)
		: m_switchValues(game.m_switchValues),
		  m_scoreBonus(game.m_scoreBonus),
		  m_gameSize(game.m_gameSize)
	{
	}

	SosGame::~SosGame()
	{
		this->m_switchValues.clear();
	}

	bool SosGame::isFinalState(SosState state)
	{
		return (state.availableMoves().empty());
	}

	double SosGame::twoPlayersGame(SosPlayer *firstplayer, 
					SosPlayer *secondplayer)
	{
		SgMove move;
		SosState state = this->initialState();
		for(int round = 0; round < (this->m_gameSize / 2); round++)
		{
			move =  firstplayer->genMove(&state);
			state.play(move);
			move = secondplayer->genMove(&state);
			state.play(move);
		}
		return this->gameScore(state);
	}
			

	double SosGame::gameScore(SosState state)
	{
		assert(this->isFinalState(state));
		if (this->m_scoreBonus)
			return this->scoreBonus(state);
		else
			return this->winLoss(state);
	}

	double SosGame::scoreBonus(SosState state)
	{
		return this->difference(state);
	}

	int SosGame::winLoss(SosState state)
	{
		int diff = this->difference(state);
		if (diff > 0)
			return 1;
		else
			return 0;
	}

//SosGame private methods:

	void SosGame::initValues(ValuesOrder order)
	{
		for (int i = 0; i < this->m_gameSize; i++)
		{
			this->m_switchValues.push_back(i);
		}
		
		if (order == ASCENDING)
			return;
		else if (order == DESCENDING){
			reverse(this->m_switchValues.begin(), 
					this->m_switchValues.end());
		}
		else //order == RANDOM
			std::random_shuffle(this->m_switchValues.begin(), 
					this->m_switchValues.end());
	}	

	SosState SosGame::initialState()
	{
		return SosState(this->m_gameSize);
	}	

	int SosGame::moveValue(SgMove move)
	{
		return this->m_switchValues.at(static_cast<int>(move));
	}

	int SosGame::valuesSum(std::vector<SgMove> moves)
	{
		int sum = 0;
		std::vector<SgMove>::iterator it;
		for( it = moves.begin(); it != moves.end(); it++)
		{
			sum += this->moveValue(*it);
		}
		return sum;
	}
		

	int SosGame::difference(SosState state)
	{
		std::vector<SgMove> whites = state.whiteMoves();
		std::vector<SgMove> blacks = state.blackMoves();
		int whiteSum = this->valuesSum(whites);
		int blackSum = this->valuesSum(blacks);
		return whiteSum - blackSum;
	}

	
