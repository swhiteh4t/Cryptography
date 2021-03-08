/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.module1;

import static org.junit.jupiter.api.Assertions.*;

/**
 *
 * @author svalle
 */
public class MathOperationsTest {

    public MathOperationsTest() {
    }

    @org.junit.jupiter.api.BeforeAll
    public static void setUpClass() throws Exception {
    }

    @org.junit.jupiter.api.AfterAll
    public static void tearDownClass() throws Exception {
    }

    @org.junit.jupiter.api.BeforeEach
    public void setUp() throws Exception {
    }

    @org.junit.jupiter.api.AfterEach
    public void tearDown() throws Exception {
    }

    /**
     * Test of xor method, of class MathOperations.
     */
    @org.junit.jupiter.api.Test
    public void testXor() {
        System.out.println("xor");

        assertEquals('0', MathOperations.xor('0', '0'));
        assertEquals('1', MathOperations.xor('1', '0'));
        assertEquals('1', MathOperations.xor('0', '1'));
        assertEquals('0', MathOperations.xor('1', '1'));
    }

    /**
     * Test of and method, of class MathOperations.
     */
    @org.junit.jupiter.api.Test
    public void testAnd() {
        System.out.println("and");

        assertEquals('0', MathOperations.and('0', '0'));
        assertEquals('0', MathOperations.and('1', '0'));
        assertEquals('0', MathOperations.and('0', '1'));
        assertEquals('1', MathOperations.and('1', '1'));
      
    }

    /**
     * Test of or method, of class MathOperations.
     */
    @org.junit.jupiter.api.Test
    public void testOr() {
        System.out.println("or");
        assertEquals('0', MathOperations.or('0', '0'));
        assertEquals('1', MathOperations.or('1', '0'));
        assertEquals('1', MathOperations.or('0', '1'));
        assertEquals('1', MathOperations.or('1', '1'));
       
    }

    /**
     * Test of adjustSize method, of class MathOperations.
     */
    @org.junit.jupiter.api.Test
    public void testAdjustSize() {
        System.out.println("adjustSize");
        String str = "123456";
        int len = 10;
        String expResult = "0000123456";
        String result = MathOperations.adjustSize(str, len);
        assertEquals(expResult, result);
        
    }

    /**
     * Test of add method, of class MathOperations.
     */
    @org.junit.jupiter.api.Test
    public void testAdd() {
        System.out.println("add");
 
        assertEquals("10100000", MathOperations.add("1010100", "1001100"));
        assertEquals("1010000", MathOperations.add("100100", "101100"));
        assertEquals("1101001", MathOperations.add("1100", "1011101"));
        assertEquals("100000", MathOperations.add("1001", "10111"));
        assertEquals("1101101", MathOperations.add("1000111", "100110"));
        assertEquals("1111010", MathOperations.add("1000100", "110110"));
        assertEquals("1110011", MathOperations.add("1000100", "101111"));
        assertEquals("10011100", MathOperations.add("1010001", "1001011"));
        assertEquals("10000111", MathOperations.add("1000100", "1000011"));
        assertEquals("1000110", MathOperations.add("111110", "1000"));
        assertEquals("10110010", MathOperations.add("1100011", "1001111"));
        assertEquals("1011100", MathOperations.add("101111", "101101"));
        assertEquals("1111000", MathOperations.add("1010011", "100101"));
        assertEquals("1000011", MathOperations.add("11011", "101000"));
        assertEquals("10100110", MathOperations.add("1000101", "1100001"));
        assertEquals("10001011", MathOperations.add("110100", "1010111"));
        assertEquals("110101", MathOperations.add("110000", "101"));
        assertEquals("1111100", MathOperations.add("101100", "1010000"));
        assertEquals("1010100", MathOperations.add("111010", "11010"));
        assertEquals("110001", MathOperations.add("10001", "100000"));

    }

    /**
     * Test of multiply method, of class MathOperations.
     */
    @org.junit.jupiter.api.Test
    public void testMultiply() {
        System.out.println("multiply");
        assertEquals("1110110", MathOperations.multiply("111011", "10"));
        assertEquals("10001011100", MathOperations.multiply("1100", "1011101"));
        assertEquals("110101100110", MathOperations.multiply("1100010", "100011"));
        assertEquals("101110110101", MathOperations.multiply("100101", "1010001"));
        assertEquals("110110010", MathOperations.multiply("111", "111110"));
        assertEquals("1010000001101", MathOperations.multiply("1010111", "111011"));
        assertEquals("1000011100", MathOperations.multiply("111100", "1001"));
        assertEquals("11000100111", MathOperations.multiply("101101", "100011"));
        assertEquals("1110100100110", MathOperations.multiply("1010010", "1011011"));
        assertEquals("1001111101100", MathOperations.multiply("1010101", "111100"));
        assertEquals("10110100", MathOperations.multiply("1100", "1111"));
        assertEquals("1111011100", MathOperations.multiply("11010", "100110"));
        assertEquals("110100010100", MathOperations.multiply("1011101", "100100"));
        assertEquals("1100100111100", MathOperations.multiply("1011111", "1000100"));
        assertEquals("1001000000", MathOperations.multiply("1001000", "1000"));
        assertEquals("11110000100", MathOperations.multiply("110100", "100101"));
        assertEquals("100111011000", MathOperations.multiply("111111", "101000"));
        assertEquals("11101010000", MathOperations.multiply("110100", "100100"));
        assertEquals("1000001", MathOperations.multiply("1", "1000001"));
        assertEquals("1011010000", MathOperations.multiply("11110", "11000"));
        
    }



}
