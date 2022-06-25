/* Copyright (c) 2015-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package graph;

import static org.junit.Assert.*;

import org.junit.Test;

import java.util.HashSet;

/**
 * Tests for ConcreteEdgesGraph.
 * 
 * This class runs the GraphInstanceTest tests against ConcreteEdgesGraph, as
 * well as tests for that particular implementation.
 * 
 * Tests against the Graph spec should be in GraphInstanceTest.
 */
public class ConcreteEdgesGraphTest extends GraphInstanceTest {
    
    /*
     * Provide a ConcreteEdgesGraph for tests in GraphInstanceTest.
     */
    @Override public Graph<String> emptyInstance() {
        return new ConcreteEdgesGraph();
    }
    
    /*
     * Testing ConcreteEdgesGraph...
     */
    
    // Testing strategy for ConcreteEdgesGraph.toString()
    //   split graph into:
    //      1. vertices, empty, non-empty.
    //      2. edges, empty, non-empty.
    //
    
    // TODO tests for ConcreteEdgesGraph.toString()

    @Test
    public void testEmpty(){
        Graph<String> graph = emptyInstance();
        System.out.println(graph.toString());
    }

    @Test
    public void testNonEmpty(){
        Graph<String> graph = emptyInstance();
        graph.add("1");
        graph.add("2");
        graph.set("1","2",1);
        System.out.println(graph.toString());
    }
    
    /*
     * Testing Edge...
     */
    
    // Testing strategy for Edge
    //   vertices()
    //

    @Test
    public void testVertices(){
        Edge edge = new Edge("1","2",1);
        assertEquals("The num of vertex of edge must be two. ",2,edge.vertices().size());
    }
    
    // TODO tests for operations of Edge
    
}
