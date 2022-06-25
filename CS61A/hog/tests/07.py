test = {
  'name': 'Question 7',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> f0 = announce_highest(1) # Only announce Player 1 score gains
          >>> f1 = f0(11, 0)
          >>> f2 = f1(11, 1)
          1 point! That's the biggest gain yet for Player 1
          >>> f3 = f2(20, 1)
          >>> f4 = f3(5, 20) # Player 1 gets 4 points, then Swine Swap applies
          19 points! That's the biggest gain yet for Player 1
          >>> f5 = f4(20, 40) # Player 0 gets 35 points, then Swine Swap applies
          20 points! That's the biggest gain yet for Player 1
          >>> f6 = f5(20, 55) # Player 1 gets 15 points; not enough for a new high
          >>> f7 = f6(21, 55)
          >>> f8 = f7(21, 75)
          >>> f9 = f8(75, 25) # Swap!
          >>> f10 = f9(50, 75) # Swap!
          50 points! That's the biggest gain yet for Player 1
          >>> # The following function call checks if the behavior of f1 changes,
          >>> # perhaps due to a side effect other than printing. The only side
          >>> # effect of a commentary function should be to print.
          >>> f2_again = f1(11, 1)
          1 point! That's the biggest gain yet for Player 1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> #
          >>> announce_both = both(announce_highest(0), announce_highest(1))
          >>> s0, s1 = play(always_roll(0), always_roll(0), goal=10, say=announce_both)
          2 points! That's the biggest gain yet for Player 0
          2 points! That's the biggest gain yet for Player 1
          6 points! That's the biggest gain yet for Player 1
          10 points! That's the biggest gain yet for Player 0
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from hog import play, always_roll, announce_highest, both
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
