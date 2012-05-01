Media Downloader
================

Movies, Series, Music, Subtitles [#]_ , etc [#]_ downloader ... 

The main idea is to group two projects that I currently have, a rss bit
transmission feeder and a subtitle downloader, and also to allow the inclusion
of new sources and destinations.

A source is any service, library or application that could return a link to a
downloadable media file.

A destination is any application, library or service that will actually download
the media file.

Development
+++++++++++

There is a script to create the development environment, it optionally receives
the environment directory path.

::

    $ ./create_env.sh dev_env

This will create the environment directory, add it to *.gitignore* file and create
a environment starter script (yeah, me so lazy)

If you want to install the requirements packages with other procedure, the list
is in *doc/requirements.txt*.

Installations from vcs repos must use -e flag with the urls and #egg=PACKAGE

Runing the Application
++++++++++++++++++++++

Right now it only can be ran from a console. Help should be shown if its run
with **-h** parameter.

::

    $ bin/media_downloader


.. [1] I know, I know, subtitles are not media files.
.. [2] This make the project name even worst, right ?

