#!/usr/bin/env python

import sys

sys.path.append( '../pymod' )
import pmstestlib

import mapscript

def dumpResultSet( layer ):
    layer.open()
    for i in range(1000):
        result = layer.getResult( i )
        if result is None:
            break
        
#        print '(%d,%d,%s)' % (result.shapeindex, result.tileindex,result.classindex)
        print '(%d,%d)' % (result.shapeindex, result.tileindex)
        
        s = layer.getShape( result.shapeindex, result.tileindex )
        for i in range(layer.numitems):
            print '%s: %s' % (layer.getItem(i), s.getValue(i))
            
    layer.close()
    
###############################################################################
# Open map and get working layer.

def rqtest_1():
    pmstestlib.map = mapscript.Map('../gdal/tileindex.map')
    pmstestlib.layer = pmstestlib.map.getLayer(0)

    return 'success'

###############################################################################
# Execute region query.

def rqtest_2():

    line = mapscript.Line()
    line.addPoint( mapscript.Point( 35, 25 ) )
    line.addPoint( mapscript.Point( 45, 25 ) )
    line.addPoint( mapscript.Point( 45, 35 ) )
    line.addPoint( mapscript.Point( 35, 25 ) )

    poly = mapscript.Shape( mapscript.MS_SHAPE_POLYGON )
    poly.addLine( line )

    pmstestlib.layer.queryByShape( pmstestlib.map, poly )

    return 'success'

###############################################################################
# Scan results, checking count and the first shape information.

def rqtest_3():
    layer = pmstestlib.layer
    
    #########################################################################
    # Check result count.
    layer.open()
    count = 0
    for i in range(1000):
        result = layer.getResult( i )
        if result is None:
            break
    
        count = count + 1

    if count != 55:
        pmstestlib.post_reason( 'got %d results instead of expected %d.' \
                             % (count, 55) )
        return 'fail'

    #########################################################################
    # Check first shape attributes.
    
    result = layer.getResult( 0 )
    s = layer.getShape( result.shapeindex, result.tileindex )
    
    if pmstestlib.check_items( layer, s,
                               [('value_0','115'),
                                ('red','115'),
                                ('green','115'),
                                ('blue','115'),
                                ('values','115'),
                                ('x','39.5'),
                                ('y','29.5')] ) == 0:
        return 'fail'
    
    #########################################################################
    # Check last shape attributes.

    result = layer.getResult( 54 )
    s = layer.getShape( result.shapeindex, result.tileindex )

    if pmstestlib.check_items( layer, s,
                               [('value_0','132'),
                                ('x','44.5'),
                                ('y','25.5')] ) == 0:
        return 'fail'
    
    layer.close() 
    layer.close() # discard resultset.

    return 'success'
    
###############################################################################
# Execute multiple point query, and check result.

def rqtest_4():

    pnt = mapscript.Point()
    pnt.x = 35.5
    pnt.y = 25.5
    
    pmstestlib.layer.queryByPoint( pmstestlib.map, pnt, mapscript.MS_MULTIPLE,
                                   1.25 )

    return 'success'

###############################################################################
# Scan results, checking count and the first shape information.

def rqtest_5():
    layer = pmstestlib.layer
    
    #########################################################################
    # Check result count.
    layer.open()
    count = 0
    for i in range(1000):
        result = layer.getResult( i )
        if result is None:
            break
    
        count = count + 1

    if count != 9:
        pmstestlib.post_reason( 'got %d results instead of expected %d.' \
                             % (count, 9) )
        return 'fail'

    #########################################################################
    # Check first shape attributes.
    
    result = layer.getResult( 0 )
    s = layer.getShape( result.shapeindex, result.tileindex )
    
    if pmstestlib.check_items( layer, s,
                               [('value_0','123'),
                                ('x','34.5'),
                                ('y','26.5')] ) == 0:
        return 'fail'
    
    #########################################################################
    # Check last shape attributes.

    result = layer.getResult( 8 )
    s = layer.getShape( result.shapeindex, result.tileindex )

    if pmstestlib.check_items( layer, s,
                               [('value_0','107'),
                                ('x','36.5'),
                                ('y','24.5')] ) == 0:
        return 'fail'
    
    layer.close() 
    layer.close() # discard resultset.

    return 'success'
    
