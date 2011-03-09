***********************************************
:mod:`modgrammar` -- The Modular Grammar Engine
***********************************************

.. automodule:: modgrammar

Grammar Classes
===============

.. autoclass:: Grammar()

Class Attributes
----------------

   .. attribute:: Grammar.grammar

      A list of sub-grammars used to make up this grammar.  This attribute almost always needs to be specified when defining a new grammar class, and is the way in which full grammars can be built up from smaller grammar elements.  In order for this grammar to match an input text, it must completely match each of the sub-grammars listed in its :attr:`grammar` attribute, in order.

   .. attribute:: Grammar.grammar_tags

      A list of "tags" to be associated with match result objects produced by this grammar.  These tags can be used with the :meth:`find_tag` and :meth:`find_tag_all` methods to extract specific elements from a parse tree after a successful match.

   .. attribute:: Grammar.grammar_collapse

      If set to :const:`True`, indicates that this grammar element should be "collapsed" when constructing the final parse tree.  Any place in the parse tree where an instance of this grammar would normally occur will instead be replaced by the list of its sub-elements.  This can be used to make result parse trees simpler in cases where a grammar element has been defined for convenience of the grammar definition, but does not provide a lot of useful information in the resulting parse tree.

   .. attribute:: Grammar.grammar_name

      A string used to identify this grammar.  This is used in a variety of places, including :func:`repr`, :func:`str`, :func:`generate_ebnf`, etc.  (Defaults to the name of the grammar class.)

   .. attribute:: Grammar.grammar_desc

      A descriptive string for the grammar to be used in :exc:`ParseError` error messages. (Defaults to the same value as :attr:`grammar_name`.)

   .. attribute:: Grammar.grammar_whitespace

      If set to :const:`True` (the default), this grammar will automatically skip over any whitespace found between its sub-grammars (it will be "whitespace consuming").  If set to :const:`False`, whitespace between elements will not be treated specially.

      Note: In general, you will want to set this universally for your whole grammar.  The best way to do this is to define a ``grammar_whitespace`` module-level variable in the same module as your grammar classes are defined.  If this is present, it will be used as the default for all grammar classes in that module.

   There are also a few less-commonly-used class attributes which may be useful when inspecting grammars, or may be overridden in special cases:

   .. attribute:: Grammar.grammar_terminal

      Determines whether this grammar is considered to be a "terminal" for the purposes of :meth:`terminals`, :meth:`tokens`, and :func:`generate_ebnf`.  By default, any grammar which contains no sub-grammars (an empty :attr:`grammar` attribute) is considered to be a terminal, and any grammar which has sub-grammars is not.

   .. attribute:: Grammar.grammar_greedy

      If set to :const:`True` (default), indicates that in cases where this grammar could match multiple instances of a sub-text (i.e. for grammars that match repetitions), it should attempt to match the longest possible string first.  By contrast, if set to :const:`False`, the grammar will attempt to match the shortest repetition first.

      Note: This attribute does not have any affect on most custom grammars (because most custom grammars are not themselves repetition grammars (instances of :class:`Repetition`)).  If you are looking to change this behavior in your own grammar definitions, you likely want to use the *collapse* parameter of :func:`REPETITON` (and related functions) instead.  Changing this attribute is mainly useful if for some reason you want to make a custom subclass of :class:`Repetition`, or if you are making a custom grammar element (with a custom :meth:`grammar_parse` definition) for which this setting might be significant.

   .. attribute:: Grammar.grammar_collapse_skip

      Specifies that, if an enclosing grammar is set to collapse, and this grammar is in its sub-grammar list, instances of this sub-grammar should also be left out of the resulting parse tree.

      Note: There is usually no reason to set this attribute.  (It is enabled by default for :func:`LITERAL` grammars, as it is often desirable to leave literal matches out when collapsing grammars since they usually provide no information which isn't already known to the grammar designer.)

Overridable Class Methods
-------------------------

   The following methods may be overridden in subclasses to change the default behavior of a grammar class:

   .. automethod:: Grammar.grammar_details
   .. automethod:: Grammar.grammar_ebnf_lhs
   .. automethod:: Grammar.grammar_ebnf_rhs
   .. automethod:: Grammar.grammar_parse
   .. automethod:: Grammar.grammar_equal
   .. automethod:: Grammar.grammar_collapsed_elems

Useful Class Methods
--------------------

   The following methods are intended to be called on grammar classes by the application:

   .. automethod:: Grammar.parser
   .. automethod:: Grammar.grammar_resolve_refs

Result Objects
==============

As match result objects are actually instances of the grammar class which produced the match, it is also possible, when defining a new grammar class, to override or add new instance methods which will affect the behavior of any associated result objects.  Result objects also posess a number of attributes and methods which can be useful when examining parse results.

Overridable Instance Methods
----------------------------

   .. automethod:: Grammar.elem_init

Useful Instance Attributes
--------------------------

   .. attribute:: Grammar.string

      Contains the portion of the text string which this match corresponds to.

   .. attribute:: Grammar.elements

      Contains result objects for each of the sub-grammars that make up this grammar match.  There is typically one entry in :attr:`elements` for each entry in :attr:`grammar` (though there may not be a direct correspondence if things like :attr:`grammar_collapse` are used)

Useful Instance Methods
-----------------------

   .. automethod:: Grammar.get
   .. automethod:: Grammar.get_all
   .. automethod:: Grammar.find
   .. automethod:: Grammar.find_all
   .. automethod:: Grammar.find_tag
   .. automethod:: Grammar.find_tag_all
   .. automethod:: Grammar.terminals
   .. automethod:: Grammar.tokens
 
Parser Objects
==============

.. autoclass:: GrammarParser()

   Methods:

   .. automethod:: GrammarParser.parse_string
   .. automethod:: GrammarParser.parse_lines
   .. automethod:: GrammarParser.parse_file
   .. automethod:: GrammarParser.remainder
   .. automethod:: GrammarParser.clear_remainder
   .. automethod:: GrammarParser.reset

Built-In Grammars
=================

The following basic grammar classes/factories are provided from which more complicated grammars can be constructed.  For those that take arguments, in addition to the arguments listed, there are a number of standard keyword arguments which can also be provided to alter the default behaviors:

* For any grammars which involve repetition, the *min* and *max* parameters can be used to change the minimum and maximum number of repetitions which are allowed.  *count* can also be used to set *min* and *max* to the same value.

* There are also several standard keyword parameters which correspond to the standard class attributes for the Grammar class.  Setting these keyword arguments will have the same effect as if the corresponding class attribute had been specified in a class definition:

   .. table::

      =============== ======================================
      Keyword         Class Attribute
      =============== ======================================
      *collapse*      :attr:`~Grammar.grammar_collapse`
      *collapse_skip* :attr:`~Grammar.grammar_collapse_skip`
      *greedy*        :attr:`~Grammar.grammar_greedy`
      *tags*          :attr:`~Grammar.grammar_tags`
      *whitespace*    :attr:`~Grammar.grammar_whitespace`
      =============== ======================================

.. autofunction:: GRAMMAR
.. function:: G(*subgrammars, **kwargs)

   This is a synonym for :func:`GRAMMAR`

.. autofunction:: LITERAL
.. function:: L(string, **kwargs)

   This is a synonym for :func:`LITERAL`

.. autofunction:: WORD
.. autofunction:: ANY_EXCEPT
.. autofunction:: OR
.. autofunction:: EXCEPT
.. autofunction:: REPEAT
.. autofunction:: OPTIONAL
.. autofunction:: ZERO_OR_MORE
.. autofunction:: ONE_OR_MORE
.. autofunction:: LIST_OF(*grammar, sep=",", **kwargs)

.. data:: ANY

   Match any single character.

.. data:: EMPTY

   Match the empty string.

   Note: In most cases, :const:`None` is also equivalent to :const:`EMPTY`

.. data:: BOL

   Match the beginning of a line.

   This grammar does not actually consume any of the input text, but can be used to ensure that the next token must occur at the beginning of a new line (i.e. either the beginning of the file, or following an :const:`EOL`).

.. data:: EOL

   Match the end of a line.

   This grammar will match most common forms of line-end (newline, carriage-return, carriage-return + newline, or newline + carriage-return).  If you need something more specific, you may just want to use :func:`LITERAL` instead.

.. data:: EOF

   Match the end of the file.

   Note: This grammar will only match if the parse function is called with ``eof=True`` to indicate the end-of-file has been encountered.

.. data:: REST_OF_LINE

   Match everything up to (but not including) the next :const:`EOL`.

.. data:: SPACE

   Match any string of whitespace.

   Note: This may not match as you expect if your grammar is whitespace-consuming (see the :attr:`~Grammar.grammar_whitespace` attribute).

The :mod:`modgrammar.extras` module also contains some additional built-in grammars which can be useful in some contexts.

References
----------

In some cases, it is necessary to refer to a portion of your grammar before it has actually been defined (for example, for recursive grammar definitions).  In this case, the :func:`REF` function can be used to refer to a grammar by name, which will be resolved to an actual grammar later.  (This construct can also be used to define a grammar which includes some "user-defined" sub-grammar, which the calling application can then provide at runtime.)

.. autofunction:: REF

Exceptions
==========

.. autoexception:: ParseError()
.. autoexception:: ReferenceError
.. autoexception:: UnknownReferenceError
.. autoexception:: BadReferenceError
.. autoexception:: InternalError

Miscellaneous
=============

.. autofunction:: generate_ebnf

