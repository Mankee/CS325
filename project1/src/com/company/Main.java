package com.company;

public class Main {

    public static void main(String[] args) {
        int[] fullArray = new int[]{22, -27, 38, -34, 49, 40, 13, -44, -13, 28, 46, 7, -26, 42, 29, 0, -6, 35, 23, -37,
                               10, 12, -2, 18, -12, -49, -10, 37, -5, 17, 6, -11, -22, -17, -50, -40, 44, 14, -41, 19,
                               -15, 45, -23, 48, -1, -39, -46, 15, 3, -32, -29, -48, -19, 27, -33, -8, 11, 21, -43, 24,
                               5, 34, -36, -9, 16, -31, -7, -24, -47, -14, -16, -18, 39, -30, 33, -45, -38, 41, -3, 4,
                               -25, 20, -35, 32, 26, 47, 2, -4, 8, 9, 31, -28, 36, 1, -21, 30, 43, 25, -20, -42};

        //first algorithm
        int beginningIndex;
        int endingIndex;
        int subArraySum;
        int finalSum;

        finalSum = fullArray[0];
        beginningIndex = 0;
        for (int i = 0; i < fullArray.length; i++) {
            endingIndex = i;
            for (int j = i; j < fullArray.length; j++) {

                //loop over each pair of indices to find the sum of of the sub array
                subArraySum = 0;
                for (int k = beginningIndex; k <= endingIndex; k++) {
                    subArraySum = subArraySum + fullArray[k];
                }

                if (subArraySum > finalSum) {
                    finalSum = subArraySum;
                }
                endingIndex++;
            }
            beginningIndex++;
        }
        System.out.println(finalSum);

        //Second Algorithm
        finalSum = fullArray[0];
        for (int i = 0; i < fullArray.length; i++) {
            subArraySum = 0;
            for (int j = i; j < fullArray.length; j++) {
                //rather than recalculate the sum each time, just use previous subArraySum j-1 for O(1)
                subArraySum = subArraySum + fullArray[j];
                if (subArraySum > finalSum) {
                    finalSum = subArraySum;
                }
            }
        }
        System.out.println(finalSum);
    }
}