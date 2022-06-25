package expressivo;

public class Constant implements Expression {
    private final Double value;

    /**
     * AF:
     * AF(non-negative number) = a non-negative number, e.g., 1, 1.2
     * RI:
     *  non-negative numbers, ranging from 0 to max double value.
     *  Rep Exposure:
     *  all filed are immutable.
     *
     */
    public Constant(Double value) {
        this.value = value;
    }
    private void checkRep(){
        assert this.value > 0;
    }
    public static Expression parse(String input) throws Exception {
        throw new Exception("not implemented!");
    }

    @Override
    public int hashCode() {
        int result = 43;
        long c = Double.doubleToLongBits(value);
        return 37*result + (int)(c&(c>>>32));
    }


    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (!(obj instanceof Variable)) return false;
        return (double)obj == value;
    }

    @Override
    public String toString() {
        return String.valueOf(this.value);
    }


    @Override
    public Expression differentiate(Variable var) {
        return new Constant(0.0);
    }

    /**
     * Simplifying a expression with the variable. evaluate the expression with the variable.
     *
     * @param var
     * @param value
     * @Returns: Evaluated expression.
     */
    @Override
    public Expression simplify(Variable var, double value) {

        return this;

    }
}
