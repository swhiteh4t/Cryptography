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
public class Exercise4 {

    private static int sRoot(int p, int m) {
        m = m % p;

        for (int x = 2; x < p; x++) {
            if ((x * x) % 4 == 3) {
                return true;
            }
        }
        return 0;
    }
    
    public static String sqrtprime(String p, String m){
        int x = Integer.parseInt(p,2);
        int y = Integer.parseInt(m,2);
        
        int result = sRoot(x,y);
        
        return Integer.toBinaryString(result);
        
        
    }
    
    
}
