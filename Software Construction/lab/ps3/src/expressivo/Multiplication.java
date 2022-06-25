package expressivo;

import java.util.Objects;

public class Multiplication implements Expression {
    /**
     * AF:
     *      AF(leftExpression, rightExpression) = leftExpression * rightExpression
     * RI:
     *      * leftExpression  and rightExpression are instance of Expression.
     *      *
     *      * Rep Exposure:
     *      *      the leftExpression and rightExpression are immutable.
     *      *
     *      *
     *
    * */
    private final Expression leftExpression;
    private final Expression rightExpression;

    public Multiplication(Expression leftExpression, Expression rightExpression) {
        this.leftExpression = leftExpression;
        this.rightExpression = rightExpression;
    }
    private void checkRep(){
        assert (leftExpression != null);
        assert (rightExpression != null);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) {
            return true;
        }
        if (!(o instanceof Multiplication)) {
            return false;
        }
        Multiplication multiplication = (Multiplication) o;
        return Objects.equals(leftExpression, multiplication.leftExpression) &&
                Objects.equals(rightExpression, multiplication.rightExpression);
    }

    @Override
    public int hashCode() {
        return Objects.hash(leftExpression, rightExpression) ;
    }

    @Override
    public String toString() {
        return leftExpression.toString()+" * "+rightExpression.toString();
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
        return new Addition(new Multiplication(leftExpression.differentiate(var),rightExpression),
                            new Multiplication(leftExpression,rightExpression.differentiate(var)));

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
        return new Multiplication(leftExpression.simplify(var,value),rightExpression.simplify(var,value));
    }
}
