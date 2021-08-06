/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.module1;

import com.google.common.base.Strings;
import java.util.ArrayList;

/**
 *
 * @author svalle
 */
public class MathOperations {
    
    public static char xor(char a, char b){
        if ( a != b ) return '1' ;
        else return '0' ;
    }

    public static char and(char a, char b){
        if ( a == '1' && b == '1') return '1' ;
        else return '0';
    }

    public static char or(char a, char b){
        if ( a == '1' || b == '1') return '1' ;
        else return '0';
    }
    
  public static String adjustSize(String str, int len ){
        
        return new String(Strings.padStart(str, len, '0')) ;
    }

    
      public static String add( String a, String b ){
        String result = new String();  // To store the sum bits

        a = adjustSize(a, b.length());
        b = adjustSize(b,a.length());

        int length = a.length() > b.length() ? a.length(): b.length() ;
        char carry = '0';  // Initialize carry
        for (int i = length-1 ; i >= 0 ; i--){
            char sum = xor(xor(a.charAt(i),b.charAt(i)),carry);
            result = String.valueOf(sum+result);
            carry = or(or(and(a.charAt(i),b.charAt(i)),and(b.charAt(i),carry)), and(a.charAt(i),carry));
        }
        // if overflow, then add a leading 1
        if (carry == '1')  result = new String('1' + result);
        return new String(result);
    }
        private static String invert(String binStr){
            char[] rtn = new char[binStr.length()];
            for ( int i = 0 ; i < rtn.length ; i++ ) rtn[i] = binStr.charAt(i) == '1' ? '0' : '1';
            return new String(String.valueOf(rtn));
    }
     
        private static String subtract (String s1, String s2){
        return new String(add(s1,add("1",invert(s2))).substring(1));
        }
     
        private static String shiftL(String a, int n){
        String add = new String(a);

        for ( int i = 0 ; i < n ; i++ ) add = add.concat("0");
        return new String(add) ;
    }
    
       public static String multiply(String a, String b){
        String result = new String();
        int j = 0 ;
        for ( int i = b.length()-1 ; i > -1 ; i-- ){
            // If encountered a 1, then shift i amount of times and add to sum
            if ( b.charAt(i) == '1' ){
                result = add(shiftL(a,b.length()-i-1),result);
            }
        }
        return new String(result) ;
    }
        
        
     public static String karatsuba(String a, String b){    
        int max = a.length() > b.length() ? a.length() : b.length() ;
        if ( a.length() <= max || b.length() <= max ){
            return multiply(a,b);
        }
        int m = a.length() > b.length() ? a.length() : b.length() ;
        m = m/2;  //floor(m/2)

        //Divide in halves the sequences
        String aRight = a.substring(0,m);
        String aLeft = a.substring(m,a.length());

        String bRight = b.substring(0,m);
        String bLeft = b.substring(m,b.length());

        //Use the recursion in the divided parts
        String p0 = karatsuba(aLeft,bLeft);
        String p1 = karatsuba(add(aRight,bRight), add(aLeft,bLeft));
        String p2 = karatsuba(aRight, bRight);

        return add( shiftL(p2,2*m), add( shiftL(subtract(p1,add(p2,p0)),m),p0));
    }
     private static final int[] divisionUsingShift(int a, int b) {
        int dividend = a;
        int divisor = b;
        int tempA, tempB, counter;

        int result = 0;
        while (a >= b) {
            tempA = a >> 1; //Right shif the dividend
            tempB = b;
            counter = 1;
            while (tempA >= tempB) { 
                tempB <<= 1;
                counter <<= 1; 
            }
            a -= tempB; // Subtract the doubled divisor to the dividend
            result += counter; // Add counter (2^number of left shifts)
        }
        return new int[] {result,(dividend-divisor*result)};
    }
     
    public static ArrayList<String> division(String a, String b){
        int x = Integer.parseInt(a,2);
        int y = Integer.parseInt(b,2);
        int[] result = divisionUsingShift(x,y);
        ArrayList<String> binRes = new ArrayList<String>();
        String quotient  = Integer.toBinaryString(result[0]);
        String remainder = Integer.toBinaryString(result[1]);
        binRes.add(quotient);
        binRes.add(remainder);
        return binRes;
    }

    public static void main(String args[]){
    String four = "111";
    String six =  "110";
    
    System.out.println(add(four,six));
    System.out.println(multiply("1000","100"));
        //System.out.println(("1010","10"));
    }
}
