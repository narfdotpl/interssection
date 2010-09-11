`DRAFT`


interssection
=============

Python lib that lets you treat Atom and RSS feeds like sets.

interssection provides `Feed` class that reads feeds from string (either
URL or XML) and supports all [frozenset methods][methods] apart from
`copy()` and `__contains__(elem)`.  You can change id and title of
created feed and print/save it as Atom 1.0 XML (at the moment it's the
only supported output format).

  [methods]: http://docs.python.org/library/stdtypes.html#frozenset


Usage
-----

### In Ideal World

    from interssection import Feed

    python = Feed('???/tags/python')
    django = Feed('???/tags/django')
    job = Feed('???/tags/job')

    feed = (python | django) & job
    feed.title = 'Python and Django jobs'
    print feed


### In Real World

    #!/usr/bin/env python
    # encoding: utf-8
    """
    Create Atom 1.0 feed containing Stack Overflow questions
    tagged with "Python" but not tagged with "Django" and save
    it to ~/Sites/nondjango.xml so that it can be accessed at
    http://localhost/nondjango.xml on your shiny Mac.
    """

    import codecs
    from os.path import expanduser

    from interssection import Feed


    def _main():
        # get source feeds
        python = Feed('http://stackoverflow.com/feeds/tag/python')
        django = Feed('http://stackoverflow.com/feeds/tag/django')

        # create smart feed
        feed = python - django
        feed.title = 'Non-Django Python Questions'

        # set unique identifier (if you're going to run this script more than
        # once, you may want the resultant feed to have the same id; you can
        # generate one with `import uuid; print uuid.uuid4().urn`)
        feed.id = 'urn:uuid:7cb27103-10fa-49ed-ad91-83583bb3b16a'

        # save xml
        xml = unicode(feed)
        filepath = expanduser('~/Sites/nondjango.xml')
        with codecs.open(filepath, encoding='utf-8', mode='w') as f:
            f.write(xml)

    if __name__ == '__main__':
        _main()


Installation
------------

    [[ ! -x "`which pip`" ]] && easy_install pip
    pip install interssection

Python 2.7 and either pip or easy_install are required.


Meta
----

interssection is written by [Maciej Konieczny][].  This software is
released into the [public domain][] and uses [semantic versioning][] for
release numbering.

  [Maciej Konieczny]: http://narf.pl/
  [public domain]: http://unlicense.org/
  [semantic versioning]: http://semver.org/
