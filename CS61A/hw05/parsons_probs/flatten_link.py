def flatten_link(lnk):
    """Takes a linked list and returns a flattened Python list with the same elements.

    >>> link = Link(1, Link(2, Link(3, Link(4))))
    >>> flatten_link(link)
    [1, 2, 3, 4]
    >>> flatten_link(Link.empty)
    []
    >>> deep_link = Link(Link(1, Link(2, Link(3, Link(4)))), Link(Link(5), Link(6)))
    >>> flatten_link(deep_link)
    [1, 2, 3, 4, 5, 6]
    """
    "*** YOUR CODE HERE ***"
    """

    base cases:
    if list is not a Link, return [list]
    if list is link and empty, return []
    if list is link and list.rest is empty, return [list.first]
    
    relation: 
        flatten(list) = flatten(list.first) + flatten(rest)
    """
    if lnk is Link.empty:
        return []
    if not isinstance(lnk, Link):
        return [lnk]
    
    if lnk.rest is Link.empty:
        if lnk.first is Link.empty:
            return []
        return [lnk.first]
    return flatten_link(lnk.first) + flatten_link(lnk.rest)

class Link:
    empty = ()

    def __init__(self, first, rest=empty):
        assert rest is Link.empty or isinstance(rest, Link)
        self.first = first
        self.rest = rest

    def __repr__(self):
        if self.rest is not Link.empty:
            rest_repr = ', ' + repr(self.rest)
        else:
            rest_repr = ''
        return 'Link(' + repr(self.first) + rest_repr + ')'

    def __str__(self):
        string = '<'
        while self.rest is not Link.empty:
            string += str(self.first) + ' '
            self = self.rest
        return string + str(self.first) + '>'


flatten_link(Link.empty)