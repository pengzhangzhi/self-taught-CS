/* Copyright (c) 2015-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package graph;

import org.junit.Test;

import java.util.*;

/**
 * An implementation of Graph.
 * 
 * <p>PS2 instructions: you MUST use the provided rep.
 * @author zhangzhiPeng
 */
public class ConcreteEdgesGraph<L> implements Graph<L> {
    
    private final Set<L> vertices = new HashSet<>();
    private final List<Edge> edges = new ArrayList<>();
    
    // Abstraction function:
    //   AF(vertices, edges) = a graph
    //
    // Representation invariant:
    // the two ends of vertex in any edge in edges must in vertices.
    // there are no repeat edges in `edges`.
    //
    // Safety from rep exposure:
    //   All filed all private vertices;
    //   vertices and edges are mutable.
    //   So any observors and producers make defensive copy of vertices and edges.
    
    // TODO constructor

    public ConcreteEdgesGraph() {
    }


    // TODO checkRep
    private void checkRep(){
        assert this.edges.isEmpty() && this.vertices.isEmpty(): "if no edges, there are no vertices.";
        Set<Edge> edgeSet = new HashSet<Edge>(this.edges);
        assert edgeSet.size() == this.edges.size(): "edges should have no repeat edges in it.";
        Set<L> verticesInEdges = new HashSet<>();
        for(var edge:edges){
            verticesInEdges.addAll(edge.vertices());
        }
        assert verticesInEdges.equals(this.vertices): "the two ends of vertex in any edge in edges must in vertices";
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
    
    @Override public Map<L, Integer> sources(L target) {
        throw new RuntimeException("not implemented");
    }
    
    @Override public Map<L, Integer> targets(L source) {
        throw new RuntimeException("not implemented");
    }
    
    // TODO toString()
    @Override
    public String toString() {
        return "ConcreteEdgesGraph{" +
                "vertices=" + vertices +
                ", edges=" + edges +
                '}';
    }

}

/**
 * TODO specification
 * An implementation of edge.
 * Immutable.
 * This class is internal to the rep of ConcreteEdgesGraph.
 * 
 * <p>PS2 instructions: the specification and implementation of this class is
 * up to you.
 */
class Edge<L> {

    // TODO fields
    private L source;
    private L target;
    private int weight;
    // Abstract Functions:
    // AF(source, target, weight) = an edge from source to target with weight.
    // Rep Invariant:
    // if the source and target are determined, the weight is also determined.
    // the source and target are not none.
    //


    // Rep Exposure:
    // The two field are string, which is immutable.


    // TODO constructor
    public Edge(L source, L target, int weight) {
        this.source = source;
        this.target = target;
        this.weight = weight;
        checkRep();
    }


    // TODO checkRep
    private void checkRep(){
        assert this.source != null && this.target != null: "source and target must be non-null string.";
    }
    // TODO methods
    /**
     * Get the source and target vertices in this edge.
     * @return a two-element set where the first element is the source vertex,
     *          and the second element is the target vertex.
     */
    public Set<L> vertices(){
        Set<L> vert = new HashSet<>();
        vert.add(this.source);
        vert.add(this.target);
        checkRep();
        return vert;
    }
    

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Edge)) return false;
        Edge edge = (Edge) o;
        return Objects.equals(getSource(), edge.getSource()) &&
                Objects.equals(getTarget(), edge.getTarget());
    }

    @Override
    public int hashCode() {
        return Objects.hash(getSource(), getTarget(), weight);
    }
    // TODO toString()
    @Override
    public String toString() {
        return "Edge{" +
                "source='" + source + '\'' +
                ", target='" + target + '\'' +
                ", weight='" + weight + '\'' +
                '}';
    }

    public L getSource() {
        return source;
    }

    public L getTarget() {
        return target;
    }

    public int getWeight() {
        return weight;
    }
}
