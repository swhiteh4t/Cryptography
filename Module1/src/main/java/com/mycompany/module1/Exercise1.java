/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.module1;

/**
 *
 * @author svalle
 */
public class Exercise1 {
    //The meaning of the variables is the following
    // a * s + b * r = gcd(a,b)
    public int gcd;
    public int s;
    public int r;
    
    
    
    private static int[] gcd(int p, int q) {
      if (q == 0)
         return new int[] { p, 1, 0 };

      int[] vals = gcd(q, p % q);
      int d = vals[0];
      int a = vals[2];
      int b = vals[1] - (p / q) * vals[2];
      return new int[] { d, a, b };
   }
    
    public static String inverse(String a, String n){
        int x = Integer.parseInt(a, 2);
        int y = Integer.parseInt(n,2);
        
        int[] result = gcd(x,y);
        if (result[0] > 1) {
        return "";
    }
        return Integer.toBinaryString(result[1]);
    }
    
    public static void main(String args[]){
        String a = "100";
        String b = "111";
        System.out.println(inverse(a,b));
    }
}
