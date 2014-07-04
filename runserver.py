# coding=utf-8
"""Simple runner for our flask app.

see http://flask.pocoo.org/docs/patterns/packages/#larger-applications
"""
import optparse

from users import APP, LOGGER

if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option('-d', '--debug', dest='debug', default=False,
                      help='turn on Flask debugging', action='store_true')

    options, args = parser.parse_args()

    if options.debug:
        print 'Running in debug mode'
        LOGGER.info('Running in debug mode')
        APP.debug = True
    else:
        print 'Running in production mode'
        LOGGER.info('Running in production mode')

    print 'Starting.....'
    APP.run(host='0.0.0.0')
