/* Copyright (c) 2007-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package twitter;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.net.URL;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

import javax.json.Json;
import javax.json.JsonArray;
import javax.json.JsonException;
import javax.json.JsonNumber;
import javax.json.JsonObject;
import javax.json.JsonReader;
import javax.json.JsonString;
import javax.json.JsonValue;

/**
 * Read tweets from files or from a web server. Uses a simplified representation
 * for tweets (with fewer fields than the Twitter API).
 * 
 * DO NOT CHANGE THIS CLASS.
 */
public class TweetReader {
    
    /**
     * Get a list of tweets from a web server.
     * 
     * @param url URL of server to retrieve tweets from
     * @return a list of tweets retrieved from the server.
     * @throws IOException if the url is invalid, the server is unreachable,
     *                     or some other network-related error occurs.
     */
    public static List<Tweet> readTweetsFromWeb(URL url) throws IOException {
        return readTweets(new InputStreamReader(url.openStream()));
    }
    
    /*
     * Read a list of tweets from a stream.
     * 
     * @return a list of tweets parsed out of the stream.
     */
    private static List<Tweet> readTweets(Reader reader) {
        JsonReader jsonReader = Json.createReader(reader);
        JsonArray array = jsonReader.readArray();
        ArrayList<Tweet> tweetList = new ArrayList<Tweet>();
        for (int i = 0; i < array.size(); i++) {
            Map<String, Object> map = constructTweetMap(array.get(i), null);
            tweetList.add(createTweetFromMap(map));
        }
        return tweetList;
    }
    
    /*
     * Crawl recursively through the JSON tree representing a single tweet.
     * 
     * @return a map that maps key paths (like "id" and "user.screen_name") to values.
     */
    private static Map<String, Object> constructTweetMap(JsonValue tree, String key) {
        Map<String, Object> tweetMap = new HashMap<String, Object>();
        switch (tree.getValueType()) {
        case OBJECT:
            JsonObject object = (JsonObject) tree;
            Map<String, Object> subMap = new HashMap<String, Object>();
            for (String name : object.keySet()) {
                subMap.putAll(constructTweetMap(object.get(name), name));
            }
            if (key == null) {
                tweetMap.putAll(subMap);
            } else {
                tweetMap.put(key, subMap);
            }
            break;
        case ARRAY:
            JsonArray array = (JsonArray) tree;
            for (JsonValue val : array)
                tweetMap.putAll(constructTweetMap(val, null));
            break;
        case STRING:
            JsonString st = (JsonString) tree;
            tweetMap.put(key, st.getString());
            break;
        case NUMBER:
            JsonNumber num = (JsonNumber) tree;
            tweetMap.put(key, num.toString());
            break;
        case TRUE:
        case FALSE:
        case NULL:
            tweetMap.put(key, tree.getValueType().toString());
            break;
        default:
            throw new JsonException("Unexpected value type " + tree.getValueType());
        }
        
        return tweetMap;
    }
    
    /*
     * Construct a Tweet from a map of (key,value) pairs parsed from JSON.
     */
    private static Tweet createTweetFromMap(Map<String, Object> tweetMap) {
        // make the Tweet
        Long id = Long.valueOf(tweetMap.get("id").toString());
        String screenName = tweetMap.get("user.screen_name").toString();
        String text = tweetMap.get("text").toString();
        ZonedDateTime timestamp = ZonedDateTime.parse(tweetMap.get("created_at").toString(),
                                                      DateTimeFormatter.ofPattern("EEE MMM dd HH:mm:ss Z yyyy", Locale.US));
        return new Tweet(id, screenName, text, timestamp.toInstant());
    }
}
