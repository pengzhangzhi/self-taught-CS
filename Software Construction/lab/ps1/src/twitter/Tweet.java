/* Copyright (c) 2007-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package twitter;

import java.time.Instant;

/**
 * This immutable datatype represents a tweet from Twitter.
 * 
 * DO NOT CHANGE THIS CLASS.
 */
public class Tweet {

    private final long id;
    private final String author;
    private final String text;
    private final Instant timestamp;
    /* Rep invariant: 
     *    author.length > 0
     *    all characters in author are drawn from {A..Z, a..z, 0..9, _, -}
     *    text.length <= 140
     */
    
    /**
     * Make a Tweet with a known unique id.
     * 
     * @param id
     *            unique identifier for the tweet, as assigned by Twitter.
     * @param author
     *            Twitter username who wrote this tweet.  
     *            Required to be a Twitter username as defined by getAuthor() below.
     * @param text
     *            text of the tweet, at most 140 characters.
     * @param timestamp
     *            date/time when the tweet was sent.
     */
    public Tweet(final long id, final String author, final String text, final Instant timestamp) {
        this.id = id;
        this.author = author;
        this.text = text;
        this.timestamp = timestamp;
    }

    /**
     * @return unique identifier of this tweet
     */
    public long getId() {
        return id;
    }

    /**
     * @return Twitter username who wrote this tweet.
     *         A Twitter username is a nonempty sequence of letters (A-Z or
     *         a-z), digits, underscore ("_"), or hyphen ("-").
     *         Twitter usernames are case-insensitive, so "jbieber" and "JBieBer"
     *         are equivalent.
     */
    public String getAuthor() {
        return author;
    }

    /**
     * @return text of this tweet, at most 140 characters
     */
    public String getText() {
        return text;
    }

    /**
     * @return date/time when this tweet was sent
     */
    public Instant getTimestamp() {
        return timestamp;
    }

    /*
     * @see Object.toString()
     */
    @Override public String toString() {
        return "(" + this.getId()
                + " " + this.getTimestamp().toString()
                + " " + this.getAuthor()
                + ") " + this.getText();
    }

    /*
     * @see Object.equals()
     */
    @Override public boolean equals(Object thatObject) {
        if (!(thatObject instanceof Tweet)) {
            return false;
        }

        Tweet that = (Tweet) thatObject;
        return this.id == that.id;
    }

    /*
     * @see Object.hashCode()
     */
    @Override public int hashCode() {
        final int bitsInInt = 32;
        final int lower32bits = (int) id;
        final int upper32bits = (int) (id >> bitsInInt);
        return lower32bits ^ upper32bits;
    }
}
