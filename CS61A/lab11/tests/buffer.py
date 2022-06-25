test = {
  'name': 'buffer',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> buf = Buffer(iter([['(', '+'], [15], [], [12, ')']]))
          >>> buf.end_of_line()   # False since we have not reached the end of a line
          False
          >>> buf.current
          '('
          >>> buf.pop_first()
          '('
          >>> buf.current
          '+'
          >>> buf.pop_first()
          '+'
          >>> buf.end_of_line()   # We have reached the end of a line
          True
          >>> buf.current
          This is a token representing the end of a line.
          >>> buf.pop_first()
          This is a token representing the end of a line.
          >>> buf.current # Move onto the next line
          15
          >>> buf.pop_first()
          15
          >>> buf.current
          This is a token representing the end of a line.
          >>> buf.pop_first()
          This is a token representing the end of a line.
          >>> buf.current # This should be EOL_TOKEN, since this line is empty
          This is a token representing the end of a line.
          >>> buf.end_of_line()
          True
          >>> buf.pop_first()
          This is a token representing the end of a line.
          >>> buf.current
          12
          >>> buf.pop_first()
          12
          >>> buf.current
          ')'
          >>> buf.pop_first()
          ')'
          >>> buf.current
          This is a token representing the end of a line.
          >>> buf.pop_first()
          This is a token representing the end of a line.
          >>> buf.current         # returns None
          >>> buf.pop_first()     # returns None
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from buffer import *
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
