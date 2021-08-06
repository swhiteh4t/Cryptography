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
public class Exercise3 {

    private static boolean checkSqRoot(int n, int p) {
        n = n % p;

        for (int x = 2; x < p; x++) {
            if ((x * x) % p == n) {
                return true;
            }
        }
        return false;
    }

    public static String isSquare(String p, String n) {
        int prime = Integer.parseInt(p, 2);
        int m = Integer.parseInt(n, 2);
        return checkSqRoot(m, prime) ? "Yes" : "No";
    }
}
