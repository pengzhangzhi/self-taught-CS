/* Copyright (c) 2007-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package twitter;

import static org.junit.Assert.*;

import java.time.Instant;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Set;

import org.junit.Test;

public class ExtractTest {

    /*
     * TODO: your testing strategies for these methods should go here.
     * See the ic03-testing exercise for examples of what a testing strategy comment looks like.
     * Make sure you have partitions.
     *
     * Testing strategy for timespan
     * Partition the input as follows:
     * tweets.length(): 1, >1
     * tweets similarity: none of tweet are similar, all of tweet are similar, part of tweet are similar.
     *
     * Testing strategy for mention
     * valid mention: 0, >0
     * capital and small letter : same mentions but presented in full capital and small letter,
     *                            same mentions but presented in partial capital and small letter,
     *                              same mentions in full capital or small letter.
     *
     *
     */
    
    private static final Instant d1 = Instant.parse("2016-02-17T10:00:00Z");
    private static final Instant d2 = Instant.parse("2016-02-17T11:00:00Z");
    
    private static final Tweet tweet1 = new Tweet(1, "alyssa", "is it reasonable to talk about rivest so much?", d1);
    private static final Tweet tweet2 = new Tweet(2, "bbitdiddle", "rivest talk in 30 minutes #hype", d2);
    private static final Tweet tweet3 = new Tweet(3, "bbitdiddle", "rivest talk in 30 minutes #hype @zhangzhipeng", d2);
    private static final Tweet tweet4 = new Tweet(4, "bbitdiddle", "@ZHANGZHIPENG rivest talk @zhangzhipeng in 30 minutes #hype ", d2);
    private static final Tweet tweet5 = new Tweet(5, "bbitdiddle", "rivest talk @xiaoMing in 30 minutes @XIAOMING #hype", d2);
    private static final Tweet tweet6 = new Tweet(6, "bbitdiddle", "rivest talk in zhangzhipengcs@outlook.com 30 minutes #hype", d2);

    @Test(expected=AssertionError.class)
    public void testAssertionsEnabled() {
        assert false; // make sure assertions are enabled with VM argument: -ea
    }
    
    @Test
    public void testGetTimespanTwoTweets() {
        Timespan timespan = Extract.getTimespan(Arrays.asList(tweet1, tweet2));
        
        assertEquals("expected start", d1, timespan.getStart());
        assertEquals("expected end", d2, timespan.getEnd());


    }
    // covers tweets.length() = 1
    //        none of tweet are similar
    @Test
    public void testGetTimespanOneTweets(){

        Timespan timespan = Extract.getTimespan(Collections.singletonList(tweet2));

        assertEquals("expected start", d2, timespan.getStart());
        assertEquals("expected end", d2, timespan.getEnd());
    }

    // covers tweets.length() > 1
    //        all tweet are similar
    @Test
    public void testGetTimespanSimilarTweets(){

        Timespan timespan = Extract.getTimespan(List.of(tweet2, tweet2));

        assertEquals("expected start", d2, timespan.getStart());
        assertEquals("expected end", d2, timespan.getEnd());
    }

    // covers tweets.length() > 1
    //        part of tweet are similar
    @Test
    public void testGetTimespanPartSimilarTweets(){

        Timespan timespan = Extract.getTimespan(List.of(tweet1,tweet2, tweet2));

        assertEquals("expected start", d1, timespan.getStart());
        assertEquals("expected end", d2, timespan.getEnd());
    }

    // covers Number of mentioned user = 0
    // valid mention: 0
    @Test
    public void testGetMentionedUsersNoMention() {
        Set<String> mentionedUsers = Extract.getMentionedUsers(Arrays.asList(tweet1));

        assertTrue("expected empty set", mentionedUsers.isEmpty());
    }

    // covers Number of mentioned user > 1
    //        tweets.length() > 1
    //        valid mention > 0
    @Test
    public void testGetMentionedUsersManyValidMention() {
        Set<String> mentionedUsers = Extract.getMentionedUsers(Arrays.asList(tweet1,tweet2,tweet3));

        assertEquals(1,mentionedUsers.size());

    }

    // covers
    //        tweets.length() > 1
    //        valid mention = 0
    @Test
    public void testGetMentionedUsersNoValidMention() {
        Set<String> mentionedUsers = Extract.getMentionedUsers(Arrays.asList(tweet1,tweet2,tweet6));

        assertTrue("expected empty set", mentionedUsers.isEmpty());
    }

    // covers
    //        tweets.length() > 1
    //        valid mention = 1
    //        same mentions but presented in full capital and small letter
    @Test
    public void testGetMentionedUsersDifferentCaseMention() {
        Set<String> mentionedUsers = Extract.getMentionedUsers(Arrays.asList(tweet1,tweet2,tweet4));

        assertEquals(mentionedUsers.size(),1);

    }

    // covers
    //        tweets.length() > 1
    //        valid mention = 0
    //        same mentions but presented in partial capital and small letter,
    @Test
    public void testGetMentionedUsersDifferentPartialCaseMention() {
        Set<String> mentionedUsers = Extract.getMentionedUsers(Arrays.asList(tweet1,tweet2,tweet5));
        assertEquals(mentionedUsers.size(),1);

    }


    // covers
    //        tweets.length() > 1
    //        valid mention = 0
    //        same mentions but presented in partial capital and small letter,
    @Test
    public void testGetMentionedUsersManyMention() {
        Set<String> mentionedUsers = Extract.getMentionedUsers(Arrays.asList(tweet3,tweet4,tweet5,tweet6));
        assertEquals(2,mentionedUsers.size());

    }


    /*
     * Warning: all the tests you write here must be runnable against any
     * Extract class that follows the spec. It will be run against several staff
     * implementations of Extract, which will be done by overwriting
     * (temporarily) your version of Extract with the staff's version.
     * DO NOT strengthen the spec of Extract or its methods.
     * 
     * In particular, your test cases must not call helper methods of your own
     * that you have put in Extract, because that means you're testing a
     * stronger spec than Extract says. If you need such helper methods, define
     * them in a different class. If you only need them in this test class, then
     * keep them in this test class.
     */

}
