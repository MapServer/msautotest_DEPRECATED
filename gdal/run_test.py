#!/usr/bin/env python
###############################################################################
# $Id$
#
# Project:  MapServer
# Purpose:  Test harnass script for MapServer autotest.
# Author:   Frank Warmerdam, warmerda@home.com
#
###############################################################################
#  Copyright (c) 2002, Frank Warmerdam <warmerdam@pobox.com>
# 
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
# 
#  The above copyright notice and this permission notice shall be included
#  in all copies or substantial portions of the Software.
# 
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#  OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#  DEALINGS IN THE SOFTWARE.
###############################################################################
# 
# $Log$
# Revision 1.3  2003/01/23 22:47:50  frank
# removed python2.2 use of st_size
#
# Revision 1.2  2002/12/21 21:47:20  frank
# preserved failed results
#
# Revision 1.1  2002/11/22 21:13:19  frank
# New
#

import sys
import os
import string

###############################################################################
# get_mapfile_list()

def get_mapfile_list():

    files = os.listdir('.')
    map_files = []

    for file in files:
        if file[-4:] == '.map':
            map_files.append( file )

    return map_files

###############################################################################
# compare_result()

def compare_result( filename ):
    import filecmp
    
    result_file = 'result/' + filename
    expected_file = 'expected/'+ filename

    try:
        result_stat = os.stat( result_file )
    except OSError:
        return 'noresult'
    
    try:
        expected_stat = os.stat( expected_file )
    except OSError:
        return 'noexpected'

    if filecmp.cmp(expected_file,result_file,0,1):
        return 'match'
    else:
        return 'nomatch'
    
    return 'match'

###############################################################################
# has_requires()

def has_requires( version_info, requires_list ):

    for item in requires_list:
        if string.find( version_info, item ) == -1:
            return 0
        
    return 1

###############################################################################
# read_test_directives()

def read_test_directives( mapfile_name ):

    runparms_list = []
    require_list = []
    
    lines = open(mapfile_name).readlines()
    for line in lines:
        req_off = string.find( line, 'REQUIRES:' )
        if req_off != -1:
            items = string.split( line[req_off+9:] )
            for item in items:
                require_list.append( item )
                
        run_off = string.find( line, 'RUN_PARMS:' )
        if run_off != -1:
            items = string.split( line[run_off+10:], None, 1 )
            if len(items) == 2:
                runparms_list.append( (items[0], items[1]) )
            elif len(items) == 1:
                runparms_list.append( (items[0],
                                       '[SHP2IMG] -m [MAPFILE] -o [RESULT]') )
                                     
    if len(runparms_list) == 0:
        runparms_list.append( (mapfile_name[:-4] + '.png',
                               '[SHP2IMG] -m [MAPFILE] -o [RESULT]') )

    return (runparms_list, require_list)
            

###############################################################################
# run_tests()

def run_tests( argv ):

    skip_count = 0
    fail_count = 0
    succeed_count = 0
    init_count = 0
    
    ###########################################################################
    # Establish paths to use for various testable programs.
    shp2img = 'shp2img' 
    
    ###########################################################################
    # Get version info.
    version_info = os.popen( shp2img + ' -v' ).read()
    print 'version = %s' % version_info
    
    ###########################################################################
    # Check directory wide requirements.
    try:
        (runparms_list, requires_list) = read_test_directives( 'all_require.txt' )
        if not has_requires( version_info, requires_list ):
            print 'Some or all of the following requirements for this directory of tests\nare not available:'
            print requires_list
            return
    except:
        pass
    
    ###########################################################################
    # Process all mapfiles.
    map_files = get_mapfile_list()

    for map in map_files:

        print 'Processing: %s' % map
        (runparms_list, requires_list) = read_test_directives( map )

        if not has_requires( version_info, requires_list ):
            print '    missing some or all of required components, skip.'
            skip_count += len(runparms_list)
            continue
        
        #######################################################################
        # Handle each RUN_PARMS item in this file.
        for run_item in runparms_list:
            out_file = run_item[0]
            command = run_item[1]
            
            command = string.replace( command, '[RESULT]', 'result/'+out_file )
            command = string.replace( command, '[MAPFILE]', map )
            command = string.replace( command, '[SHP2IMG]', 'shp2img' )
            command = string.replace( command, '[LEGEND]', 'legend' )
            command = string.replace( command, '[SCALEBAR]', 'scalebar' )

            os.system( command )

            cmp = compare_result( out_file )
            
            if cmp == 'match':
                succeed_count = succeed_count + 1
                os.remove( 'result/' + out_file )
                print '    results match.'
            elif cmp ==  'nomatch':
                fail_count = fail_count + 1
                print '    results dont match, TEST FAILED.'
            elif cmp == 'noresult':
                fail_count = fail_count + 1
                print '    no result file generated, TEST FAILED.'
            elif cmp == 'noexpected':
                print '    no expected file exists, accepting result as expected.'
                init_count = init_count + 1
                os.rename( 'result/' + out_file, 'expected/' + out_file )
                
    print 'Test done:\n    %d tested skipped\n    %d tests succeeded\n    %d tests failed\n    %d test results initialized' \
          % (skip_count, succeed_count, fail_count, init_count )

###############################################################################
# main()

if __name__ == '__main__':
    run_tests( sys.argv[1:] )
    


