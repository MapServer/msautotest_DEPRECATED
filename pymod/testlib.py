###############################################################################
# $Id: mstestlib.py 6763 2007-08-31 21:05:17Z warmerdam $
#
# Project:  MapServer
# Purpose:  Generic test machinery shared between mstestlib and pmstestlib.
# Author:   Frank Warmerdam, warmerdam@pobox.com
#
###############################################################################
#  Copyright (c) 2007, Frank Warmerdam <warmerdam@pobox.com>
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

import sys
import os
import string

have_pdiff = None

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

    if filecmp.cmp(expected_file,result_file,0):
        return 'match'

    ###################################################################
    # Check image checksums with GDAL if it is available.
    
    try:
	import osgeo.gdal
        gdal.PushErrorHandler()
	exp_ds = gdal.Open( expected_file )
        gdal.PopErrorHandler()
        if exp_ds == None:
            return 'nomatch'
        
	res_ds = gdal.Open( result_file )

        match = 1
	for band_num in range(1,exp_ds.RasterCount+1):
	    if res_ds.GetRasterBand(band_num).Checksum() != \
                exp_ds.GetRasterBand(band_num).Checksum():
		match = 0

        if match == 1:
            return 'files_differ_image_match'
    except:
        pass

    ###################################################################
    # Test with perceptualdiff if this is tiff or png.  If we discover
    # we don't have it, then set have_pdiff to 'false' so we will know.
    
    global have_pdiff

    try:
        result = open(result_file, "rb").read(1000)
    except:
        result = ''
    
    if have_pdiff != 'false' and \
       ('\x49\x49\x2A\x00' in result \
       or '\x49\x49\x00\x2A' in result \
       or '\x89\x50\x4e\x47\x0d\x0a\x1a\x0a' in result):
    
        try:
            cmd = 'perceptualdiff %s %s -verbose > pd.out' % (result_file,expected_file)
            os.system( cmd )
            pdout = open('pd.out').read()
            os.remove( 'pd.out' )
            
            if string.find(pdout,'PASS:') != -1 \
               and string.find(pdout,'binary identical') != -1:
                return 'files_differ_image_match'
        
            if string.find(pdout,'PASS:') != -1 \
               and string.find(pdout,'indistinguishable') != -1:
                return 'files_differ_image_nearly_match'

            if string.find(pdout,'PASS:') == -1 \
               and string.find(pdout,'FAIL:') == -1:
                have_pdiff = 'false'

        except:
            pass
        
    return 'nomatch'
    
