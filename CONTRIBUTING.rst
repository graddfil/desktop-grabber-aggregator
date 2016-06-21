Contributing
------------

Basic workflow
==============

.. code:: sh

        git clone $project
        cd $project

        # create and activate a development environment
        tox -e devenv
        source devenv/bin/activate

        # install pre-commit hooks
        pre-commit install

        # switch to feature branch
        git checkout -b dev-$feat

        # make some changes
        $EDITOR $filename.py

        # make sure you didn't break anything
        tox

        git add $filename.py
        # pre-commit hooks with linters and formatters will be run
        git commit
