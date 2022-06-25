grammar Configuration;

// This puts a package statement at the top of the output Java files.
@header {
package abc.parser;
// Do not edit this .java file! Edit the .g4 file and re-run Antlr.
}

// This adds code to the generated parser.
@members {
    // This method makes the parser stop running if it encounters
    // invalid input and throw a RuntimeException.
    public void reportErrorsAsExceptions() {
        // To prevent any reports to standard error, add this line:
        //removeErrorListeners();
        
        addErrorListener(new BaseErrorListener() {
            public void syntaxError(Recognizer<?, ?> recognizer,
                                    Object offendingSymbol, 
                                    int line, int charPositionInLine,
                                    String msg, RecognitionException e) {
                throw new ParseCancellationException(msg, e);
            }
        });
    }
}
