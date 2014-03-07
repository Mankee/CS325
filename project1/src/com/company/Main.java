package com.company;

import java.io.*;

public class Main {

    public static void main(String[] args) throws IOException {

        String arrayString = null;
        long startTime, currentTime;

        if (args.length <= 0) {
            System.out.println("please specify the full path of the .txt file you wish you examine");
        }
        else {
            try {
                File file = new File(args[0]);
                FileInputStream fileInputStream =  new FileInputStream(file);
                BufferedInputStream bufferedInputStream = new BufferedInputStream(fileInputStream);
                DataInputStream dataInputStream = new DataInputStream(bufferedInputStream);

                while (dataInputStream.available() != 0) {
                    arrayString = dataInputStream.readLine();
                }

                fileInputStream.close();
                bufferedInputStream.close();
                dataInputStream.close();
            }
            catch (FileNotFoundException e) {
                e.printStackTrace();  //To change body of catch statement use File | Settings | File Templates.
            }
            catch (IOException e) {
                e.printStackTrace();
            }

            String[] items = arrayString.replaceAll("\\[", "").replaceAll("\\]", "").replaceAll(" ", "").split(",");

            int[] fullArray = new int[items.length];

            for (int i = 0; i < items.length; i++) {
                try {
                    fullArray[i] = Integer.parseInt(items[i]);
                }
                catch (NumberFormatException nfe) {
                    nfe.printStackTrace();
                    System.exit(-1);
                };
            }
            System.out.println("Calculating max sum, start time = " + System.nanoTime());
            algorithm1(fullArray);
            System.out.println("Done calculating = " + System.nanoTime());

            System.out.println("Calculating max sum, start time = " + System.nanoTime());
            algorithm2(fullArray);
            System.out.println("Done calculating = " + System.nanoTime());
        }
    }

    public static void algorithm1(int[] fullArray) {
        int beginningIndex, endingIndex, subArraySum, finalSum;

        finalSum = fullArray[0];
        beginningIndex = 0;
        int counter = 0;

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

                if (counter % 1000000 == 0) {
                    System.out.println("index: " + counter + " sum: " + finalSum + " time: " + System.nanoTime());
                }
                counter++;
                endingIndex++;
            }
            beginningIndex++;
        }
    }

    public static int algorithm2(int[] fullArray) {
        //Second Algorithm
        int subArraySum, finalSum, counter;

        counter = 0;

        finalSum = fullArray[0];
        for (int i = 0; i < fullArray.length; i++) {
            subArraySum = 0;
            for (int j = i; j < fullArray.length; j++) {
                //rather than recalculate the sum each time, just use previous subArraySum j-1 for O(1)
                subArraySum = subArraySum + fullArray[j];
                if (subArraySum > finalSum) {
                    finalSum = subArraySum;
                }
                if (counter % 1000000 == 0) {
                    System.out.println("index: " + counter + " sum: " + finalSum + " time: " + System.nanoTime());
                }
                counter++;
            }
        }
        return finalSum;
    }
}