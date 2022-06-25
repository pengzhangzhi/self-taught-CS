/* Copyright (c) 2015-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package expressivo;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.HashMap;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Optional;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Console interface to the expression system.
 * 
 * <p>PS3 instructions: you are free to change this user interface class.
 */
public class Main {
    
    
    /**
     * Read expression and command inputs from the console and output results.
     * An empty input terminates the program.
     * @param args unused
     * @throws IOException if there is an error reading the input
     */
    public static void main(String[] args) throws IOException {
        final BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
        Optional<String> currentExpression = Optional.empty();
        
        while (true) {
            System.out.print("> ");
            final String input = in.readLine();
            
            if (input.isEmpty()) {
                return; // exits the program
            }
            
            try {
                final String output;
                
                if (input.startsWith(DIFFERENTIATE_PREFIX)) {
                    final String variable = parseDifferentiate(input);
                    output = Commands.differentiate(currentExpression.get(), variable);
                    currentExpression = Optional.of(output);
                } else if (input.startsWith(SIMPLIFY_PREFIX)) {
                    final Map<String,Double> environment = parseSimpify(input);
                    output = Commands.simplify(currentExpression.get(), environment);
                    // ... but don't change currentExpression
                } else {
                    final Expression expression = Expression.parse(input);
                    output = expression.toString();
                    currentExpression = Optional.of(output);
                }
                
                System.out.println(output);
            } catch (NoSuchElementException nse) {
                // currentExpression was empty
                System.out.println("must enter an expression before using this command");
            } catch (RuntimeException re) {
                System.out.println(re.getClass().getName() + ": " + re.getMessage());
            }
        }
    }
 
    private static final String DIFFERENTIATE_PREFIX = "!d/d";
    private static final String VARIABLE = "[A-Za-z]+";
    private static final String DIFFERENTIATE = DIFFERENTIATE_PREFIX + "(" + VARIABLE + ") *";

    private static String parseDifferentiate(final String input) {
        final Matcher commandMatcher = Pattern.compile(DIFFERENTIATE).matcher(input);
        if (!commandMatcher.matches()) {
            throw new CommandSyntaxException("usage: !d/d must be followed by a variable name");
        }

        final String variable = commandMatcher.group(1);
        return variable;
    }
    
    private static final String SIMPLIFY_PREFIX = "!simplify";
    private static final String ASSIGNMENT = "(" + VARIABLE + ") *= *([^ ]+)";
    private static final String SIMPLIFY = SIMPLIFY_PREFIX + "( +" + ASSIGNMENT + ")* *";    

    private static Map<String,Double> parseSimpify(final String input) {
        final Matcher commandMatcher = Pattern.compile(SIMPLIFY).matcher(input);
        if (!commandMatcher.matches()) {
            throw new CommandSyntaxException("usage: !simplify var1=val1 var2=val2 ...");
        }
        
        final Map<String,Double> environment = new HashMap<>();
        final Matcher argumentMatcher = Pattern.compile(ASSIGNMENT).matcher(input);
        while (argumentMatcher.find()) {
            final String variable = argumentMatcher.group(1);
            final double value = Double.valueOf(argumentMatcher.group(2));
            environment.put(variable, value);
        }

        // un-comment the following line to print the environment after each !simplify command
        //System.out.println(environment);
        return environment;
    }
    
    public static class CommandSyntaxException extends RuntimeException {
        private static final long serialVersionUID = 1;
        public CommandSyntaxException(String message) {
            super(message);
        }
    }
    
}
