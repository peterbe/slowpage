import time
import os
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
from tornado.options import define, options

define("debug", default=False, help="run in debug mode", type=bool)
define("port", default=8080, help="run on the given port", type=int)


class CrazyStaticFileHandler(tornado.web.StaticFileHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, path, *args, **kwargs):
        delay = 0
        print path
        if path == 'script.js':
            delay = 10
        if delay:
            print "\tsleeping", delay, "seconds"
            ioloop_instance = tornado.ioloop.IOLoop.instance()
            yield tornado.gen.Task(
                ioloop_instance.add_timeout,
                time.time() + delay
            )
        super(CrazyStaticFileHandler, self).get(path, *args, **kwargs)
        self.finish()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

class Version2Handler(tornado.web.RequestHandler):
    def get(self):
        self.render('index2.html')

class Version3Handler(tornado.web.RequestHandler):
    def get(self):
        self.render('index3.html')

routes = [
    (r"/", MainHandler),
    (r"/index2.html", Version2Handler),
    (r"/index3.html", Version3Handler),
]

if __name__ == "__main__":
    tornado.options.parse_command_line()
    application = tornado.web.Application(
        routes,
        debug=options.debug,
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        static_handler_class=CrazyStaticFileHandler,
    )
    application.listen(options.port)
    print "Starting server on localhost:%s" % options.port
    try:
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        pass
