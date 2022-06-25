/* Copyright (c) 2015-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package graph;

import static org.junit.Assert.*;

import java.util.Collections;
import java.util.Map;
import java.util.Set;

import org.junit.Test;

/**
 * Tests for instance methods of Graph.
 * 
 * <p>PS2 instructions: you MUST NOT add constructors, fields, or non-@Test
 * methods to this class, or change the spec of {@link #emptyInstance()}.
 * Your tests MUST only obtain Graph instances by calling emptyInstance().
 * Your tests MUST NOT refer to specific concrete implementations.
 */
public abstract class GraphInstanceTest {
    
    // Testing strategy
    //   add()
    //   input: new vertex, existing vertex
    //
    //   set()
    //   test functionality: add, change, remove edge.
    //   for add, the weight is non-zero, the edge does not exist.
    //   and change, the weight is non-zero, the edge exist.
    //   for remove, the weight is zero, the edge exists.
    //
    //   remove()
    //   input vertex: existing and new vertex
    //
    //   vertices()
    //   split into empty graph and non-empty graph
    //
    //   sources()
    //   1. input target does not exist.
    //   2. exist,
    //      2.1 has not sources.
    //      2.2 has sources.
    //
    //   target()
    //   1. input source does not exist.
    //   2. exist,
    //      2.1 has not target.
    //      2.2 has target.
    
    /**
     * Overridden by implementation-specific test classes.
     * 
     * @return a new empty graph of the particular implementation being tested
     */
    public abstract Graph<String> emptyInstance();
    
    @Test(expected=AssertionError.class)
    public void testAssertionsEnabled() {
        assert false; // make sure assertions are enabled with VM argument: -ea
    }

    @Test
    public void testInitialVerticesEmpty() {
        // TODO you may use, change, or remove this test
        assertEquals("expected new graph to have no vertices",
                Collections.emptySet(), emptyInstance().vertices());
    }

    @Test
    public void testAddNewVertex() {
        ;
        assertTrue("expected successful adding",emptyInstance().add("1"));
    }

    @Test
    public void testAddExistingVertex() {
        emptyInstance().add("1");
        assertFalse("expected fail adding",emptyInstance().add("1"));
    }

    @Test
    public void testAddEdge() {
        emptyInstance().add("1");
        emptyInstance().add("2");

        assertEquals("expected successful adding new edge",0,emptyInstance().set("1","2",2));
    }

    @Test
    public void testUpdateEdge() {
        emptyInstance().add("1");
        emptyInstance().add("2");
        emptyInstance().set("1","2",2);

        assertEquals("expected successful update edge",2,emptyInstance().set("1","2",3));
    }

    @Test
    public void testRemoveEdge() {
        emptyInstance().add("1");
        emptyInstance().add("2");
        emptyInstance().set("1","2",2);

        assertEquals("expected successful remove edge",2,emptyInstance().set("1","2",0));
    }
    @Test
    public void testRemoveNonExistingVertex() {
        Boolean result = emptyInstance().remove("1");
        assertEquals("expected fail of removing non-existing vertex",false,result);
    }

    @Test
    public void testRemoveExistingVertex() {
        emptyInstance().add("1");
        emptyInstance().add("2");
        emptyInstance().set("1","2",2);
        Boolean result = emptyInstance().remove("1");
        // Check the vertex is removed and those connected edges are removed.
        assertEquals("expected success of removing non-existing vertex",true,result);
        assertEquals("no connected edge from 1 to 2.",0, java.util.Optional.ofNullable(emptyInstance().sources("2").get("1")));
    }


    @Test
    public void testVertexNonEmptyGraph() {
        emptyInstance().add("1");
        emptyInstance().add("2");
        Set<String> result = emptyInstance().vertices();
        assertEquals("expected two vertex",2,result.size());
    }

    @Test
    public void testSourceNoExist() {

        Map<String, Integer> target = emptyInstance().targets("1");
        assertTrue("the source does not exist in the graph, thus its targets should be empty.",target.isEmpty());
    }

    @Test
    public void testSourceExistHasNoTarget() {
        emptyInstance().add("1");
        Map<String, Integer> target = emptyInstance().targets("1");
        assertTrue("the source is in the graph, but it has no connected nodes, thus its targets should be empty.",target.isEmpty());

    }

    @Test
    public void testSourceExistHasTarget() {
        emptyInstance().add("1");
        emptyInstance().add("2");
        emptyInstance().set("1","2",1);
        Map<String, Integer> target = emptyInstance().targets("1");
        assertFalse("the source is in the graph and it has connected nodes, thus its targets should be non empty.",target.isEmpty());
        assertEquals("the edge from source to target should be 1",java.util.Optional.of(1),target.get("2"));
    }

    @Test
    public void testTargetNoExist() {

        Map<String, Integer> source = emptyInstance().sources("1");
        assertTrue("the target does not exist in the graph, thus its sources should be empty.",source.isEmpty());
    }

    @Test
    public void testTargetExistHasNoSource() {
        emptyInstance().add("1");
        Map<String, Integer> source = emptyInstance().sources("1");
        assertTrue("the target is in the graph, but it has no connected nodes, thus its source should be empty.",
                source.isEmpty());

    }

    @Test
    public void testTargetExistHasSource() {
        emptyInstance().add("1");
        emptyInstance().add("2");
        emptyInstance().set("1","2",1);
        Map<String, Integer> source = emptyInstance().sources("2");
        assertFalse("the target is in the graph and it has connected nodes, thus its source should be non empty.",source.isEmpty());
        assertEquals("the edge from source to the target should be 1",java.util.Optional.of(1),source.get("1"));
    }

    // TODO other tests for instance methods of Graph
    
}
