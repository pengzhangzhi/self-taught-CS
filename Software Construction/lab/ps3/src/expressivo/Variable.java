package expressivo;

import org.hamcrest.SelfDescribing;

import java.util.Objects;

public class Variable implements Expression {
    /**
     * AF:
     * AF(varname) = a variable in the name of varname.
     * RI:
     * the varname must be a single letter, and case-sensitive.
     *
     *
    * */
    private final char variable;

    public Variable(char varname) {
        this.variable = varname;
    }

    private void checkRep(){
        assert !Character.isDigit(variable);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Variable)) return false;
        Variable variable1 = (Variable) o;
        return variable == variable1.variable;
    }

    @Override
    public int hashCode() {
        return Objects.hash(variable);
    }

    @Override
    public String toString() {
        return String.valueOf(variable);
    }

    /**
     * differentiation operation of the expression towards the var.
     * Params:
     * var: a variable of which the expression derivative is on.
     * Returns:
     * the derivative expression
     *
     * @param var
     */
    @Override
    public Expression differentiate(Variable var) {
        if(var.equals(this.variable)){
            return new Constant(1.0);
        }
        else{
            return this;
        }
    }

    /**
     * Simplifying a expression with the variable. evaluate the expression with the variable.
     *
     * @param var
     * @param value
     * @Returns: Evaluated expression.
     */
    @Override
    public Expression simplify(Variable var, Double value) {
        if(this.equals(var)){
            return new Constant(value);
        }
        else{
            return this;
        }
    }
}
