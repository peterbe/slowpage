Experimenting with browsers' resource download behaviour
========================================================

By: Peter Bengtsson, mail@peterbe.com


About this experiment
---------------------

I wanted to know how various browsers deal with external resources
getting stuck and how the browser decides to proceed.

This experiment makes three URLs available:

* http://localhost:8080/
* http://localhost:8080/index2.html
* http://localhost:8080/index3.html

Each page references 4 different resources:

* script.js
* style.css
* photo.jpg
* favicon.ico

What I do is that if the `script.js` file is requested, I deliberately
make it take 10 seconds to download. That simulates the sometimes
sporadic delays caused when you reference a javascript file on a
different DNS location.

The server is asynchronous so, whilst your browser is waiting (10
seconds) for `/static/script.js` you can load `/static/style.css` or
`/static/photo.jpg`.


Why this experiment
-------------------

I wanted to check a few things when I wrote this:

http://www.peterbe.com/plog/never-put-external-javascript-in-the-head


How to run it
-------------

You need python to run it. Install the dependencies first:

```
pip install -r requirements.txt
```

then start the server:

```
python asyncserver.py
```

Then go to `http://localhost:8080/` and notice what a terrible
experience it is just because the page has an external resource in the
head tag that the browser can't wait for.
