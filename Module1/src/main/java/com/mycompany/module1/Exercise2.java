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
public class Exercise2 {
    
    static int power(int a, int b, int n) 
    {  
        int result = 1;    
         
        // a has to be greater or equal than n 
        a = a % n;  
  
       if (a == 0) return 0;  
  
        while (b > 0) 
        { 
            //Check if the power is an odd number 
            if((b & 1)==1) 
                result = (result * a) % n; 
      
            //Now it is an even number
            b = b >> 1;  
            a = (a * a) % n;  
        } 
        return result; 
    } 
    
    public static String powerMod(String a, String b, String n){
        int x = Integer.parseInt(a,2);
        int y = Integer.parseInt(b,2);
        int z = Integer.parseInt(n,2);
        
        int result = power(x,y,z);
        return Integer.toBinaryString(result);
    }
}
