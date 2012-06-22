<?php

class LineObjTest extends PHPUnit_Framework_TestCase
{
    protected $line;

    public function setUp()
    {
        $this->line = new lineObj();
        $start = new pointObj;
        $start->setXY(1,1);
        $middle = new pointObj();
        $middle->setXY(2,1);
        $end = new pointObj();
        $end->setXY(3,3);
        $this->line->add($start);
        $this->line->add($middle);
        $this->line->add($end);
    }

    /**
     * @expectedException           MapScriptException
     * @expectedExceptionMessage    Property 'numpoints' is read-only
     */
    public function test__setNumPoints()
    {
        $this->line->numpoints = 5;
    }

    public function test__getNumPoints()
    {
        $this->assertEquals(3, $this->line->numpoints);
    }

    public function testClone()
    {
        $newline = clone $this->line;
    }

}

?>
