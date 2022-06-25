/* Copyright (c) 2015-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package graph;

import java.util.*;

/**
 * An implementation of Graph.
 * 
 * <p>PS2 instructions: you MUST use the provided rep.
 */
public class ConcreteVerticesGraph<L> implements Graph<L> {
    
    private final List<Vertex> vertices = new ArrayList<>();
    
    // Abstraction function:
    //   AF(vertices) = a Graph where each vertex in vertices.
    // Representation invariant:
    //   no repeat elements in vertices.
    // Safety from rep exposure:
    //   make defensive copy.
    
    // TODO constructor

    public ConcreteVerticesGraph() {
    }

    // TODO checkRep
    private void checkRep(){
        Set<Vertex> verticesSet = new HashSet<Vertex>(this.vertices);
        assert verticesSet.size() == this.vertices.size(): "graph has no repeat vertex.";
    }
    
    @Override public boolean add(L vertex) {
        throw new RuntimeException("not implemented");
    }
    
    @Override public int set(L source, L target, int weight) {
        throw new RuntimeException("not implemented");
    }
    
    @Override public boolean remove(L vertex) {
        throw new RuntimeException("not implemented");
    }
    
    @Override public Set<L> vertices() {
        throw new RuntimeException("not implemented");
    }
    
    @Override public Map<L, L> sources(L target) {
        throw new RuntimeException("not implemented");
    }
    
    @Override public Map<L, L> targets(L source) {
        throw new RuntimeException("not implemented");
    }
    
    // TODO toString()

    @Override
    public String toString() {
        return "ConcreteVerticesGraph{" +
                "vertices=" + vertices +
                '}';
    }
}

/**
 * TODO specification
 * Mutable.
 * This class is internal to the rep of ConcreteVerticesGraph.
 * 
 * <p>PS2 instructions: the specification and implementation of this class is
 * up to you.
 */
class Vertex<L> {
    
    // TODO fields
    private L label;
    private Map<L,L> targetVertices;


    // Abstraction function:
    //   AF(label,targetVertices) = a vertex named label that points to target vertices with corresponding weights.
    // Representation invariant:
    //   label is not null.
    // Safety from rep exposure:
    //   This class is mutable, thus there is no need to make defensive copy..
    //   The targetVertices is also mutable.
    
    // TODO constructor

    public Vertex(L label, Map<L, L> targetVertices) {
        this.label = label;
        this.targetVertices = targetVertices;
    }

    // TODO checkRep
    private void checkRep(){
        assert this.label != null;
    }
    // TODO methods

    /**
    *  get all the target vertices from current vertex.
    *
     * @return a set of all the target vertices from current vertex.
     * */
    public Set<L> targets(){
        return this.targetVertices.keySet();
    }

    // TODO toString()


    @Override
    public String toString() {
        return "Vertex{" +
                "label='" + label + '\'' +
                ", targetVertices=" + targetVertices +
                '}';
    }
}
