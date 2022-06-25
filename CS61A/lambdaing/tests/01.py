test = {
  'name': 'Problem 1',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> staff_member = Card('staff', 400, 300)
          >>> staff_member.name
          'staff'
          >>> staff_member.attack
          400
          >>> staff_member.defense
          300
          >>> other_staff = Card('other', 300, 500)
          >>> other_staff.attack
          300
          >>> other_staff.defense
          500
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> staff_member = Card('staff', 400, 300)
          >>> other_staff = Card('other', 300, 500)
          >>> staff_member.power(other_staff)
          -100
          >>> other_staff.power(staff_member)
          0
          >>> third_card = Card('third', 200, 400)
          >>> staff_member.power(third_card)
          0
          >>> third_card.power(staff_member)
          -100
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> test_card = Card('test', 100, 100)
          >>> test_deck = Deck([test_card.copy() for _ in range(6)])
          >>> test_player = Player(test_deck, 'tester')
          >>> len(test_deck.cards)
          1
          >>> len(test_player.hand)
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> test_card = Card('test', 100, 100)
          >>> test_deck = Deck([test_card.copy() for _ in range(6)])
          >>> test_player = Player(test_deck, 'tester')
          >>> test_player.draw()
          >>> len(test_deck.cards)
          0
          >>> len(test_player.hand)
          6
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> from cards import *
          >>> test_player = Player(standard_deck, 'tester')
          >>> ta1, ta2 = TACard("ta_1", 300, 400), TACard("ta_2", 500, 600)
          >>> tutor1, tutor2 = TutorCard("t1", 200, 500), TutorCard("t2", 600, 400)
          >>> test_player.hand = [ta1, ta2, tutor1, tutor2]
          >>> test_player.play(0) is ta1
          True
          >>> test_player.play(2) is tutor2
          True
          >>> len(test_player.hand)
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from classes import *
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
