*******************
Modgrammar Tutorial
*******************

Grammar Basics
==============

Creating a Grammar
------------------

The first thing we need to do before we can do any text parsing is to define the grammar (rules) we will be trying to match the text against.  This is usually done by creating a class definition for a new class based on the :class:`Grammar` base class, and then setting its :attr:`~modgrammar.Grammar.grammar` class attribute to describe the details of the actual grammar, so let's start with a simple example::

   from modgrammar import *

   class MyGrammar (Grammar):
       grammar = (LITERAL("Hello,"), LITERAL("world!"))

Some things to note here:  First, the :attr:`~modgrammar.Grammar.grammar` attribute will always contain a list of other grammars.  In this case, we've used two :func:`~modgrammar.LITERAL` grammars to make up our new grammar.  :func:`~modgrammar.LITERAL` is a built-in function provided by the :mod:`modgrammar` module which returns a grammar which will match a specific literal string (in this case, the first one will (only) match the string "Hello,", and the second one will match "world!").  Because our grammar is composed of these two sub-grammars, our grammar will only match a string if it matches both of them, in sequence, so our grammar will only match a piece of text if it contains "Hello, world!".

As a side-note, here, instead of ``LITERAL("Hello,")``, we could also have used its shorter alias, ``L("Hello,")``.  Actually, in most cases where grammars are required, if you just provide a string value, :mod:`modgrammar` will automatically convert it into a :func:`~modgrammar.LITERAL` grammar for you, so we really could have just used plain strings in our grammar definition, with the same results::

   class MyGrammar (Grammar):
       grammar = ("Hello,", "world!")

So we have a grammar defined, and that's all well and good, but how do we actually use it now that we've got it?  Well, next we need to create a :class:`~modgrammar.GrammarParser` object associated with the grammar.  This is done by calling the :meth:`~modgrammar.Grammar.parser` method on our newly defined :class:`MyGrammar` class::

   myparser = MyGrammar.parser()

This parser object can then be used to take pieces of text and attempt to match them against the associated grammar.  Parser objects have several different methods for doing this, depending on whether you're reading from a file, parsing all your text at once, getting it a bit at a time, etc, but for now we'll stick to trying to parse a single string.  To do this, just call the :meth:`~modgrammar.GrammarParser.parse_string` method::

   result = myparser.parse_string("Hello, world!")

Congratulations!  If you're following along in your own window, you have just successfully parsed a piece of text using a custom grammar and now have a parse result object containing all of the relevant information.  Let's take a look::

   >>> result
   MyGrammar<'Hello,', 'world!'>
   >>> result.string
   'Hello, world!'
   >>> result.elements
   (L('Hello,')<'Hello,'>, L('world!')<'world!'>)

As you can see, parse result objects have a couple of useful attributes.  :attr:`~modgrammar.Grammar.string` contains the full text that the grammar matched.  The :attr:`~modgrammar.Grammar.elements` attribute contains result objects for each part of the sub-grammar we defined (typically, there will be one entry in :attr:`~modgrammar.Grammar.elements` for each entry in the :attr:`~modgrammar.Grammar.grammar` attribute of the grammar class).  The :func:`repr` of the object also reflects (in a slightly briefer form) the :attr:`~modgrammar.Grammar.elements` of the match, for descriptive purposes.

As a convenience, it's also possible to access individual sub-elements by just looking up their index on the result object itself (without having to reference the :attr:`~modgrammar.Grammar.elements` attribute directly):

   >>> result[0]
   L('Hello,')<'Hello,'>

The particularly astute might have already noticed something else about these result objects, too::

   >>> isinstance(result, MyGrammar)
   True

That's right, the results we get back from parsing with the :class:`MyGrammar` grammar class are actually instances of that class.  Thus, the class defines the grammar, and each instance of that class is a result of matching that grammar against some text.  This actually turns out to be very powerful, but we'll get into a lot of that later.  One of the most immediate benefits of this, though, is that you can always tell which piece of grammar was matched to produce a particular result just by checking what type of object the result is.

Making Things More Interesting
------------------------------

So far, our grammar works, but it's pretty boring.  It only matches one literal phrase.  Let's start making it a little more interesting, shall we?

First off, let's try giving the speaker a choice::

   class MyGrammar (Grammar):
       grammar = (OR("Hello", "Goodbye"), ",", "world!")

As one might guess, the :func:`~modgrammar.OR` construct above will match either "Hello" or "Goodbye".  We used two literals here, but you can actually use any grammars you want with :func:`~modgrammar.OR` (and as many as you want).  When parsing, it will try each of the sub-grammars in order until it finds one that matches (as long as the rest of the larger grammar matches too, of course).

If you prefer, it's also possible to do :func:`~modgrammar.OR` grammars by just combining two or more sub-grammars together with the or-operator (``|``), like so::

   class MyGrammar (Grammar):
       grammar = (L("Hello") | L("Goodbye"), ",", "world!")

This actually produces exactly the same result as the previous example.  Note that this is one of the few times where you can't just use plain strings to mean literals, because if you tried to do ``"Hello" | "Goodbye"``, the python interpreter wouldn't know that you had intended the two strings to be grammar-literals, so it wouldn't know how to "or" them together::

   >>> "Hello" | "Goodbye"
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: unsupported operand type(s) for |: 'str' and 'str'

As long as you make sure at least one of the operands is a grammar class of some sort, though, it can usually figure it out::

   >>> L("Hello") | "Goodbye"
   <Grammar: (L('Hello') | L('Goodbye'))>
   >>> "Hello" | L("Goodbye")
   <Grammar: (L('Hello') | L('Goodbye'))>

