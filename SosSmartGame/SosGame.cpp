#include "SosGame.h"
#include "SgSystem.h"
/**
	constructor.
	@param size Number of switches.
	*/
	SosState::SosState(int size)
		: m_size(size),
		  m_turn(SG_WHITE)					
	{
		std::vector<MoveColor>::iterator it;
		for (it = m_moves.begin(); it != m_moves.end(); ++it){
			*it = GREY;
		}
	}

	/**
	copy constructor.
	@param state The instance to copy.
	*/
 	SosState::SosState(const SosState& state)
		: m_size(state.m_size),
		  m_turn(state.m_turn),
		  m_moves(state.m_moves),
		  m_played(state.m_played)
	{
	}

	SosState::~SosState()
	{
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
		return (m_turn == SG_WHITE);
	}

	/**
	play a move.
	@param move The move to play.
	*/
	void SosState::play(SgMove move){
		int index = static_cast<int>(move);
		SG_ASSERT(m_moves.at(index) == GREY);
		if (m_turn == SG_WHITE){
			m_moves.at(index) = WHITE;
			m_turn = SG_BLACK;
		}
		else{
			m_moves.at(index) = BLACK;
			m_turn = SG_WHITE;
		}
		m_played.push_back(move);
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
		return m_size;
	}

	void SosState::undo(int n)
	{
		for (int i = 0; i < n; i++)
		{
			SgMove move = m_played.pop_back();
			m_moves.at(static_cast<int>(move)) = GREY;
		}
		if ((n % 2) != 0){
			if  (m_turn == SG_WHITE)
				m_turn = SG_BLACK;
			else
				m_turn = SG_WHITE;
		}
	}

	std::vector<SgMove> SosState::someMoves(MoveColor color){
		std::vector<SgMove> moves;
		for (int index = 0; index <  m_moves.size(); index++){
			if (m_moves.at(index) == color)
				moves.push_back(static_cast<SgMove>(index));
		}	
		return moves;
	}