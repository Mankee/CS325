package com.company;

public class Main {

    public static void main(String[] args) {
        int[] fullArray = new int[]{22, -27, 38, -34, 49, 40, 13, -44, -13, 28, 46, 7, -26, 42, 29, 0, -6, 35, 23, -37,
                               10, 12, -2, 18, -12, -49, -10, 37, -5, 17, 6, -11, -22, -17, -50, -40, 44, 14, -41, 19,
                               -15, 45, -23, 48, -1, -39, -46, 15, 3, -32, -29, -48, -19, 27, -33, -8, 11, 21, -43, 24,
                               5, 34, -36, -9, 16, -31, -7, -24, -47, -14, -16, -18, 39, -30, 33, -45, -38, 41, -3, 4,
                               -25, 20, -35, 32, 26, 47, 2, -4, 8, 9, 31, -28, 36, 1, -21, 30, 43, 25, -20, -42};

        System.out.println("test");

        int finalSum = fullArray[0];
        for (int i = 0; i < fullArray.length; i++) {
            int subArraySum = 0;
            for (int j = i; j < fullArray.length; j++) {
                subArraySum = subArraySum + fullArray[j];
                if (subArraySum > finalSum) {
                    finalSum = subArraySum;
                }
            }
        }
        System.out.println(finalSum);
    }
}