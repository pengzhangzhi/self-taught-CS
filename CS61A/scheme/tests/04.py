test = {
  'name': 'Problem 4',
  'points': 2,
  'suites': [
    {
      'cases': [
        {
          'answer': 'e92e90f58a272e7a74651635251ade14',
          'choices': [
            r"""
            Pair(A, Pair(B, nil)), where:
                A is the symbol being bound,
                B is an expression whose value should be evaluated and bound to A
            """,
            r"""
            Pair(A, Pair(B, nil)), where:
                A is the symbol being bound,
                B is the value that should be bound to A
            """,
            r"""
            Pair(A, B), where:
                A is the symbol being bound,
                B is the value that should be bound to A
            """,
            r"""
            Pair(A, B), where:
                A is the symbol being bound,
                B is an expression whose value should be evaluated and bound to A
            """,
            r"""
            Pair('define', Pair(A, Pair(B, nil))), where:
                A is the symbol being bound,
                B is an expression whose value should be evaluated and bound to A
            """
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': 'What is the structure of the expressions argument to do_define_form?'
        },
        {
          'answer': '0ed53dce7bacc4766422abc478c5c895',
          'choices': [
            'make_child_frame',
            'define',
            'lookup',
            'bindings'
          ],
          'hidden': False,
          'locked': True,
          'multiline': False,
          'question': r"""
          What method of a Frame instance will bind
          a value to a symbol in that frame?
          """
        }
      ],
      'scored': False,
      'type': 'concept'
    },
    {
      'cases': [
        {
          'code': r"""
          scm> (define size 2)
          cc3c061fb8167d02a4ddda1f1c19966e
          # locked
          scm> size
          2b7cdec3904f986982cbd24a0bc12887
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (define x (+ 2 3))
          38ba916dc1f41eb239567ee41a251ecd
          # locked
          scm> x
          b33c0f7206201b4aaeae595493888600
          # locked
          scm> (define x (+ 2 7))
          38ba916dc1f41eb239567ee41a251ecd
          # locked
          scm> x
          27c11fef0d1b8697654b38bb53c550c8
          # locked
          scm> (eval (define tau 6.28)) ; eval takes an expression represented as a list and evaluates it
          aa59dd661f134fa3eab23231a65d789e
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (define pi 3.14159)
          pi
          scm> (define radius 10)
          radius
          scm> (define area (* pi (* radius radius)))
          area
          scm> area
          314.159
          scm> (define radius 100)
          radius
          scm> radius
          100
          scm> area
          314.159
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          scm> (define 0 1)
          SchemeError
          scm> (define error (/ 1 0))
          SchemeError
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          scm> (define x 0)
          x
          scm> ((define x (+ x 1)) 2)
          SchemeError
          scm> x
          1
          scm> (define x 2 y 4)
          SchemeError
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          scm> (define x 15)
          38ba916dc1f41eb239567ee41a251ecd
          # locked
          scm> (define y (* 2 x))
          1a9a3321b8b99a0f9291d89be986e74c
          # locked
          scm> y
          f21c086efebbe30ead8e65c805ec6c78
          # locked
          scm> (+ y (* y 2) 1)
          f8bef99b0acb9318d4bd35fc40f2d4ff
          # locked
          scm> (define x 20)
          38ba916dc1f41eb239567ee41a251ecd
          # locked
          scm> x
          4ce27a311486b293ac49408159fd2437
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (define x 0)
          38ba916dc1f41eb239567ee41a251ecd
          # locked
          scm> ((define x (+ x 1)) 2)
          ec908af60f03727428c7ee3f22ec3cd8
          # locked
          scm> x
          eb892a26497f936d1f6cae54aacc5f51
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': '',
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
