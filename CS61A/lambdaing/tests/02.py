test = {
  'name': 'Problem 2',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> test_card = AICard("AI Card", 500, 500)
          >>> initial_deck_length = len(player1.deck.cards)
          >>> initial_hand_size = len(player1.hand)
          >>> test_card.effect(opponent_card, player1, player2)
          AI Card allows me to draw two cards!
          >>> initial_hand_size == len(player1.hand) - 2
          True
          >>> initial_deck_length == len(player1.deck.cards) + 2
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> test_card = TutorCard("Tutor Card", 10000, 10000)
          >>> player1.hand = [Card("card1", 0, 100), Card("card2", 100, 0)]
          >>> test_card.effect(opponent_card, player1, player2)
          Tutor Card allows me to add a copy of a card to my hand!
          >>> print(player1.hand)
          [card1: Staff, [0, 100], card2: Staff, [100, 0], card1: Staff, [0, 100]]
          >>> player1.hand[0] is player1.hand[2] # must add a copy!
          False
          >>> player1.hand = []
          >>> test_card.effect(opponent_card, player1, player2)
          >>> print(player1.hand) # must not add a card if not available
          []
          >>> test_card.power(opponent_card) < opponent_card.power(test_card)
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> test_card = TACard("TA Card", 500, 500)
          >>> player1.hand = []
          >>> test_card.effect(opponent_card, player1, player2) # if no cards in hand, no effect.
          >>> print(test_card.attack, test_card.defense)
          500 500
          >>> player1.hand = [Card("card1", 0, 100), TutorCard("tutor", 10000, 10000), Card("card3", 100, 0)]
          >>> test_card.effect(opponent_card, player1, player2) # must use card's power method.
          TA Card discards card3 from my hand to increase its own power!
          >>> print(player1.hand)
          [card1: Staff, [0, 100], tutor: Tutor, [10000, 10000]]
          >>> print(test_card.attack, test_card.defense)
          600 500
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> test_card = InstructorCard("Instructor Card", 1000, 1000)
          >>> player1.hand = [Card("card1", 0, 100)]
          >>> test_card.effect(opponent_card, player1, player2)
          Instructor Card returns to my hand!
          >>> print(player1.hand) # survives with non-negative attack
          [card1: Staff, [0, 100], Instructor Card: Instructor, [0, 0]]
          >>> player1.hand = [Card("card1", 0, 100)]
          >>> test_card.effect(opponent_card, player1, player2)
          >>> print(player1.hand)
          [card1: Staff, [0, 100]]
          >>> print(test_card.attack, test_card.defense)
          -1000 -1000
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from classes import *
      >>> from cards import *
      >>> player1, player2 = Player(player_deck, 'p1'), Player(opponent_deck, 'p2')
      >>> opponent_card = Card("other", 500, 500)
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
