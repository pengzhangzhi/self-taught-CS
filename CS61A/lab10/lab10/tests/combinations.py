test = {
  'name': 'What Would Scheme Display?',
  'points': 1,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          scm> (- 10 4)
          ad06a9a5930cdb4717260a68b2cca9b7
          # locked
          scm> (* 7 6)
          7a95666384f0e660b057d37a58ae72b2
          # locked
          scm> (+ 1 2 3 4)
          e22bdbd25c9aca39ec85b51ce5397f2c
          # locked
          scm> (/ 8 2 2)
          8f01429f05539100445ff1214be81240
          # locked
          scm> (quotient 29 5)
          fc2b3643bc0ad882bd631ec7e0059563
          # locked
          scm> (modulo 29 5)
          77dc3c4c1e581a2dae92fcb6752dc48c
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (= 1 3)                    ; Scheme uses '=' instead of '==' for comparison
          d8822bef940483b302705d6301130605
          # locked
          scm> (< 1 3)
          77a392e3d9610adc8d0a003c4882ee01
          # locked
          scm> (or 1 #t)                  ; or special form short circuits
          5d57f236bfa316cde9f9cd563993dae4
          # locked
          scm> (and #t #f (/ 1 0))
          d8822bef940483b302705d6301130605
          # locked
          scm> (not #t)
          d8822bef940483b302705d6301130605
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (define x 3)
          adfa7f54c8ad7613f4804096e85be4da
          # locked
          scm> x
          154ae95398009673bcf6847be0496a27
          # locked
          scm> (define y (+ x 4))
          612417f3d036b486fb3efc75ae7d405e
          # locked
          scm> y
          a22c93d07c800a43710ed8cc4198ceb2
          # locked
          scm> (define x (lambda (y) (* y 2)))
          adfa7f54c8ad7613f4804096e85be4da
          # locked
          scm> (x y)
          fd1238f16134df959674bfd9b4c00f92
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          scm> (if (not (print 1)) (print 2) (print 3))
          5d57f236bfa316cde9f9cd563993dae4
          154ae95398009673bcf6847be0496a27
          # locked
          scm> (* (if (> 3 2) 1 2) (+ 4 5))
          404c33bca0bbf0acccef6aa3a7fc218c
          # locked
          scm> (define foo (lambda (x y z) (if x y z)))
          c25528d439305d00a95afbbc086171b9
          # locked
          scm> (foo 1 2 (print 'hi))
          27c7050e9eff8f024f5da76ffe485f71
          8f01429f05539100445ff1214be81240
          # locked
          scm> ((lambda (a) (print 'a)) 100)
          e4518cbebdc0d1652a389becf2daf11b
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      
      """,
      'teardown': '',
      'type': 'scheme'
    }
  ]
}
