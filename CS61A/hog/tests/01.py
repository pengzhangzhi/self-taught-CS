test = {
  'name': 'Question 1',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> roll_dice(2, make_test_dice(4, 6, 1))
          70e71b420a966665c548a3bb2cb30d7d
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> roll_dice(3, make_test_dice(4, 6, 1))
          43d176e102c8d95338faf8791aa509b3
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> roll_dice(4, make_test_dice(2, 2, 3))
          872dbe4a4fe5d8451aa842c21194c866
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> roll_dice(4, make_test_dice(1, 2, 3))
          43d176e102c8d95338faf8791aa509b3
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> counted_dice = make_test_dice(4, 1, 2, 6)
          >>> roll_dice(3, counted_dice)
          43d176e102c8d95338faf8791aa509b3
          # locked
          >>> roll_dice(1, counted_dice)  # Make sure you call dice exactly num_rolls times!
          327b19ffebddf93982e1ad2a4a6486f4
          # locked
          """,
          'hidden': False,
          'locked': True
        },
        {
          'code': r"""
          >>> roll_dice(9, make_test_dice(6))
          72862184559d57299206f055e2cc5a63
          # locked
          >>> roll_dice(7, make_test_dice(2, 2, 2, 2, 2, 2, 1))
          43d176e102c8d95338faf8791aa509b3
          # locked
          """,
          'hidden': False,
          'locked': True
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from hog import *
      """,
      'teardown': '',
      'type': 'doctest'
    },
    {
      'cases': [
        {
          'code': r"""
          >>> roll_dice(5, make_test_dice(4, 2, 3, 3, 4, 1))
          16
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> roll_dice(2, make_test_dice(1))
          1
          """,
          'hidden': False,
          'locked': False
        },
        {
          'code': r"""
          >>> dice = make_test_dice(5, 4, 3, 2, 1)
          >>> roll_dice(1, dice)    # Roll 1 (5)
          5
          >>> roll_dice(4, dice)    # Reset (4, 3, 2, 1)
          1
          >>> roll_dice(2, dice)    # Roll 2 (5, 4)
          9
          >>> roll_dice(3, dice)    # Reset (3, 2, 1)
          1
          >>> roll_dice(3, dice)    # Roll 3 (5, 4, 3)
          12
          >>> roll_dice(2, dice)    # Reset (2, 1)
          1
          >>> roll_dice(4, dice)    # Roll 4 (5, 4, 3, 2)
          14
          >>> roll_dice(1, dice)    # Reset (1)
          1
          >>> roll_dice(5, dice)    # Roll 5 (5, 4, 3, 2, 1)
          1
          >>> roll_dice(10, dice)    # Roll 10 (5, 4, 3, 2, 1, 5, 4, 3, 2, 1)
          1
          """,
          'hidden': False,
          'locked': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from hog import *
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
