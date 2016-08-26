#!/usr/bin/python
import logging
import sys
import os.path
import math

def ls_files(files, options={}):
    """
    list file names and sizes, formatted and sorted
    """
    logger = logging.getLogger(__name__)
    logger.info('ls_files: {}'.format(options))
    logger.info('options : {}'.format(options))
    #
    # find max filename length and initialize max width
    # for size field
    #
    listing = []
    max_len = max( [len(f) for f in files])
    max_size = 0
    #
    # foreach file
    #
    for f in files:
        #
        # ignore directories
        #
        if os.path.isdir(f):
            print("ERROR! {0} is a directory".format(f))
            continue
        #
        # find the file size and estimate the
        # number of characters to print it with
        # commas
        #
        file_sz = os.path.getsize(f)
        n_digits = math.ceil(math.log10(file_sz))
        n_digits += n_digits//3
        if n_digits > max_size:
            max_size = n_digits
        #
        # build a list of filenames and size
        #
        listing.append( (f,file_sz))
    #
    # sort the list as specified (name or size)
    #
    if options.get('sort','name').endswith('size'):
        listing = sorted(listing,key=lambda t: t[1])
    else:
        listing = sorted(listing)
    #
    # if descending sort specified, reverse the list
    #
    if options.get('sort','name').startswith('-'):
        listing.reverse()
    #
    # format the file info
    #
    listing = ['{0:<{1}} {2:>{3},d}'.format(fn,max_len,sz,max_size) for (fn,sz) in listing]
    return listing

if __name__ == '__main__':
    #
    # ----- handle command line args
    #
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-d','--debug',action='store_true', dest='debug',
                        help='turn on debugging')
    parser.add_argument('-s','--sort',action='store', dest='sort',default='name',
                        help='how to sort [+-][size|name]')
    parser.add_argument('filename',nargs='+',help='filename(s) to search')
    args = parser.parse_args()
    #
    # convert the argparse object to a dict
    #
    import sys
    options = vars(args)
    #
    # enable logging
    #
    logfile = os.path.splitext(os.path.basename(sys.argv[0]))[0] + '.log'
    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(filename=logfile,
                        filemode='w',
                        level=log_level)
    #
    # call the main function
    #
    listing = ls_files(args.filename,options)
    print('\n'.join(listing))