(It's usually just best to make sure all of them are explicitly converted to grammars first, though, as we did above)

Since we're adding choices, let's also add a bit more flexibility in the form of an optional portion of the phrase::

   class MyGrammar (Grammar):
       grammar = (L("Hello") | L("Goodbye"), ",", OPTIONAL("cruel"), "world!")

As you probably figured out already, this will allow us to match both "Goodbye, world!" and "Goodbye, cruel world!" (and, somewhat masochistically, also "Hello, cruel world!", but we won't worry about that now).  What does this look like in our results?
::

   >>> myparser = MyGrammar.parser()
   >>> result = myparser.parse_string("Hello, world!")
   >>> result.elements
   (L('Hello,')<'Hello,'>, L(',')<','>, None, L('world!')<'world!'>)

   >>> result = myparser.parse_string("Goodbye, cruel world!")
   >>> result.elements
   (L('Goodbye')<'Goodbye'>, L(',')<','>, L('cruel')<'cruel'>, L('world!')<'world!'>)

As you can see, :func:`~modgrammar.OPTIONAL` will result in the matching sub-grammar element if there is a match, or if there isn't a match, it will produce :const:`None` in that spot.

Note, also, that we've been using literals for most of the sub-grammars here, but, as with :func:`~modgrammar.OR`, :func:`~modgrammar.OPTIONAL` can actually take any kind of grammar as an argument, so you could, for example, nest these two constructs::

   class MyGrammar (Grammar):
       grammar = (L("Hello") | L("Goodbye"), ",", OPTIONAL(L("cruel") | L("wonderful")), "world!")

...or do even more complicated things.  In fact, by just combining the couple of tools we've used so far in different ways, it's possible to construct a whole world of grammars, and we've just gotten started.

Going Deeper: Nested Grammars
-----------------------------

Our grammar definition is starting to get a bit long, and we're going to want to make it even more complex, so maybe it's time we started splitting it up into sub-grammars.  How do we do that?  Easy, just create some more :class:`~modgrammar.Grammar` classes::

   class OpeningWord (Grammar):
       grammar = (L("Hello") | L("Goodbye"))

   class WorldPhrase (Grammar):
       grammar = (OPTIONAL(L("cruel") | L("wonderful")), "world")

...and then hook them together in the main one::

   class MyGrammar (Grammar):
       grammar = (OpeningWord, ",", WorldPhrase, "!")

There we go.. we now have not just one grammar, but a whole grammar tree (well, ok, a small tree... maybe a bush?).  As you can see, you can use :class:`~modgrammar.Grammar` classes you create in exactly the same way as the stock grammars we were already using.  The one thing to note here, of course, is that you have to define them before you can reference them, which is why the :class:`MyGrammar` class had to be defined last.

So, let's see how it works::

   >>> myparser = MyGrammar.parser()
   >>> result = myparser.parse_string("Hello, world!")
   >>> result.elements
   (OpeningWord<'Hello'>, L(',')<','>, WorldPhrase<None, 'world'>, L('!')<'!'>)

You can see now that, since we've defined some more levels in our grammar, our result objects will have some more levels, too.  The top-level result object has four elements, each corresponding to the four sub-grammars we specified in its :attr:`~modgrammar.Grammar.grammar` attribute (an :class:`OpeningWord` result, the literal comma, a :class:`WorldPhrase` result, and the literal exclamation point).  We can look at the third element (the :class:`WorldPhrase` match) to get more details on that part of things::

   >>> result[2].elements
   (None, L('world')<'world'>)

As we would expect, its elements correspond to the :func:`~modgrammar.OPTIONAL` phrase (which we didn't use, so it's :const:`None`), and the literal "world".

Now that we've got things broken up this way, though, we can start making things more complex while still keeping them reasonably organized.  Let's add some new grammar for a completely different style of greeting::

   class FirstName (Grammar):
       grammar = (WORD("A-Z", "a-z"))

   class LastName (Grammar):
       grammar = (WORD("A-Z", "a-z"))

   class MyNameIs (Grammar):
       grammar = ("my name is", FirstName, OPTIONAL(LastName))

And we'll update our :class:`MyGrammar` to add the new option::

   class MyGrammar (Grammar):
       grammar = (OpeningWord, ",", WorldPhrase | MyNameIs, "!")

There!  Now let's give it a whirl::

   >>> myparser = MyGrammar.parser()
   >>> myparser.parse_string("Hello, wonderful world!")
   MyGrammar<'Hello', ',', 'wonderful world', '!'>

   >>> myparser.parse_string("Hello, my name is Inigo Montoya!")
   MyGrammar<'Hello', ',', 'my name is Inigo Montoya', '!'>

Remember that bit above about identifying results based on their class?  Here's an example of where it comes in handy.  Both of these are valid matches to the grammar, but they're two very different sorts of sentences.  How do we tell what type of sentence we're dealing with?  Well, just look at the type of the third element::

   >>> isinstance(result[2], WorldPhrase)
   False
   >>> isinstance(result[2], MyNameIs)
   True

You may have also noticed we introduced a new construct, too: ``WORD("A-Z", "a-z")``.  This is a very handy one, so you'll probably end up using it frequently.  It basically means 'match a sequence of any characters, where the first one is in the set "A-Z" and all the following ones are in the set "a-z"'.  Obviously, you can use whatever set of characters fits your purposes.  The rules are basically the same as for regular expression character-ranges (``[]`` inside regular expressions), so you could say "ABCabc", or "A-Ca-c", etc.  As with regular expressions, you can also put a "^" at the beginning of the string to mean "anything except the following characters".  (Note: You can also leave out the second argument and it'll default to the same set as the first, so ``WORD("A-Z")`` is the same as ``WORD("A-Z", "A-Z")``)

So what if we wanted to be able to include multiple phrases in the same sentence?  Well, it's also possible to specify that a particular sub-grammar can be repeated, using the :func:`~modgrammar.REPEAT` construct::

   class MyGrammar (Grammar):
       grammar = (OpeningWord, ",", REPEAT(WorldPhrase | MyNameIs), "!")

There, now we can have any number of :class:`WorldPhrase` or :class:`MyNameIs` matches before the final exclamation point::

   >>> myparser = MyGrammar.parser()
   >>> results = myparser.parse_string("Hello, cruel world my name is Inigo Montoya!")
   >>> results.elements
   (OpeningWord<'Hello'>, L(',')<','>, <REPEAT><'cruel world', 'my name is Inigo Montoya'>, L('!')<'!'>)
   >>> results[2].elements
   (WorldPhrase<'cruel', 'world'>, MyNameIs<'my name is', 'Inigo', 'Montoya'>)

As you can see, the third element is now a :func:`~modgrammar.REPEAT` match, which contains a list of the (multiple) phrases it was able to match.  But wait a minute, something's not quite right at the moment.  If we're going to be correct about things, there really should be a comma between the "cruel world" and the "my name is ...".  We could turn the :func:`~modgrammar.REPEAT` into ``REPEAT(WorldPhrase | MyNameIs, ",")``, but then we'd have an awkward trailing comma at the end.  There is, in fact, a better way::

   class MyGrammar (Grammar):
       grammar = (OpeningWord, ",", LIST_OF(WorldPhrase | MyNameIs, sep=","), "!")

Because it's so common, the :func:`~modgrammar.LIST_OF` construct was created specifically to deal with this sort of case.  It's basically like :func:`~modgrammar.REPEAT`, except that you can specify a separator that should come between each repeated occurrence (but not at the beginning or end), so now we can have multiple sentiments in our sentence, but they have to be separated by commas::

   >>> myparser = MyGrammar.parser()
   >>> result = myparser.parse_string("Hello, cruel world, my name is Inigo Montoya!")
   >>> result[2].elements
   (WorldPhrase<'wonderful', 'world'>, L(',')<','>, MyNameIs<'my name is', 'Inigo', 'Montoya'>)

Advanced Tip: The argument to *sep* is usually a literal string, but can in fact be any grammar you want, even complex ones (so, for example, you could specify an :func:`~modgrammar.OR` grammar to allow any of several different possible separators).

One last thing:  Currently our grammar will match a potentially infinite number of repetitions for its second part.  What if we wanted to limit that a bit, say to only allowing one or two repetitions?  The *min* and *max* arguments to :func:`~modgrammar.REPEAT` and :func:`~modgrammar.LIST_OF` can be used to control how many times a match can repeat.  *min* automatically defaults to 1, but we can set *max* to restrict the maximum bounds::

   class MyGrammar (Grammar):
       grammar = (OpeningWord, ",", LIST_OF(WorldPhrase | MyNameIs, sep=",", max=2), "!")

Now it won't let us go too far overboard with our sentences::

   >>> myparser.parse_string("Hello, cruel world!")
   MyGrammar<'Hello', ',', 'cruel world', '!'>
   >>> myparser.parse_string("Hello, cruel world, wonderful world!")
   MyGrammar<'Hello', ',', 'cruel world, wonderful world', '!'>
   >>> myparser.parse_string("Hello, cruel world, wonderful world, cruel world!")
   Traceback (most recent call last):
   ...
   modgrammar.ParseError: [line 1, column 91] Expected '!': found ', cruel world!'

We'll get into :exc:`~modgrammar.ParseError` in more detail later on, but as you can see, it happily accepted one or two of the WorldPhrases, but not three.

(*min* and *max* actually work in all kinds of places (for example, they also work for :func:`~modgrammar.WORD` constructs).  You can also use the *count* parameter instead if you want to set *min* and *max* to the same value.)

Full Circle: References and Recursion
-------------------------------------

There's one last piece of the puzzle that needs to be covered if we're going to be able to create all possible sorts of grammars.  Up to now, we've been defining sub-grammar classes, and then pulling them all together into one larger grammar, but this does have one problem.  Since the sub-grammar classes have to be defined before they can be referenced in other grammars, all of the sub-grammars must come before any of the larger grammars that use them.  This is fine for many applications, but what if you need your grammar to refer to *itself* in some way?

Let's take an example of a (very) basic mathematical-expression grammar::

   class Number (Grammar):
       grammar = (WORD("0-9"))

   class Operator (Grammar):
       grammar = (L("+") | L("-") | L("*") | L("/"))

   class Expression (Grammar):
       grammar = (Number, Operator, Number)

This grammar will handle very basic constructs like "1 + 1" or "45 / 12", but what if we wanted to add parenthetical sub-expressions to it (for example, "1 + (2 * 5)")?  Well, let's create another class to cover that case:

   class ParenExpr (Grammar):
       grammar = ("(", Expression, ")")

And then update Expression so it includes that option:

   class Expression (Grammar):
       grammar = (Number | ParenExpr, Operator, Number | ParenExpr)

But wait a minute..  :class:`ParenExpr` is referenced by :class:`Expression` so it has to come first, but :class:`Expression` is referenced by :class:`ParenExpr`, so it has to come first.  How do we solve this?  This is where the special :func:`~modgrammar.REF` function comes in.   If in our :class:`ParenExpr` definition, instead of referencing :class:`Expression` directly, we instead did the following::

   class ParenExpr (Grammar):
       grammar = ("(", REF("Expression"), ")")

...then we can put :class:`ParenExpr` before :class:`Expression` with no problem.  How does this affect the parse results?  Not at all.  In fact, you can actually use a :func:`~modgrammar.REF` construct anywhere you would normally just reference a grammar directly and it will work exactly the same way, so the above functions exactly the same as if we'd just used :class:`Expression` directly (except without the chicken-and-egg problem).

There is one disadvantage to using :func:`~modgrammar.REF`, though.  Every time the grammar is parsed and it comes to that point, it needs to do a lookup to figure out what sub-grammar to use.  This lookup isn't tremendously expensive, but in most cases it's still something we don't really need to do over and over again.  Once we've actually defined all our grammar classes, it should be possible to just do the lookups and resolve everything once, and then not need to do it again.

And, in fact, this is what the :meth:`~modgrammar.Grammar.grammar_resolve_refs` method of the grammar class is for.  Once we've defined all our grammar classes, we can just call that method on the top-level grammar and it will go through the whole thing and resolve any references it can and replace them with the actual grammar classes they resolve to.  You can see the results before and after running grammar_resolve_refs by looking at the :class:`ParenExpr` class::

   >>> ParenExpr.grammar
   (<Grammar: L('(')>, <Grammar: REF('Expression')>, <Grammar: L(')')>)

   >>> Expression.grammar_resolve_refs()
   >>> ParenExpr.grammar
   (<Grammar: L('(')>, <Grammar[Expression]: ((Number | ParenExpr), Operator, (Number | ParenExpr))>, <Grammar: L(')')>)

And presto, a fully recursive grammar::

   >>> Expression.parser().parse_string("(1*2)+(3*(4/(5-6)))")
   Expression<'(1*2)', '+', '(3*(4/(5-6)))'>

Note that while this grammar can theoretically support an unlimited depth of recursion, from a practical perspective each time the :mod:`modgrammar` engine descends into a sub-grammar it involves an associated method call, so the actual depth is limited by the python interpreter's stack.  (For most python implementations, however, the stack is large enough that this is usually not a large concern.)

Left Recursion
^^^^^^^^^^^^^^

We should also talk for a moment about what is known as "left recursion".  This is a situation where a grammar is defined in such a way that the first component of the grammar is actually a recursive reference to itself.  Let's start with an example of "right recursion"::

   class RightRecursive (Grammar):
       grammar = ("A", OPTIONAL(REF("RightRecursive")))

   RightRecursive.grammar_resolve_refs()

This (recursive) grammar will match any number of literal "A"s, with the first element being an "A", and the second being a recursive :class:`RightRecursive` match, like so::

   >>> result = RightRecursive.parser().parse_string("AAAB")
   >>> result
   RightRecursive<'A', 'AA'>
   >>> result.elements[1]
   RightRecursive<'A', 'A'>
   >>> result.elements[1][1]
   RightRecursive<'A', None>

Now let's look at the same thing, but done in a left-recursive way::

   class LeftRecursive (Grammar):
       grammar = (OPTIONAL(REF("LeftRecursive")), "A")

   LeftRecursive.grammar_resolve_refs()

Now, theoretically, according to the rules of defining grammars, this is a perfectly valid grammar definition: it should match the same thing as :class:`RightRecursive`, but just with the recursive part being the first element of each match and the literal being the second.  The problem, however, is that since the :mod:`modgrammar` parser works in a left-to-right order, the first thing it will try to match is the first sub-grammar, which is a reference to :class:`LeftRecursive`, so it will try to match the first sub-grammar of that, which is a reference to :class:`LeftRecursive`, and so on, and so on.  The end result is that it will recurse infinitely (or really, until it runs out of stack space) before it ever starts actually matching anything at all::

   >>> result = LeftRecursive.parser().parse_string("AAAB")
   Traceback (most recent call last):
   ...
   RuntimeError: maximum recursion depth exceeded in __instancecheck__

There are a couple of different techniques for dealing with left-recursion in the computer science world, but they are non-trivial to implement and at the moment the :mod:`modgrammar` parser does not have any support for this.  The good news is that it is usually possible to rewrite these sorts of constructs in other ways to avoid the problem to begin with.

Customizing General Behaviors
-----------------------------

Whitespace Handling
^^^^^^^^^^^^^^^^^^^

Up to now we've been sorta glossing over one of the default behaviors of these grammars: whitespace handling.  As you may or may not have noticed, up to now all of our grammars have been whitespace-consuming, meaning that they automatically allow any amount of whitespace to come between two tokens, and will skip right over it.  Thus, in our :class:`Expression` grammar above, it would match not only "1+1", but also "1 + 1", or even "1\t+\r1" all equally.  This is convenient for many applications where whitespace really doesn't matter, but what if it should?

Luckily, this behavior is configurable.  If you would prefer that your grammar *not* quietly ignore whitespace, there are a couple of ways to do this:

# If you only want to change this for certain grammar classes, you can set the *grammar_whitespace* attribute of the classes to :const:`False` when you define them.  This is good for one or two classes, but is not really ideal if you want this to be the case for your entire grammar, as not only do you need to set it for every class definition, but you will also need to make sure to explicitly set it (via the *whitespace* parameter) whenever you use :func:`~modgrammar.REPEAT`, :func:`LIST_OF`, :func:`GRAMMAR`, etc, etc.

# You can set ``modgrammar.grammar_whitespace = False``.  This will cause the *grammar_whitespace* attribute on all grammar classes default to :const:`False`.  Note, however, that this will change the behavior of *all* grammars by default, even grammars in other modules which may use the same instance of :mod:`modgrammar`, so this is generally not recommended.

# The best way, usually, is to set ``grammar_whitespace = False`` at the module level of the module in which you're defining your grammar classes.  Whenever you create a grammar class, :mod:`modgrammar` will look for this setting at the module level and use it instead of the global default, if found.

Tip: Even if you do want your grammars to skip whitespace, it's a good idea to set *grammar_whitespace* explicitly at the beginning of your module just to be sure.  This way, if somehow the global ``modgrammar.grammar_whitespace`` gets set to something different than you expect, it won't affect any of your defined grammar classes.

Greed Is Good (But Not Always)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, all the grammars you define will be "greedy".  That means that whenever you use :func:`~modgrammar.REPEAT` or its variants, or things like :func:`~modgrammar.WORD`, they will automatically try to find the longest possible match first.  As an example, consider the following::

   class GreedyGrammar (Grammar):
       grammar = ("A", REPEAT(L("A") | L("B") | L("C")), "C")

This grammar will match an "A", followed by a number of "A"s, "B"s, or "C"s, finally terminated by a "C".  If we try matching a few texts::

   >>> GreedyGrammar.parser().parse_string("ABCD")
   GreedyGrammar<'A', 'B', 'C'>
   >>> GreedyGrammar.parser().parse_string("ABCBCD")
   GreedyGrammar<'A', 'BCB', 'C'>
   >>> GreedyGrammar.parser().parse_string("ABCCCCCCD")
   GreedyGrammar<'A', 'BCCCCC', 'C'>

As you can see, in each case the match it found was the longest one possible.  However, if we want to change this behavior, we can configure this using the *greedy* parameter to :func:`~modgrammar.REPEAT`::

   class NonGreedyGrammar (Grammar):
       grammar = ("A", REPEAT(L("A") | L("B") | L("C"), greedy=False), "C")

   >>> NonGreedyGrammar.parser().parse_string("ABCD")
   NonGreedyGrammar<'A', 'B', 'C'>
   >>> NonGreedyGrammar.parser().parse_string("ABCBCD")
   NonGreedyGrammar<'A', 'B', 'C'>
   >>> NonGreedyGrammar.parser().parse_string("ABCCCCCCD")
   NonGreedyGrammar<'A', 'B', 'C'>

Now the grammar matches the smallest possible match instead.

Note, however, that any match returned must always match the entire grammar, so if, for example, we added a "D" to the end of the grammar, then even a non-greedy grammar would have to match the full strings above, because those would be the only matches which have a final "D"::

   class NonGreedyGrammar (Grammar):
       grammar = ("A", REPEAT(L("A") | L("B") | L("C"), greedy=False), "C", "D")

   >>> NonGreedyGrammar.parser().parse_string("ABCD")
   NonGreedyGrammar<'A', 'B', 'C', 'D'>
   >>> NonGreedyGrammar.parser().parse_string("ABCBCD")
   NonGreedyGrammar<'A', 'BCB', 'C', 'D'>
   >>> NonGreedyGrammar.parser().parse_string("ABCCCCCCD")
   NonGreedyGrammar<'A', 'BCCCCC', 'C', 'D'>

Using the Results
-----------------

So we've pretty thoroughly covered most of the details of actually creating grammars, now it's time to get into the real point of the whole exercise:  results!

As we showed earlier, when you parse some text using a parser, you will (hopefully) get back a result object, and we showed some of the general attributes of result objects, but there's some other nifty tricks that can be done with them as well.

In many applications, for example, you may not actually care about the whole parse tree, but only one particular bit of it.  Let's go back to our modified "hello world" example::

   >>> result = myparser.parse_string("Hello, cruel world, my name is Inigo Montoya!")
   >>> result[2].elements
   (WorldPhrase<'wonderful', 'world'>, L(',')<','>, MyNameIs<'my name is', 'Inigo', 'Montoya'>)

Now let's say in this case all we really care about is finding out the person's first name.  We could traverse the whole tree, pulling out result[2], going through each one, checking to see if it's a MyNameIs, then pulling out the right sub-element of that, etc, but actually we don't have to.  Since we know we're looking for an occurrence of :class:`FirstName`, we can just ask the result object to find it and return it for us using :meth:`~modgrammar.Grammar.find`::

   >>> result.find(FirstName)
   FirstName<'Inigo'>

Tada!  But what if there's more than one, and we want to see all of them?  Well, there's also a :meth:`~modgrammar.Grammar.find_all` method::

   >>> result = myparser.parse_string("Hello, my name is Inigo Montoya, my name is Fezzik!")
   >>> result.find_all(FirstName)
   [FirstName<'Inigo'>, FirstName<'Fezzik'>]

If, however, you had some other part of your grammar that also used :class:`FirstName` but you're only interested in :class:`FirstName`\ s that are part of :class:`MyNameIs` constructs, you can do that too.  The :meth:`~modgrammar.Grammar.find` and :meth:`~modgrammar.Grammar.find_all` methods will actually accept a list of any number of grammar types, which will be followed in order to find the result, so if, for example, you say ``result.find(MyNameIs, FirstName)``, then an element will only match if it's of type :class:`FirstName` which is contained somewhere inside an element of type :class:`MyNameIs`::

   >>> result.find_all(MyNameIs, FirstName)
   [FirstName<'Inigo'>, FirstName<'Fezzik'>]

In some applications, you may just want to break some text down into its components, and don't really care about the whole parse tree.  If this is the case, there's a couple of other handy methods for you::

   >>> result.terminals()
   [L('Hello')<'Hello'>, L(',')<','>, L('my name is')<'my name is'>, WORD('A-Z', 'a-z')<'Inigo'>, WORD('A-Z', 'a-z')<'Montoya'>, L(',')<','>, L('my name is')<'my name is'>, WORD('A-Z', 'a-z')<'Fezzik'>, L('!')<'!'>]
   >>> result.tokens()
   ['Hello', ',', 'my name is', 'Inigo', 'Montoya', ',', 'my name is', 'Fezzik', '!']

The :meth:`~modgrammar.Grammar.terminals` method will return all of the terminal elements (that is, elements that don't have any sub-elements) in the tree.  Typically, this results in all of the individual literal strings, :func:`~modgrammar.WORD`s, etc, without any of the larger tree structures.  Likewise, the :meth:`~modgrammar.Grammar.tokens` method actually just returns all of the actual strings associated with the terminals (thus it returns the original text, broken down into its component parts).

Finally, if just searching by element type isn't precise enough for you, there's one more way to look up individual elements in a parse tree: tags.

When defining any grammar class, you can associate with it one or more "tags".  These are simple strings that can be used to identify or group elements which were generated from that grammar later.  For example, say we want to find any name component (both :class:`FirstName` and :class:`LastName`) of the parsed text.  We could search for each individually and put them together into one list, or we could just create a "name" tag and assign it to both :class:`FirstName` and :class:`LastName`::

   class FirstName (Grammar):
       grammar = (WORD("A-Z", "a-z"))
       grammar_tags = ("name",)

   class LastName (Grammar):
       grammar = (WORD("A-Z", "a-z"))
       grammar_tags = ("name",)

Now if we generate a new result from this grammar, we can actually search for elements with a "name" tag using :meth:`~modgrammar.Grammar.find_tag` and :meth:`~modgrammar.Grammar.find_tag_all`, just the same as we used :meth:`~modgrammar.Grammar.find` and :meth:`~modgrammar.Grammar.find_all` before::

   >>> myparser = MyGrammar.parser()
   >>> result = myparser.parse_string("Hello, my name is Inigo Montoya, my name is Fezzik!")
   >>> result.find_tag("name")
   FirstName<'Inigo'>
   >>> result.find_tag_all("name")
   [FirstName<'Inigo'>, LastName<'Montoya'>, FirstName<'Fezzik'>]

(You can even supply a list of tags to traverse, the same as we did with a list of types for the :meth:`~modgrammar.Grammar.find` methods.)

Results May Vary: Customizing Result Objects
--------------------------------------------

Those with good memories will remember, back when we first introduced result objects, that result objects are actually instances of the grammar classes that produce them, and the comment that this could be very powerful, but we never really got into the details of that statement.  Now we're going to.

The reason this is so powerful, quite simply, is that it means when you define a grammar class, you're not just defining the grammatical pattern of an element, but you're also defining the characteristics of the result object which will be produced.  Specifically, you can define methods and attributes which will be inherited by the result object when it's created.

elem_init
^^^^^^^^^

Now, there are two kinds of methods you can define for this purpose: methods which override standard result object behaviors, and methods which provide entirely new functionality.  In the first category, the one you will most commonly be interested in is :meth:`~modgrammar.Grammar.elem_init`.

:meth:`~modgrammar.Grammar.elem_init` is called by the parsing engine after each result object is created, but before it is returned as part of a parse tree result.  This gives the object an opportunity to set up any custom state it wants before being returned to the caller.  For example, in our previous example, we could do the following::

   class MyNameIs (Grammar):
       grammar = ("my name is", FirstName, OPTIONAL(LastName))

       def elem_init(self, sessiondata):
           self.firstname = self[1].string
           if self[2]:
               self.lastname = self[2].string
           else:
               self.lastname = ""
           self.fullname = " ".join([self.firstname, self.lastname])

Now if we take a look at the MyNameIs element produced from a parse result, it has some new (useful) attributes already set up for us::

   >>> myparser = MyGrammar.parser()
   >>> result = myparser.parse_string("Hello, my name is Inigo Montoya!")
   >>> mynameis = result.find(MyNameIs)
   >>> mynameis.firstname
   'Inigo'
   >>> mynameis.lastname
   'Montoya'
   >>> mynameis.fullname
   'Inigo Montoya'

(Note: You might be inclined to do this sort of thing in :meth:`__init__` instead, but :meth:`~modgrammar.Grammar.elem_init` is preferred for several reasons.  One is that :meth:`__init__` has some specific arguments and expected behavior which the parsing engine relies on, so it is not recommended to override it.  Another is that at the time of :meth:`__init__`, the result object is not completely configured, so you do not have access to some useful aspects, such as the finalized list of sub-elements, session data, or anything that might be set up in sub-elements' :meth:`~modgrammar.Grammar.elem_init` methods.  By the time :meth:`~modgrammar.Grammar.elem_init` is called, you are guaranteed that the object has been fully set up and all of its sub-elements have been fully initialized.)

You might also have noticed the *sessiondata* parameter passed to :meth:`~modgrammar.Grammar.elem_init`.  We didn't take advantage of this earlier, but when you create your parser object, it is also possible to supply some "session data" (in the form of a dictionary of key-value parameters) which will be used when parsing text.  There are a couple of parser features that make use of this, but it's mainly useful because it's also passed to every object's :meth:`~modgrammar.Grammar.elem_init` method, giving you a way to communicate useful information from the creation of the parser all the way down to the initialization of the results.  For example, what if we changed :meth:`MyNameIs.elem_init` slightly, so the last line read::

   self.fullname = " ".join([sessiondata["name_prefix"], self.firstname, self.lastname])

Now, depending on how we create the parser, we can get different results::

   >>> myparser = MyGrammar.parser({"name_prefix": "Mr."})
   >>> result = myparser.parse_string("Hello, my name is Inigo Montoya!")
   >>> result.find(MyNameIs).fullname
   'Mr. Inigo Montoya'

   >>> myparser = MyGrammar.parser({"name_prefix": "The swordfighter"})
   >>> result = myparser.parse_string("Hello, my name is Inigo Montoya!")
   >>> result.find(MyNameIs).fullname
   'The swordfighter Inigo Montoya'

The example here is obviously a bit trivial, but it at least shows some of the potential of such a feature.

Dynamic Tagging
^^^^^^^^^^^^^^^

Another nifty trick that can be performed with :meth:`~modgrammar.Grammar.elem_init` is to combine it with tagging to produce dynamically-assigned element tags.  All you need to do is set a :attr:`grammar_tags` attribute on the result object containing a tuple with the tags you want::

   class MyNameIs (Grammar):
       grammar = ("my name is", FirstName, OPTIONAL(LastName))

       def elem_init(self, sessiondata):
           self.firstname = self[1].string
           if self[2]:
               self.lastname = self[2].string
           else:
               self.lastname = ""
           self.fullname = " ".join([self.firstname, self.lastname])
           if self.lastname:
               self.grammar_tags = ("has_lastname",)

Now any MyNameIs result object which is created will have the "has_lastname" tag if, and only if, it actually has a last name::

   >>> myparser = MyGrammar.parser()
   >>> result = myparser.parse_string("Hello, my name is Inigo Montoya, my name is Fezzik!")
   >>> result.find_all(MyNameIs)
   [MyNameIs<'my name is', 'Inigo', 'Montoya'>, MyNameIs<'my name is', 'Fezzik', None>]
   >>> result.find_tag_all("has_lastname")
   [MyNameIs<'my name is', 'Inigo', 'Montoya'>]

Custom Methods and Behaviors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The other big advantage to being able to create your own methods and attributes for result objects is that you can give them their own custom behaviors.  For example, say we had a list of people's names, and after we parse a line, we wanted to add any names we found to the list.  We could add a new method to the :class:`MyGrammar` class::

   class MyGrammar (Grammar):
       grammar = (OpeningWord, ",", LIST_OF(WorldPhrase | MyNameIs, sep=",", max=2), "!")

       def add_names_to_list(self, list_of_names):
           for elem in self.find_all(MyNameIs):
              list_of_names.append(elem.fullname)

Now all we have to do is take the result object we get, and call that method, and presto::

   >>> names = []
   >>> myparser = MyGrammar.parser()
   >>> result = myparser.parse_string("Hello, my name is Inigo Montoya, my name is Fezzik!")
   >>> result.add_names_to_list(names)
   >>> names
   ['Inigo Montoya', 'Fezzik ']

Obviously, the options for this are limited only by one's imagination.  It could range from something simple, like adding an :meth:`open` method to a grammar which parses filenames, to defining recursive methods to do complex analysis over an entire parse tree.  In fact, for simple programming language grammars, one might even create an :meth:`execute` method that takes the parse results and actually performs the operations they represent, turning a simple grammar definition into its own full-fledged self-interpreter.

Advanced Topics
===============

As Simple As Possible (But No Simpler)
--------------------------------------

Once you've started creating fairly complex grammars, you may come to notice that they tend to accumulate a lot of extra levels that you don't necessarily care about.  For example, in our perennial heavily-modified "hello world" example, every result object we get back is going to have an :class:`OpeningWord` as its first element, which then inside it will have the actual word used, so to get the word we need to do an extra level of indirection (``result[0][0]``)::

   >>> result = myparser.parse_string("Hello, world!")
   >>> result[0]
   OpeningWord<'Hello'>
   >>> result[0][0]
   L('Hello')<'Hello'>

Since the actual OpeningWord element doesn't provide us with any real value, it would be nice if we could just remove it from the parse tree entirely so we only needed to do something like ``result[0]`` to get the value we care about instead.

We can actually do this, using "grammar collapsing".  Any individual grammar definition can be set to "collapse", meaning that in the final parse tree, instead of the grammar object itself, its position will contain its sub-elements instead.  We can set the :class:`OpeningWord` to collapse by setting its :attr:`~modgrammar.Grammar.grammar_collapse` attribute, like so::

   class OpeningWord (Grammar):
       grammar = (L("Hello") | L("Goodbye"))
       grammar_collapse = True

Now, if we take a look at a result object, we'll see that the first element, instead of being an :class:`OpeningWord` object, is now the literal object itself::

   >>> result = myparser.parse_string("Hello, world!")
   >>> result[0]
   L('Hello')<'Hello'>

There are some obvious things to watch out for with this, of course.  We've lost any information that the :class:`OpeningWord` would have given us.  In this case it doesn't matter, because we know it's always going to be an :class:`OpeningWord`, but in cases where it could be one of several different grammars, if they all collapse, there's now no way to tell which grammar it actually was that matched.  Also, obviously, if we had defined custom methods/attributes on :class:`OpeningWord`, those would be completely inaccessible to us now.

One other thing to be careful of:  If you have a grammar which could result in a variable number of sub-elements (for example, a :func:`~modgrammar.REPEAT` grammar, or an :func:`~modgrammar.OR` grammar where the different options have different numbers of sub-elements), then if you set that grammar to collapse, it may not be easy in the result to tell where your collapsed grammar ends and the next element begins.

Oh, one more thing:  Generally, if you have a grammar which contains literals, the collapsing mechanism will automatically leave out the literals from the collapsed result (unless the result *only* contains literals, in which case it will leave them in).  This is done because it usually doesn't hurt anything (because literals will always be the same, you already should know what and where they're going to be, so there's no real need to have them in the collapsed result), and it makes for some useful side-benefits in some cases, but if for some reason this isn't what you want for a particular grammar, then collapsing might not be appropriate for that case.

Advanced Parsing
----------------

Buffering and Partial Matches
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We covered basic use of a parser object earlier, but now it's time to get into some more advanced techniques.  First of all, let's talk a little bit about how parser objects actually work.

In all the examples so far, we've been using our parser to parse single, individual texts which exactly match the full grammar.  Obviously, this works well when it's feasible, but most real-world parsing situations aren't that convenient.  Text to be parsed often consists of multiple instances of a grammar over and over (one per line in a file, for example), and the data can also often come in pieces which don't necessarily line up with the beginning and end of the grammar (for example, if received in packets over a network).  In many cases it may even be very difficult for the calling program to know where the boundaries should be without actually doing the parsing, so we can't always rely on being able to feed the parser exactly what it's looking for.

Luckily, parser objects are designed to take some of the complexity out of this for us.  In addition to nice, neatly split up texts like we've been using, you can actually feed any amount of text, in any number of pieces, into a parser object and it will still do its thing quite happily.  Take the following example::

   >>> myparser.parse_string("Hello, my na")
   >>> myparser.parse_string("me is Inigo Montoya! Hello, my name is Fezzik!")
   MyGrammar<'Hello', ',', 'my name is Inigo Montoya', '!'>
   >>> myparser.parse_string("")
   MyGrammar<'Hello', ',', 'my name is Fezzik', '!'>

In this, you can see a few things.  First, when we first called :meth:`~modgrammar.GrammarParser.parse_string`, we had a good start (the text matched the beginning of our grammar), but it wasn't complete yet, so the parser just took that info and stored it away for later (returning :const:`None` to indicate it needed more text).  The next time, we actually gave it too much text, but that's ok, it finished matching the first instance of the grammar in the text and gave us back the result.  The extra didn't get lost, though, it's still stored in there ready for parsing the next time.  We then called :meth:`~modgrammar.GrammarParser.parse_string` again with an empty string.  This didn't add any more text to the buffer, but that's ok because we already had a complete match in the buffer left over from before, so it was able to parse that and return it to us.

But what if we didn't want to parse the extra text left over in the buffer with this grammar?  What if we wanted to do something else with it instead?  Well, if we put too much in, we can always get it back by checking the remainder::

   >>> myparser.parse_string("Hello, my name is Inigo Montoya! Hello, my name is Fezzik!")
   MyGrammar<'Hello', ',', 'my name is Inigo Montoya', '!'>
   >>> myparser.remainder()
   ' Hello, my name is Fezzik!'

As a side-note, we can also find out how much of the text we actually did consume up to now (as well as what line/column we'd be on, assuming we were reading this from a file or something)::

   >>> myparser.char
   32
   >>> myparser.line
   0
   >>> myparser.col
   32

So our match took up 32 characters of the input text, and left us with some leftover text of ' Hello, my name is Fezzik!' (leaving us on column 32 of the 0th line (as with python indices, line/column numbers here are 0-based)).

If we're going to do something else with the remainder, though, we probably don't want it to stay in the buffer, because then it would get in the way of whatever we wanted to parse next.  The :meth:`~modgrammar.GrammarParser.clear_remainder` method will take care of that for you.  Of course, that still keeps the character/line/column counts where they are.  If you want to reset everything back to its initial state, you can use :meth:`~modgrammar.GrammarParser.reset` instead::

   >>> myparser.clear_remainder()
   >>> myparser.remainder()
   ''
   >>> myparser.char
   32

   >>> myparser.reset()
   >>> myparser.remainder()
   ''
   >>> myparser.char
   0

:meth:`~modgrammar.GrammarParser.parse_string` Options and Other Parsing Methods
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Up to now, we've been using :meth:`~modgrammar.GrammarParser.parse_string` in its most basic way, by simply passing a string of text, but :meth:`~modgrammar.GrammarParser.parse_string` also supports several optional parameters which can affect how it parses the text, as well:

   *reset*
      If this option is set to a true value, the parser will automatically call :meth:`~modgrammar.GrammarParser.reset` before starting to parse the supplied text.

   *multi*
      If set to a true value, then instead of just returning one match at a time, the parser will keep matching as many times as it can before returning, and return them all in a list.  Note that in this case, if it is unable to make any full matches (yet), it will return an empty list instead of :const:`None`.

   *eof*
      This indicates that we have hit the "end of file", and there will not be any more text to process.  (This can really be used any time the calling application knows there isn't any more text coming, regardless of whether the source is actually a file or not.)  This is needed for some grammars where it may not be clear from the grammar whether we've hit the end or not, but the calling application knows this must be the end so the parser should return the best match it's got so far.  If *eof* is set, the parser will never return a :const:`None` result, unless the buffer is completely empty.

   *data*
      You remember the *sessiondata* from before?  Well, we can actually override it for individual parsing calls, too.  If this parameter is provided it's used in place of the *sessiondata* provided when the parser was created.  (Note that if you get a partial-match (:const:`None` result), you should use the *same* data for any successive calls until the match is completed, as changing the data provided in the middle of parsing a grammar can produce some unpredictable results.)

   *matchtype*
      For many grammars, there end up being cases where a piece of text could match multiple different ways.  This parameter lets you change how the parser decides which match is the "best" one to return.  It can be one of several different options:

      "first" (default)
         The parser will return the first successful match the grammar comes up with.  As mentioned before, matches are generally attempted in left-to-right order of the grammar definition, so for any :func:`~modgrammar.OR` clauses this means the leftmost successful match will be used.  (This is also affected by whether the grammars are greedy or not.  If a repetition is greedy, then the longest possible match will be first, otherwise the shortest will be the first one)
      "last"
         The parser will return the last successful match (using the same ordering  as for "first", just taking the last one instead of the first one)
      "longest"
         The parser will return the match which uses up the longest portion of the input text.
      "shortest"
         The parser will return the match which uses up the shortest portion of the input text.
      "all"
         For each match, instead of returning one result object, the parser will return all possible result objects, in a list.  Note that in this case, the parser will consider the match to consume as much of the text as was matched by the longest result, and will also advance the buffer that far.

      (It should be fairly obvious that "first" can be much more efficient than the other options, as the parser can stop after it gets the first match.  For all the other choices, the parser must keep trying until it finds all possible matches before it can decide which one to return.)

   *bol*
      Indicates whether the parser should consider this text to be at the "beginning of a line".  This is usually not needed, and really only affects grammars that use the :const:`~modgrammar.BOL` built-in to match on beginning-of-line.  This defaults to true if we are just starting (i.e. after a :meth:`~modgrammar.GrammarParser.reset`), or if the last bit of text ended with a newline sequence, and false otherwise.  About the only time you will usually need to use this is if you are doing some unusual parsing where end-of-line is indicated by something outside the context of the text itself (even in those cases, it is often more convenient to just "fake it" by inserting newlines into the text before passing it to the parser instead).

(One sometimes useful combination is to call :meth:`~modgrammar.GrammarParser.parse_string` with ``reset=True, eof=True``, which basically eliminates all buffering, and forces the parser to match (or fail to match) each input text on its own merits for each call, regardless of what may come before or after (note that there may still be a remainder after the match, though, which would be discarded on the next call))

In addition to the basic :meth:`~modgrammar.GrammarParser.parse_string`, parser objects also have a couple of other useful methods for parsing common types of inputs.  If you have a list (or really any iterable) of text items to parse, for example, you can use :meth:`~modgrammar.GrammarParser.parse_lines` to iterate through them and return each match::

   >>> text = ["Hello, my na", "me is Inigo Montoya! Hello, my name is Fezzik!"]
   >>> result = myparser.parse_lines(text)
   >>> result
   <generator object parse_lines at 0x737f30>
   >>> list(result)
   [MyGrammar<'Hello', ',', 'my name is Inigo Montoya', '!'>, MyGrammar<'Hello', ',', 'my name is Fezzik', '!'>]

Note that :meth:`~modgrammar.GrammarParser.parse_lines` is a generator method, which means it will only actually perform the parsing as each item is needed, so you can stop early if you've already gotten what you needed without incurring the extra overhead of parsing everything that might come later (It basically functions by calling :meth:`~modgrammar.GrammarParser.parse_string` as many times as necessary for each line in the input).  Note that although the method is called "parse_lines", the input does not necessarily need to be broken up on line boundaries.  Also note that you must still include newline sequences at the end of your lines (if they're important), the routine will not add them for you.

Likewise, if you want to parse input from a file, there is a convenient :meth:`~modgrammar.GrammarParser.parse_file` method::

   >>> f = open("helloworld_input.txt", "w")
   >>> f.write("Hello, my name is Inigo Montoya!")
   32
   >>> f.write("Hello, my name is Fezzik!")
   25
   >>> f.close()

   >>> result = myparser.parse_file("helloworld_input.txt")
   >>> result
   <generator object parse_file at 0x65aa30>
   >>> list(result)
   [MyGrammar<'Hello', ',', 'my name is Inigo Montoya', '!'>, MyGrammar<'Hello', ',', 'my name is Fezzik', '!'>]

(:meth:`~modgrammar.GrammarParser.parse_file` is really just a wrapper method that opens the file, feeds its contents to :meth:`~modgrammar.GrammarParser.parse_lines`, and then closes it.)

Both of these other parsing methods accept all of the same optional parameters that :meth:`~modgrammar.GrammarParser.parse_string` does (except *multi*).  In the case of :meth:`~modgrammar.GrammarParser.parse_file`, the *eof* argument defaults to true, meaning that when the end of the input file is reached, the parser will consider that to be EOF for the grammar (this can be overridden, though, if you don't want this behavior).

Exceptional Insight
-------------------

Up to now, we've mostly been taking it for granted that the text you feed into the parser is going to match the grammar you've defined, but obviously in the real world this often isn't the case.  When this happens, instead of returning a result to you, the parser will raise a :exc:`ParseError` exception instead.

If you don't catch a :exc:`ParseError` when it is raised, it will result in a traceback looking something like the following::

   >>> myparser.parse_string("Something Bogus")
   Traceback (most recent call last):
   ...
   modgrammar.ParseError: [line 1, column 1] Expected 'Goodbye' or 'Hello': Found 'Something Bogus'

Most of the time, of course, you will want to catch these exceptions and take appropriate action for your application.  If you choose to do this, there are some useful attributes of :exc:`ParseError` exception objects which you may want to take advantage of.

As you can see by the default message (which you can obtain by just calling :func:`str` on the exception object), :exc:`ParseError`\ s have a lot of information in them.  They record not only that a problem occurred, but where (line and column) it was encountered in the input, as well as what the parser expected to find, and what it actually found.  All of these pieces of information are available via attributes on the exception object as well:

   :attr:`~modgrammar.ParseError.line`, :attr:`~modgrammar.ParseError.col`, and :attr:`~modgrammar.ParseError.char`
      The line, column, and character of the input where the problem occurred (measured in the same way as the corresponding attributes on :class:`GrammarParser`).  Note that after a parse exception occurs, the parser object's values for these attributes will still reflect the end position of the last successful parse call (i.e. they'll be the same as they were before the failed parse attempt), whereas the :exc:`ParseError` values will reflect the actual location within the failed input where the error occurred.

   :attr:`~modgrammar.ParseError.expected`
      This contains a set of the possible valid grammars which could have matched at the given location (but obviously, none of them did).

   :attr:`~modgrammar.ParseError.buffer` and :attr:`~modgrammar.ParseError.pos`
      These are the parse buffer being used at the time of the error, and the position within that buffer at which the error occurred.

   :attr:`~modgrammar.ParseError.message`
      This contains the text which is included after the line and column when printing this exception (or getting its string value with :func:`str`).

Note that once you get a :exc:`ParseError`, the offending text will still be in the parser's buffer, so you will continue to get :exc:`ParseError`\ s until you use either :meth:`~modgrammar.GrammarParser.clear_remainder` or :meth:`~modgrammar.GrammarParser.reset` to clear the remainder.

Now, the default message of the :exc:`ParseError` exception attempts to give a pretty good description of what it was expecting, (so that an end-user might be able to figure out what they did wrong and correct the input, for example), but what if it's not quite as clear for your particular grammar as you'd like?  For example, generally if it runs into a problem on a particular token, it will say it was expecting that token, but sometimes a more descriptive way of identifying the actual construct it wanted can make things easier to understand.

Luckily, this behavior is customizable.  The :attr:`~modgrammar.Grammar.grammar_desc` attribute of a grammar class is what :exc:`ParseError`\ s use for this purpose, so if you want to you can override this to change what gets printed for a given grammar.  Note, however, that in most cases it won't be your (custom) grammar that fails to match, but rather one of its sub-grammars (such as a :func:`~modgrammar.LITERAL` or :func:`~modgrammar.WORD`) instead, so most of the time you'll actually need to change their :attr:`~modgrammar.Grammar.grammar_desc` attributes, which can be done by passing the *desc* keyword argument when you create them.

Optional Extras
---------------

There is one other neat little feature I wanted to mention.  Once you've created your custom grammar, it is sometimes useful (for documentation, etc) to be able to represent it in a standard, textual form.  The :mod:`modgrammar` module also supplies a function which can be used to take any grammar and produce an EBNF (Extended Backus-Naur Form) text description of it::

   >>> import sys
   >>> from modgrammar import generate_ebnf
   >>> sys.stdout.writelines(generate_ebnf(MyGrammar))
   MyGrammar   = OpeningWord, ',', ( WorldPhrase | MyNameIs ), [( WorldPhrase |
                 MyNameIs )], '!';
   OpeningWord = ( 'Hello' | 'Goodbye' );
   WorldPhrase = [( 'cruel' | 'wonderful' )], 'world';
   MyNameIs    = 'my name is', FirstName, [LastName];
   FirstName   = ? WORD('A-Z', 'a-z') ?;
   LastName    = ? WORD('A-Z', 'a-z') ?;

The :func:`~modgrammar.generate_ebnf` function is a generator function that produces text output lines, suitable for writing to a file, etc.  As you can see, it generates a full EBNF description of the grammar, using the same class names we used when defining it.  It does its best to convert standard constructs (such as optional phrases and repetitions) to the standard form of representing them in EBNF, but as shown in the ``FirstName`` and ``LastName`` cases, there are some constructs that just don't translate very well (it is possible to represent them in standard EBNF, but the results are often really cumbersome and difficult to understand).  For those cases, it will use EBNF "special sequences" to provide a more readable representation by default.

There are a few different options to control exactly how it will represent grammars in EBNF.  We won't get into those in detail here, but for more information, take a look at the documentation for the :func:`~modgrammar.generate_ebnf` function.
