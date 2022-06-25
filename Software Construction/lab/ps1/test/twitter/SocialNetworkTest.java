/* Copyright (c) 2007-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package twitter;

import static org.junit.Assert.*;

import java.lang.reflect.Array;
import java.time.Instant;
import java.util.*;

import org.junit.Test;

public class SocialNetworkTest {

    /*
     * TODO: your testing strategies for these methods should go here.
     * See the ic03-testing exercise for examples of what a testing strategy comment looks like.
     * Make sure you have partitions.
     *
     *  partition strategy:
     *  is text contains mentioned users: true, false
     *  tweets.length: 0, > 0
     *  has capital and small divergence: true, false
     *  number of key of the socialNetwork: 0, 1, > 1
     *  number of value of a key in socialNetwork: 0, 1, >1
     *
     *  partition strategy: socialNetwork graphs
     *  length of socialNetwork graph: 0, 1, > 1
     *  the length of following users: 0, 1, > 1
     *  mutual following: true, false
     *
     */
    private static final Instant d1 = Instant.parse("2016-02-17T10:00:00Z");
    private static final Instant d2 = Instant.parse("2016-02-17T11:00:00Z");
    private static final Tweet tweet1 = new Tweet(1, "alyssa", "is it reasonable to talk about rivest so much?", d1);
    private static final Tweet tweet2 = new Tweet(2, "bbitdiddle", "rivest talk in 30 minutes #hype", d2);
    private static final Tweet tweet3 = new Tweet(3, "xiaoMing", "rivest talk in 30 minutes #hype @zhangzhipeng", d2);
    private static final Tweet tweet4 = new Tweet(4, "bbitdiddle", "@ZHANGZHIPENG rivest talk @zhangzhipeng in 30 minutes #hype ", d2);
    private static final Tweet tweet5 = new Tweet(5, "xiaoli", "rivest talk @xiaoMing in 30 minutes @XIAOMING #hype", d2);
    private static final Tweet tweet6 = new Tweet(6, "xiaowang", "rivest talk in zhangzhipengcs@outlook.com @xiaoli 30 minutes #hype", d2);
    private static final Tweet tweet7 = new Tweet(7, "zhangzhipeng", "rivest talk in zhangzhipengcs@outlook.com @xiaoMing 30 minutes #hype", d2);

    @Test(expected=AssertionError.class)
    public void testAssertionsEnabled() {
        assert false; // make sure assertions are enabled with VM argument: -ea
    }
    // covers tweets.length: > 0
    // is text contains mentioned users: true
    // has capital and small divergence:  false
    // number of key of the socialNetwork:  1
    // number of value of a key in socialNetwork: 1
    @Test
    public void testGuessFollowsGraphManyMentioned() {
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(new ArrayList<Tweet>(Collections.singleton(tweet3)));

        assertTrue("expected xiaoming's graph", followsGraph.containsKey("xiaoming"));
        assertTrue("expected xiaoming's graph", followsGraph.get("xiaoming").contains("zhangzhipeng"));
    }

    // covers tweets.length: > 0
    // is text contains mentioned users: true
    // has capital and small divergence:  true
    // number of key of the socialNetwork:  2
    // number of value of a key in socialNetwork: 2
    @Test
    public void testGuessFollowsGraphManyToManyMentionedCaseDivergence() {
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(new ArrayList<Tweet>(Arrays.asList(tweet5, tweet6)));

        assertTrue("expected bbitdiddle's graph", followsGraph.containsKey("xiaowang"));
        assertTrue("expected bbitdiddle's graph", followsGraph.get("xiaowang").contains("xiaoli"));
        assertTrue("expected bbitdiddle's graph", followsGraph.containsKey("xiaoli"));
        assertTrue("expected bbitdiddle's graph", followsGraph.get("xiaoli").contains("xiaoming"));
    }

    // covers tweets.length: > 0
    // is text contains mentioned users: true
    // has capital and small divergence:  true
    // number of key of the socialNetwork:  1
    // number of value of a key in socialNetwork: 2
    @Test
    public void testGuessFollowsGraphManyMentionedCaseDivergence() {
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(new ArrayList<Tweet>(Arrays.asList(tweet4, tweet5)));

        assertTrue("expected bbitdiddle's graph", followsGraph.containsKey("xiaoli"));
        assertTrue("expected bbitdiddle's graph", followsGraph.get("xiaoli").contains("xiaoming"));
        assertTrue("expected bbitdiddle's graph", followsGraph.get("bbitdiddle").contains("zhangzhipeng"));
    }


    // covers tweets.length: > 0
    // is text contains mentioned users: false
    // has capital and small divergence:  false
    // number of key of the socialNetwork:  0
    // number of value of a key in socialNetwork: 0
    @Test
    public void testGuessFollowsGraphManyNoMentioned() {
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(new ArrayList<Tweet>(Arrays.asList(tweet1, tweet2)));

        assertTrue("expected empty graph, "+followsGraph, followsGraph.isEmpty());
    }

    // covers tweets.length: == 0
    // is text contains mentioned users: false
    // has capital and small divergence:  false
    // number of key of the socialNetwork: 0
    // number of value of a key in socialNetwork: 0
    @Test
    public void testGuessFollowsGraphEmpty() {
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(new ArrayList<>());

        assertTrue("expected empty graph", followsGraph.isEmpty());
    }

    //     *  covers:
    //     *  length of socialNetwork graph: 0,
    //     *  the length of following users: 0
    //     *  mutual following: true, false
    @Test
    public void testInfluencersEmpty() {
        Map<String, Set<String>> followsGraph = new HashMap<>();
        List<String> influencers = SocialNetwork.influencers(followsGraph);
        
        assertTrue("expected empty list", influencers.isEmpty());
    }

    //     *  covers:
    //     *  length of socialNetwork graph: 1
    //     *  the length of following users: 0
    //     *  mutual following: false
    @Test
    public void testInfluencersOneElementGraph() {
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(Collections.singletonList(tweet1));
        List<String> influencers = SocialNetwork.influencers(followsGraph);

        assertTrue("expected empty list", influencers.isEmpty());
    }

    //     *  covers:
    //     *  length of socialNetwork graph: 2
    //     *  the length of following users: 0
    //     *  mutual following: false
    @Test
    public void testInfluencersTwoElementGraph() {
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(List.of(tweet1, tweet2));
        List<String> influencers = SocialNetwork.influencers(followsGraph);

        assertTrue("expected empty list", influencers.isEmpty());
    }

    //     *  covers:
    //     *  length of socialNetwork graph: 2
    //     *  the length of following users set: > 0
    //     *  mutual following: false
    @Test
    public void testInfluencersTwoElementGraphManyFollowing() {
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(List.of(tweet3, tweet4));
        List<String> influencers = SocialNetwork.influencers(followsGraph);

        assertTrue("expected pengzhangzhi", influencers.contains("zhangzhipeng"));
    }

    //     *  covers:
    //     *  length of socialNetwork graph: 2
    //     *  the length of following users set: > 0
    //     *  mutual following: true
    @Test
    public void testInfluencersTwoElementGraphManyFollowingMutualFollowing() {
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(List.of(tweet3, tweet7));
        List<String> influencers = SocialNetwork.influencers(followsGraph);

        assertTrue("expected zhangzhipeng", influencers.contains("zhangzhipeng"));
        assertTrue("expected xiaoming", influencers.contains("xiaoming"));
    }

    //     *  covers:
    //     *  length of socialNetwork graph: 2
    //     *  the length of following users set: > 0
    //     *  mutual following: true
    //     * multiple followers: true
    @Test
    public void testInfluencersTwoElementGraphManyFollowingMutualFollowingMultipleFollower() {
        Map<String, Set<String>> followsGraph = SocialNetwork.guessFollowsGraph(List.of(tweet3, tweet5,tweet7));
        List<String> influencers = SocialNetwork.influencers(followsGraph);
        assertEquals(0, influencers.indexOf("xiaoming"));
        assertEquals(1, influencers.indexOf("zhangzhipeng"));
    }

    /*
     * Warning: all the tests you write here must be runnable against any
     * SocialNetwork class that follows the spec. It will be run against several
     * staff implementations of SocialNetwork, which will be done by overwriting
     * (temporarily) your version of SocialNetwork with the staff's version.
     * DO NOT strengthen the spec of SocialNetwork or its methods.
     * 
     * In particular, your test cases must not call helper methods of your own
     * that you have put in SocialNetwork, because that means you're testing a
     * stronger spec than SocialNetwork says. If you need such helper methods,
     * define them in a different class. If you only need them in this test
     * class, then keep them in this test class.
     */

}
