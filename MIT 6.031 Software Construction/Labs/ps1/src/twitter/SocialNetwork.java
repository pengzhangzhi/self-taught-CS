/* Copyright (c) 2007-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package twitter;

import com.sun.source.doctree.SummaryTree;
import org.jetbrains.annotations.NotNull;

import java.lang.reflect.Array;
import java.util.*;

/**
 * SocialNetwork provides methods that operate on a social network.
 * 
 * A social network is represented by a Map<String, Set<String>> where map[A] is
 * the set of people that person A follows on Twitter, and all people are
 * represented by their Twitter usernames. Users can't follow themselves. If A
 * doesn't follow anybody, then map[A] may be the empty set, or A may not even exist
 * as a key in the map; this is true even if A is followed by other people in the network.
 * Twitter usernames are not case sensitive, so "ernie" is the same as "ERNie".
 * A username should appear at most once as a key in the map or in any given
 * map[A] set.
 * 
 * DO NOT change the method signatures and specifications of these methods, but
 * you should implement their method bodies, and you may add new public or
 * private methods or classes if you like.
 */
public class SocialNetwork {

    /**
     * Guess who might follow whom, from evidence found in tweets.
     * 
     * @param tweets
     *            a list of tweets providing the evidence, not modified by this
     *            method.
     * @return a social network (as defined above) in which Ernie follows Bert
     *         if and only if there is evidence for it in the given list of
     *         tweets.
     *         One kind of evidence that Ernie follows Bert is if Ernie
     *         @-mentions Bert in a tweet. This must be implemented. Other kinds
     *         of evidence may be used at the implementor's discretion.
     *         All the Twitter usernames in the returned social network must be
     *         either authors or @-mentions in the list of tweets.
     */
    public static Map<String, Set<String>> guessFollowsGraph(List<Tweet> tweets) {
        Map<String, Set<String>> socialMap = new HashMap<>();
        Map<String, List<Tweet>> author2Tweets = groupTweetsByAuthor(tweets);
        for(String author:author2Tweets.keySet()){
            author = author.toLowerCase();
            Set<String> followingUsers = Extract.getMentionedUsers(author2Tweets.get(author));
            if (!followingUsers.isEmpty()){
                socialMap.put(author,followingUsers);
            }

        }
        return socialMap;
    }

    /**
     * groupTweetsByAuthor tweets by its author.
     *
     * @param tweets
     *            a list of tweets providing the evidence, not modified by this
     *            method.
     * @return a map where key denotes author, and the corresponding value refers to the tweets that the author posts.
     */
    private static Map<String, List<Tweet>> groupTweetsByAuthor(List<Tweet> tweets) {
        Map<String, List<Tweet>> author2Tweet= new HashMap<>();
        for(Tweet tweet:tweets){
            String author = tweet.getAuthor().toLowerCase();
            if(!author2Tweet.containsKey(author)){
                List<Tweet> values = new ArrayList<>();
                values.add(tweet);
                author2Tweet.put(author,values);
            }
            else{
                author2Tweet.get(author).add(tweet);
            }
        }
        return author2Tweet;
    }

    /**
     * Find the people in a social network who have the greatest influence, in
     * the sense that they have the most followers.
     * 
     * @param followsGraph
     *            a social network (as defined above)
     * @return a list of all distinct Twitter usernames in followsGraph, in
     *         descending order of follower count.
     */
    public static List<String> influencers(Map<String, Set<String>> followsGraph) {
        /*
        * 1. construct graph (transforming linked-list graph to correlation matrix)
        * 2. inverse graphs ( Diagonal symmetric value set to 1)
        * 3. derive the follower graphs in linked list format.
        * 4. calculate the number of followers
        * 5. sort.
        * 6. return result.
        * */
        Set<String> nodesSet = new HashSet<>(followsGraph.keySet());
        for(var authorSet: followsGraph.values()){
            nodesSet.addAll(authorSet);
        }
        int matrixLength = nodesSet.size();
        int [][] followingMatrix = new int[matrixLength][matrixLength];
        List<String> nodesList = new ArrayList<>(nodesSet);
        Map<String, Integer> author2index = new HashMap<>();
        for (int i = 0; i < matrixLength; i++) {
            author2index.put(nodesList.get(i),i);
        }
        for(String author:followsGraph.keySet()){
            int authorIndex = author2index.get(author);
            List<String> followingUsers = new ArrayList<>(followsGraph.get(author));
            for (int i = 0; i < followingUsers.size(); i++) {
                String followedAuthorName = followingUsers.get(i);
                int followedAuthorIndex = author2index.get(followedAuthorName);
                followingMatrix[authorIndex][followedAuthorIndex] = 1;
            }
        }
        int [][] followerMatrix = new int[matrixLength][matrixLength];
        for (int i = 0; i <matrixLength; i++) {
            for (int j = 0; j < matrixLength; j++) {
                if(followingMatrix[i][j] == 1){
                    assert i!=j: "the Diagonal value must be false. ";
                    followerMatrix[j][i] = 1;
                }

            }
        }

        List<User> users = new ArrayList<>();
        for (int i = 0; i <matrixLength; i++) {
            int sum = 0;
            String author = nodesList.get(i);
            for (int j = 0; j < matrixLength; j++) {
                if(followerMatrix[i][j] == 1){
                    assert i!=j: "the Diagonal value must be false. A person is not counted as his follower!";
                    sum += 1;
                }
            }
            if(sum != 0){
                users.add(new User(author,sum));
            }
        }
        users.sort(new Comparator<User>() {
            @Override
            public int compare(User user, User t1) {
                return t1.getNumberOfFollower() - user.getNumberOfFollower();
            }
        });
        List<String> userListAscending = new ArrayList<>();
        for(var user:users){
            userListAscending.add(user.getName());
        }
        return userListAscending;
    }

}

/**
 * this is a helper class used for sorting the tweets users by its number of followers.
 *
 *
 */
class User implements Comparator<User>{
    private String name;
    private int numberOfFollower;
    User(String name,int numberOfFollower){
        this.name = name;
        this.numberOfFollower = numberOfFollower;
    }

    @Override
    public int compare(User user, User t1) {
        return user.numberOfFollower - t1.numberOfFollower;
    }
    public String getName(){
        return this.name;
    }
    public int getNumberOfFollower(){
        return this.numberOfFollower;
    }
}