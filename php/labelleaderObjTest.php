<?php

class LabelleaderObjTest extends PHPUnit_Framework_TestCase
{
    protected $labelleader;

    public function setUp()
    {
        $map_file = 'maps/labels-leader.map';
        $map = new mapObj($map_file);
        $layer = $map->getLayer(0);
        $class = $layer->getClass(0);
        $label = $class->getLabel(0);
        $this->labelleader = $class->leader;
    }

    public function testpmaxdistance()
    {

    }
}

?>
