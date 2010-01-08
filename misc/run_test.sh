#!/bin/sh

SHP2IMG=shp2img
LEGEND=legend
SCALEBAR=scalebar

MAPS=`ls *.map`

for map in $MAPS ; do

  basename=`basename $map .map`
  png_file=${basename}.png

  rm -f result/$png_file

  case $basename in 
   (*_legend )
     echo "Processing(legend): $map"
     $LEGEND $map result/$png_file
     ;;
   (*_scalebar )
     echo "Processing(scalebar): $map"
     $SCALEBAR $map result/$png_file
     ;;
   (*)
     echo "Processing(shp2img): $map"
     $SHP2IMG -m $map -o result/$png_file
     ;;
  esac

  if [ ! -r result/$png_file ] ; then
    echo "  Shp2img did not produce an output file, SERIOUS TEST FAILURE."
    continue
  fi

  if [ ! -r expected/$png_file ] ; then
    echo "  No expected result, accepting this result as expected."
    mv result/$png_file expected/$png_file
  elif cmp --quiet expected/$png_file result/$png_file ; then
    rm result/$png_file
    echo "  Results matched." 
  else
    echo "  Results differed, TEST FAILURE." 
  fi
  echo
done
