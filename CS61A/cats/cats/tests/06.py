test = {
  'name': 'Problem 6',
  'points': 3,
  'suites': [
    {
      'cases': [
        {
          'code': r"""
          >>> big_limit = 10
          >>> sphinx_swaps("car", "cad", big_limit)
          52f1b72ba99dddc798bb5cebce0be695
          # locked
          >>> sphinx_swaps("this", "that", big_limit)
          45c27a29bbaeb163dec9a0eaed9c7c9c
          # locked
          >>> sphinx_swaps("one", "two", big_limit)
          91711de69bc1d16e478231c51fac5db8
          # locked
          >>> sphinx_swaps("from", "form", big_limit)
          45c27a29bbaeb163dec9a0eaed9c7c9c
          # locked
          >>> sphinx_swaps("awe", "awesome", big_limit)
          bfdc03a3c261c5dc71255ec79dd5977e
          # locked
          >>> sphinx_swaps("someawe", "awesome", big_limit)
          ca82d3ac444a7724c7a6f8a337e495f5
          # locked
          >>> sphinx_swaps("awful", "awesome", big_limit)
          f29bb7189bc0116caaaf05635899b49b
          # locked
          >>> sphinx_swaps("awful", "awesome", 3) > 3
          f0a7036a7438d73054555da0482ad042
          # locked
          >>> sphinx_swaps("awful", "awesome", 4) > 4
          f0a7036a7438d73054555da0482ad042
          # locked
          >>> sphinx_swaps("awful", "awesome", 5) > 5
          81e16d9126cb46b28abbb0a979cb030a
          # locked
          """,
          'hidden': False,
          'locked': True,
          'multiline': False
        },
        {
          'code': r"""
          >>> big_limit = 10
          >>> sphinx_swaps("nice", "rice", big_limit)    # Substitute: n -> r
          1
          >>> sphinx_swaps("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
          2
          >>> sphinx_swaps("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
          3
          >>> sphinx_swaps("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
          5
          >>> sphinx_swaps("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> big_limit = 10
          >>> sphinx_swaps("goodbye", "good", big_limit)
          3
          >>> sphinx_swaps("pront", "print", big_limit)
          1
          >>> sphinx_swaps("misspollid", "misspelled", big_limit)
          2
          >>> sphinx_swaps("worry", "word", big_limit)
          2
          >>> sphinx_swaps("first", "flashy", big_limit)
          4
          >>> sphinx_swaps("hash", "ash", big_limit)
          4
          >>> sphinx_swaps("ash", "hash", big_limit)
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> small_words_list = ["spell", "nest", "test", "pest", "best", "bird", "wired",
          ...                     "abstraction", "abstract", "peeling", "gestate", "west",
          ...                     "spelling", "bastion"]
          >>> autocorrect("speling", small_words_list, sphinx_swaps, 10)
          'peeling'
          >>> autocorrect("abstrction", small_words_list, sphinx_swaps, 10)
          'abstract'
          >>> autocorrect("wird", small_words_list, sphinx_swaps, 10)
          'bird'
          >>> autocorrect("gest", small_words_list, sphinx_swaps, 10)
          'nest'
          >>> # ban iteration, list comprehensions
          >>> test.check('cats.py', 'sphinx_swaps', ['While', 'For', 'ListComp'])
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> # Check that the recursion stops when the limit is reached
          >>> import trace, io
          >>> from contextlib import redirect_stdout
          >>> with io.StringIO() as buf, redirect_stdout(buf):
          ...     trace.Trace(trace=True).runfunc(sphinx_swaps, "someaweqwertyuio", "awesomeasdfghjkl", 3)
          ...     output = buf.getvalue()
          >>> len([line for line in output.split('\n') if 'funcname' in line]) < 10
          True
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('rut', 'ruhw', 100)
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('yo', 'yo', 100)
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('slurp', 'slurpn', k) > k for k in range(6)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('nice', 'nica', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('owen', 'owen', k) > k for k in range(4)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('donee', 'shush', 100)
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('drest', 'dresm', k) > k for k in range(5)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('cand', 'towy', 100)
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('drawn', 'terry', 100)
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('stour', 'shows', k) > k for k in range(5)])
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('plash', 'cw', k) > k for k in range(5)])
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('cube', 'cube', 100)
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('envy', 'en', k) > k for k in range(4)])
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('panto', 'panto', k) > k for k in range(5)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('herem', 'herem', k) > k for k in range(5)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('zanze', 'culm', k) > k for k in range(5)])
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('kauri', 'kourj', k) > k for k in range(5)])
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('hiver', 'hicer', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('tulip', 'lulipi', k) > k for k in range(6)])
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('aside', 'ataxy', k) > k for k in range(5)])
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('volt', 'vol', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('sleep', 'sleop', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('cet', 'duad', k) > k for k in range(4)])
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('opal', 'oral', k) > k for k in range(4)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('pathy', 'pathy', k) > k for k in range(5)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('drive', 'dritebcx', 100)
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('bater', 'bateri', k) > k for k in range(6)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('ward', 'crier', k) > k for k in range(5)])
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('massy', 'massy', 100)
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('tonk', 'tonhbx', 100)
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('sith', 'demit', 100)
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('arty', 'ar', 100)
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('exist', 'exisp', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('plot', 'plotf', k) > k for k in range(5)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('wreak', 'wreak', k) > k for k in range(5)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('icon', 'ipog', 100)
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('caza', 'scale', 100)
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('rann', 'daw', k) > k for k in range(4)])
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('natal', 'natalj', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('tji', 'tjv', k) > k for k in range(3)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('input', 'input', 100)
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('lysin', 'lzsunl', k) > k for k in range(6)])
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('bed', 'bey', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('topsl', 'topsl', 100)
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('becap', 'becap', k) > k for k in range(5)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('tiny', 'sizes', 100)
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('plots', 'plotss', k) > k for k in range(6)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('plote', 'plot', k) > k for k in range(5)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('libra', 'unact', k) > k for k in range(5)])
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('shed', 'shetg', k) > k for k in range(5)])
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('lunes', 'lunes', k) > k for k in range(5)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('shooi', 'sgcoi', 100)
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('cahow', 'cahow', 100)
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('watch', 'watch', k) > k for k in range(5)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('jeans', 'uefnp', 100)
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('floey', 'uvea', 100)
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('pew', 'pe', k) > k for k in range(3)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('tec', 'teca', k) > k for k in range(4)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('chef', 'drib', k) > k for k in range(4)])
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('sowel', 'evert', k) > k for k in range(5)])
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('zebu', 'zbb', k) > k for k in range(4)])
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('magma', 'magmasm', 100)
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('shood', 'ketal', 100)
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('stall', 'ftall', k) > k for k in range(5)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('towd', 'tow', k) > k for k in range(4)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('doty', 'dsto', k) > k for k in range(4)])
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('prime', 'huso', 100)
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('raspy', 'raeiya', k) > k for k in range(6)])
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('sight', 'szghtw', k) > k for k in range(6)])
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('scho', 'sc', 100)
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('sher', 'sided', 100)
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('glime', 'plane', k) > k for k in range(5)])
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('canon', 'canon', k) > k for k in range(5)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('soon', 'sb', k) > k for k in range(4)])
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('would', 'douldtl', 100)
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('yeat', 'yeat', k) > k for k in range(4)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('lexus', 'lexrs', k) > k for k in range(5)])
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('randy', 'lose', k) > k for k in range(5)])
          5
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('thee', 'theea', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('pilot', 'pilot', 100)
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('irk', 'hokey', 100)
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('foody', 'lough', k) > k for k in range(5)])
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('mensa', 'ken', k) > k for k in range(5)])
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('spung', 'spu', k) > k for k in range(5)])
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('db', 'db', 100)
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('beala', 'beama', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('bepun', 'bepu', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('film', 'fblu', k) > k for k in range(4)])
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('espn', 'esp', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('hondo', 'hbndao', k) > k for k in range(6)])
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('reps', 'gata', 100)
          4
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('tirr', 'tsr', k) > k for k in range(4)])
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('slote', 'svotjg', k) > k for k in range(6)])
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('beeve', 'jegvd', k) > k for k in range(5)])
          3
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('evade', 'evade', k) > k for k in range(5)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('sinew', 'dineb', k) > k for k in range(5)])
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('goods', 'good', 100)
          1
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('kiley', 'kiley', k) > k for k in range(5)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sum([sphinx_swaps('score', 'score', k) > k for k in range(5)])
          0
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        },
        {
          'code': r"""
          >>> sphinx_swaps('flags', 'flaq', 100)
          2
          """,
          'hidden': False,
          'locked': False,
          'multiline': False
        }
      ],
      'scored': True,
      'setup': r"""
      >>> from cats import sphinx_swaps, autocorrect
      >>> import tests.construct_check as test
      """,
      'teardown': '',
      'type': 'doctest'
    }
  ]
}