###############################################################################
# Execute multiple point query, and check result.

def rqtest_6():

    pnt = mapscript.Point()
    pnt.x = 35.2
    pnt.y = 25.3
    
    pmstestlib.layer.queryByPoint( pmstestlib.map, pnt, mapscript.MS_SINGLE,
                                   10.0 )

    return 'success'

###############################################################################
# Scan results, checking count and the first shape information.

def rqtest_7():
    layer = pmstestlib.layer
    
    #########################################################################
    # Check result count.
    layer.open()
    count = 0
    for i in range(1000):
        result = layer.getResult( i )
        if result is None:
            break
    
        count = count + 1

    if count != 1:
        pmstestlib.post_reason( 'got %d results instead of expected %d.' \
                             % (count, 1) )
        return 'fail'

    #########################################################################
    # Check first shape attributes.
    
    result = layer.getResult( 0 )
    s = layer.getShape( result.shapeindex, result.tileindex )
    
    if pmstestlib.check_items( layer, s,
                               [('value_0','115'),
                                ('x','35.5'),
                                ('y','25.5')] ) == 0:
        return 'fail'
    
    layer.close() 
    layer.close() # discard resultset.

    return 'success'
    
###############################################################################
# Execute multiple point query, and check result.

def rqtest_8():

    rect = mapscript.Rect()
    rect.minx = 35
    rect.maxx = 45
    rect.miny = 25
    rect.maxy = 35
    
    pmstestlib.layer.queryByRect( pmstestlib.map, rect )

    return 'success'

###############################################################################
# Scan results, checking count and the first shape information.

def rqtest_9():
    layer = pmstestlib.layer
    
    #########################################################################
    # Check result count.
    layer.open()
    count = 0
    for i in range(1000):
        result = layer.getResult( i )
        if result is None:
            break
    
        count = count + 1

    if count != 100:
        pmstestlib.post_reason( 'got %d results instead of expected %d.' \
                             % (count, 100) )
        return 'fail'

    #########################################################################
    # Check first shape attributes.
    
    result = layer.getResult( 0 )
    s = layer.getShape( result.shapeindex, result.tileindex )
    
    if pmstestlib.check_items( layer, s,
                               [('value_0','148'),
                                ('red','148'),
                                ('green','148'),
                                ('blue','148'),
                                ('values','148'),
                                ('x','35.5'),
                                ('y','34.5')] ) == 0:
        return 'fail'
    
    #########################################################################
    # Check last shape attributes.

    result = layer.getResult( 99 )
    s = layer.getShape( result.shapeindex, result.tileindex )

    if pmstestlib.check_items( layer, s,
                               [('value_0','132'),
                                ('red','132'),
                                ('green','132'),
                                ('blue','132'),
                                ('values','132'),
                                ('x','44.5'),
                                ('y','25.5')] ) == 0:
        return 'fail'
    
    layer.close() 
    layer.close() # discard resultset.

    return 'success'
    
###############################################################################
# Cleanup.

def rqtest_cleanup():
    pmstestlib.layer = None
    pmstestlib.map = None
    return 'success'

test_list = [
    rqtest_1,
    rqtest_2,
    rqtest_3,
    rqtest_4,
    rqtest_5,
    rqtest_6,
    rqtest_7,
    rqtest_8,
    rqtest_9,
    rqtest_cleanup ]

if __name__ == '__main__':

    pmstestlib.setup_run( 'rqtest' )

    pmstestlib.run_tests( test_list )

    pmstestlib.summarize()

