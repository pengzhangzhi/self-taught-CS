/* Copyright (c) 2015-2016 MIT 6.005 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
package expressivo;

import static org.junit.Assert.*;
import org.junit.Test;

import java.util.function.Consumer;

/**
 * Tests for the Expression abstract data type.
 */
public class ExpressionTest {

    // Testing strategy
    /**
     * for each Expression class, we test the four methods.:
     * 1. constructor()
     * 2. tostring()
     * 3. hashcode()
     * 4. equals()
     *
     * for constants and variable, the tests strategies are:
     *  constants:
     *      double, and integer
     *  variable:
     *      'x', 'xy'(invalid)
     *
     * for addition and multiplication, the test strategies are split as follows:
     *
     * two constants,
     * two variables,
     * two multiplications,
     * two additions,
     * addition and multiplication
     * variable and addition
     *
     *
     *
     * */
    
    @Test(expected=AssertionError.class)
    public void testAssertionsEnabled() {
        assert false; // make sure assertions are enabled with VM argument: -ea
    }
    @Test
    public void testConstant(){
        Constant constantInt = new Constant((double) 1);
        Constant constantDouble = new Constant(1.2);
        System.out.println(constantDouble);
        System.out.println(constantInt);
        assertNotEquals(constantDouble,constantInt);
        assertNotEquals(constantDouble.hashCode(),constantInt.hashCode());

    }

    /**
     *
     * * for addition and multiplication, the test strategies are split as follows:
     *      *
     *      * two constants,
     *      * two variables,
     *      * two multiplications,
     *      * two additions,
     *      * addition and multiplication
     *      * variable and addition
     * */
    @Test
    public void testAddition(){
        Constant constant = new Constant(1.2);
        Variable variable = new Variable('x');
        Addition additionConstVar = new Addition(constant, variable);
        Addition addVarConst = new Addition(variable, constant);
        Multiplication mul1 = new Multiplication(constant,variable);
        Multiplication mul2 = new Multiplication(variable,constant);
        Addition addConstAdd = new Addition(constant,addVarConst);
        Constant constantInt = new Constant((double) 1);
        Addition doubleAdd = new Addition(addConstAdd,addVarConst);
        Addition doubleMul = new Addition(mul1,mul2);
        testAdditionOrder(additionConstVar,addVarConst);
        testAdditionOrder(addConstAdd,additionConstVar);
        testAdditionOrder(doubleAdd,doubleMul);
    }


    public void testAdditionOrder(Addition left, Addition right){
        Addition addition = new Addition(left,right);
        Addition add2 = new Addition(right, left);
        helpTestAdditionNotEqual(add2,addition);
    }

    public void helpTestAdditionNotEqual(Addition add1,Addition add2){
        assertNotEquals(add1,add2);
        assertNotEquals(add1.hashCode(),add2.hashCode());
        System.out.println(add1);
        System.out.println(add2);
        assertNotEquals(add1.toString(),add2.toString());
    }

    @Test
    public void testMultiplication(){
        Constant constant = new Constant(1.2);
        Variable variable = new Variable('x');
        Addition additionConstVar = new Addition(constant, variable);
        Addition addVarConst = new Addition(variable, constant);
        Multiplication mul1 = new Multiplication(constant,variable);
        Multiplication mul2 = new Multiplication(variable,constant);
        Addition addConstAdd = new Addition(constant,addVarConst);
        Constant constantInt = new Constant((double) 1);
        Addition doubleAdd = new Addition(addConstAdd,addVarConst);
        Addition doubleMul = new Addition(mul1,mul2);
        Multiplication mul3 = new Multiplication(mul2, doubleMul);
        assertNotEquals(mul2,mul1);
        assertNotEquals(mul2,mul3);
        assertNotEquals(mul2.hashCode(),mul1.hashCode());
        System.out.println(mul2);
        System.out.println(mul1);
        System.out.println(mul3);
    }

    @Test
    public void testVariable(){
        Variable variable = new Variable('x');
        Variable varX = new Variable('X');
        assertNotEquals(variable,varX);
        assertNotEquals(variable.hashCode(),varX.hashCode());
        System.out.println(variable);
        System.out.println(variable.hashCode());
    }




    // TODO tests for Expression
    
}
