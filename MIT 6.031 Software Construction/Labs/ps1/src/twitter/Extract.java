/* Copyright (c) 2007-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package twitter;

import org.jetbrains.annotations.NotNull;

import javax.accessibility.AccessibleText;
import java.time.Instant;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


/**
 * Extract consists of methods that extract information from a list of tweets.
 * 
 * DO NOT change the method signatures and specifications of these methods, but
 * you should implement their method bodies, and you may add new public or
 * private methods or classes if you like.
 */
public class Extract {

    /**
     * Get the time period spanned by tweets.
     * 
     * @param tweets
     *            list of tweets with distinct ids, not modified by this method.
     * @return a minimum-length time interval that contains the timestamp of
     *         every tweet in the list.
     */
    public static Timespan getTimespan(List<Tweet> tweets) {
        Instant minimalTimeInstant = tweets.get(0).getTimestamp();
        Instant maximalTimeInstant = tweets.get(0).getTimestamp();
            for(Tweet tweet : tweets){
                Instant timeInstant = tweet.getTimestamp();
                if (timeInstant.compareTo(minimalTimeInstant) < 0){
                    minimalTimeInstant = timeInstant;
                }
                if (timeInstant.compareTo(maximalTimeInstant) > 0){
                    maximalTimeInstant = timeInstant;
                }
            }
        return new Timespan(minimalTimeInstant,maximalTimeInstant);
    }

    /**
     * Get usernames mentioned in a list of tweets.
     * 
     * @param tweets
     *            list of tweets with distinct ids, not modified by this method.
     * @return the set of usernames who are mentioned in the text of the tweets.
     *         A username-mention is "@" followed by a Twitter username (as
     *         defined by Tweet.getAuthor()'s spec).
     *         The username-mention cannot be immediately preceded or followed by any
     *         character valid in a Twitter username.
     *         For this reason, an email address like bitdiddle@mit.edu does NOT 
     *         contain a mention of the username mit.
     *         Twitter usernames are case-insensitive, and the returned set may
     *         include a username at most once.
     */
    @NotNull
    public static Set<String> getMentionedUsers(List<Tweet> tweets) {

        Set<String> mentionedUsers = new HashSet<>();
        for(Tweet tweet : tweets){
            String text = tweet.getText();
            List<String> atGroups = getAtSubString(text);

            for(String atString:atGroups){
                boolean containSpacial = false;
                char[] specialChars = new char[]{'.', '*', '/', '+', '-'};
                for(char spatialCharacter : specialChars){
                    // find spatial character
                    if(atString.indexOf(spatialCharacter) != -1){
                        containSpacial = true;
                        break;
                    }

                }
                if(!containSpacial){
                    atString = atString.toLowerCase();
                    mentionedUsers.add(atString.substring(atString.indexOf("@")+1).trim());
                }

            }


        }
        return mentionedUsers;
    }

    private static List<String> getAtSubString(String text) {
        Pattern pat = Pattern.compile("@[A-Za-z0-9]+.");
        Matcher mat = pat.matcher(text);
        List<String> atGroups = new ArrayList<>();
        while(mat.find()){
            atGroups.add(mat.group(0));
        }
        return atGroups;
    }

}
