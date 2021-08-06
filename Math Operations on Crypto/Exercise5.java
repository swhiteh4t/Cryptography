/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.mycompany.module1;

import java.util.Random;

/**
 *
 * @author svalle
 */
public class Exercise5 {

    private static int gcd(int a, int b) {
        while (b != 0) {
            int t = a;
            a = b;
            b = t % b;
        }
        return a;
    }

    public static boolean isPrime(int n, int iteration) {

        //Base case of the recursion
        if (n == 0 || n == 1) {
            return false;
        }

        //Base case of prime number
        if (n == 2) {
            return true;
        }

        //If the number is even then 
        // is not prime
        if (n % 2 == 0) {
            return false;
        }

        //Get the random object
        Random rand = new Random();

        for (int i = 0; i < iteration; i++) {
            int r, a;

            //Generate a random number
            r = Math.abs(rand.nextInt());

            a = r % (n - 1) + 1;

            if (Exercise2.power(a, n - 1, n) != 1) {
                return false;
            }

        }

        return true;

    }

    public static String fermatTest(int n, int N) {
        if (isPrime(n, N)) {
            return "yes";
        } else {
            return "no conclusion";
        }
    }

    public static void main(String args[]) {
        System.out.println(fermatTest(21521, 1000));
    }
}
