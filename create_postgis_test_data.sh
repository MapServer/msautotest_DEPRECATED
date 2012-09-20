#!/bin/bash

psql -c "drop database if exists msautotest" -U postgres
psql -c "create database msautotest" -U postgres
psql -c "create extension postgis" -d msautotest -U postgres
shp2pgsql -g the_geom query/data/bdry_counpy2.shp bdry_counpy2 | psql -U postgres -d msautotest
shp2pgsql -g the_geom -s 3978 wxs/data/popplace.shp popplace | psql -U postgres -d msautotest
shp2pgsql -g the_geom -s 3978 wxs/data/province.shp province | psql -U postgres -d msautotest
shp2pgsql -g the_geom -s 3978 wxs/data/road.shp road| psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern1.shp pattern1 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern2.shp pattern2 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern3.shp pattern3 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern4.shp pattern4 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern5.shp pattern5 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern6.shp pattern6 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern7.shp pattern7 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern8.shp pattern8 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern9.shp pattern9 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern10.shp pattern10 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern11.shp pattern11 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern12.shp pattern12 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern13.shp pattern13 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern14.shp pattern14 | psql -d msautotest -U postgres
shp2pgsql -s 4326 -g the_geom wxs/data/pattern15.shp pattern15 | psql -d msautotest -U postgres
