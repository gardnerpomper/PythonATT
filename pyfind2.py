#!/usr/bin/python
"""
simple grep-alternative example
"""

import sys
import re
import logging

def grep(regex,filenames,options={}):
    """
    search multiple files for matches to a regular expression
    """
    logger = logging.getLogger(__name__)
    #
    # ----- compile the regex (optionally case insensitive)
    #
    try:
        if options.get('nocase',False):
            pat = re.compile(regex,re.I)
        else:
            pat = re.compile(regex)
    except Exception as e:
        logger.error("compiling RE: {0}".format(e))
        return 1
    logger.info('regex: {}, files={}'.format(regex,filenames))
    #
    # ---- foreach file
    #
    fmtS = "{0}({2:4d}): {1}" if options.get('number',False) else "{0}: {1}"

    for fname in filenames:
        try:
            with open(fname) as f:
                logger.info(fname)
                #
                # ----- print the matchine lines
                # ----- optionally include the line number
                #
                for lineno,line in enumerate(f):
                    if not pat.search(line): continue
                    logger.debug(fmtS.format(fname,line.strip(),lineno))
                    print(fmtS.format(fname,line,lineno), end='')

        except IOError as e:
            print("Unable to open {0}: {1}".format(fname,e))
    return 0

if __name__ == '__main__':
    #
    # ----- handle command line args
    #
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-d','--debug',action='store_true', dest='debug',
                        help='turn on debugging')
    parser.add_argument('-i','--ignore-case',action='store_true', dest='nocase',
                        help='make search case insensitive')
    parser.add_argument('-n','--number',action='store_true',dest='number',
                        help='number output lines')
    parser.add_argument('regex', help='regular expression to match')
    parser.add_argument('filename',nargs='+',help='filename(s) to search')
    args = parser.parse_args()
    #
    # convert the argparse object to a dict
    #
    options = vars(args)
    #
    # enable logging
    #
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(filename='pyfind2.log',
                        filemode='w',
                        level=log_level)
    #
    # call the main function
    #
    rc = grep(args.regex,args.filename,options)
    sys.exit(rc)


