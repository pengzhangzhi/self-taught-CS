package abc.sound;

/**
 * Pitch is an immutable type representing the frequency of a musical note.
 * Standard music notation represents pitches by letters: A, B, C, ..., G.
 * Pitches can be sharp or flat, or whole octaves up or down from these
 * primitive generators.
 * 
 * <p> For example:
 * <br> new Pitch('C') makes middle C
 * <br> new Pitch('C').transpose(1) makes C-sharp
 * <br> new Pitch('E').transpose(-1) makes E-flat
 * <br> new Pitch('C').transpose(OCTAVE) makes high C
 * <br> new Pitch('C').transpose(-OCTAVE) makes low C
 */
public class Pitch {

    private final int value;

    /*
     * Rep invariant: true.
     *
     * Abstraction function AF(value): 
     *   AF(0),...,AF(12) map to middle C, C-sharp, D, ..., A, A-sharp, B.
     *   AF(i+12n) maps to n octaves above middle AF(i)
     *   AF(i-12n) maps to n octaves below middle AF(i)
     */

    private static final int[] SCALE = {
        9,  // A
        11, // B
        0,  // C
        2,  // D
        4,  // E
        5,  // F
        7,  // G
    };

    private static final String[] VALUE_TO_STRING = {
            "C", "^C", "D", "^D", "E", "F", "^F", "G", "^G", "A", "^A", "B"
    };

    /**
     * Middle C.
     */
    public static final Pitch MIDDLE_C = new Pitch('C');
    
    /**
     * Number of pitches in an octave.
     */
    public static final int OCTAVE = 12;
    
    private Pitch(int value) {
        this.value = value;
    }

    /**
     * Make a Pitch named c in the middle octave of the piano keyboard.
     * For example, new Pitch('C') constructs middle C.
     * @param c letter in {'A',...,'G'}
     */
    public Pitch(char c) {
        try {
            value = SCALE[c-'A'];
        } catch (ArrayIndexOutOfBoundsException aioobe) {
            throw new IllegalArgumentException(c + " must be in the range A-G");
        }
    }

    /**
     * @return pitch made by transposing this pitch by semitonesUp semitones;
     *         for example, middle C transposed by 12 semitones is high C, and
     *         E transposed by -1 semitones is E flat
     */
    public Pitch transpose(int semitonesUp) {
        return new Pitch(value + semitonesUp);
    }

    /**
     * @return number of semitones between this and that; i.e., n such that
     *         that.transpose(n).equals(this)
     */
    public int difference(Pitch that) {
        return this.value - that.value;
    }

    /**
     * @return true iff this pitch is lower than that pitch
     */
    public boolean lessThan(Pitch that) {
        return this.difference(that) < 0;
    }

    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null) return false;
        if (obj.getClass() != this.getClass()) return false;
        
        Pitch that = (Pitch) obj;
        return this.value == that.value;
    }

    @Override
    public int hashCode() {
        return value;
    }


    /**
     * @return the MIDI note of this pitch
     */
    public int toMidiNote() {
        return value + 60;
    }

    /**
     * @return this pitch in abc music notation
     * @see http://www.walshaw.plus.com/abc/examples/
     */
    @Override
    public String toString() {
        String suffix = "";
        int v = value;

        while (v < 0) {
            suffix += ",";
            v += 12;
        }

        while (v >= 12) {
            suffix += "'";
            v -= 12;
        }

        return VALUE_TO_STRING[v] + suffix;
    }
}
