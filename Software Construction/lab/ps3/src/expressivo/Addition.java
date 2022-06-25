package expressivo;

import org.hamcrest.core.IsInstanceOf;

import java.util.Objects;

public class Addition implements Expression {
    private final Expression leftExpression;
    private final Expression rightExpression;
    private Expression ex;

    /**
    * AF:
    * AF(leftExpression, rightExpression) = leftExpression + rightExpression,
     *
     *
    * RI:
     * leftExpression  and rightExpression are instance of Expression.
     *
     * Rep Exposure:
     *      the leftExpression and rightExpression are immutable.
     *
     *
    * */

    public Addition(Expression leftExpression, Expression rightExpression) {
        this.leftExpression = leftExpression;
        this.rightExpression = rightExpression;
    }
    private void checkRep(){
        assert (leftExpression instanceof Expression);
        assert (rightExpression instanceof Expression);
    }
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Addition)) return false;
        Addition addition = (Addition) o;
        return Objects.equals(leftExpression, addition.leftExpression) &&
                Objects.equals(rightExpression, addition.rightExpression);
    }

    @Override
    public int hashCode() {
        return Objects.hash(leftExpression, rightExpression) ;
    }

    @Override
    public String toString() {
        return leftExpression.toString()+" + "+rightExpression.toString();
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
        return new Addition(leftExpression.differentiate(var), rightExpression.differentiate(var));
    }

    /**
     * Simplifying a expression with the variable. evaluate the expression with the variable.
     *
     * @param
     *      var: the variable
     *      value: the value of the variable.
     * @Returns: Evaluated expression.
     */
    @Override
    public Expression simplify(Variable var,Double value) {
        return new Addition(leftExpression.simplify(var,value),rightExpression.simplify(var,value));

    }
}
