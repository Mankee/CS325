placeholder text file for project 2 repo. All project 2 files should go in this sub directory, including any archive folders.

Version 1: pseudocode
A[i] = [-2, -3, 4, -1, -2, 1, 5, -3], where i is the index in array A

S{i} = Max sub-sequence sum, where i equals the current index in the array A

This algorithm works by using a sliding window to calculate the max sub-sequence sum. If the sum of the previous max sub-sequence array (i-1) and the current value A[i] is less than or equal to A[i] then S{i} = A[i]; otherwise increase the window size by 1 and repeat this process until all max sub-sequences have been calculated. The largest S will be our answer.


S{i} = max { S(i-1) + A[i], A[i] }


example:
[-2, -3, 4, -1, -2, 1, 5, -3]
S(1) = max { S(i -1) + A[i], A[i] }
S(1) = max { S(0) + A[0], A[0] }
S(1) = max { 0 + -2, -2 } 
S(1) = max { -2, -2 }
S(1) = -2

S(2) = max { S(2 - 1) + A[2], A[2] }
S(2) = max { S(1) + A[2], A[2] }
S(2) = max { -2 + -3, -3 }
S(2) = max { -5, -3 }
S(2) = -3

S(3) = max { S(2) + A[3], A[3] }
S(3) = max { -3 + 4, 4 }
S(3) = max { 1, 4 }
S(3) = 4

S(4) = max { S(3) + A[4], A[4]}
S(4) = max { 4 + -1, -1 }
S(4) = max { 3, -1 }
S(4) = 3

S(5) = max { S(4) + A[5], A[5] }
S(5) = max { 3 + -2, 1 }
S(5) = max { 1, 1 }
S(5) = 1

S(6) = max { S(5) + A[6], A[6] }
S(6) = max { 1 + 5, 5}
S(6) = 6

S(7) = max { S(6) + A[7], A[7]}
S(7) = max { 6 + -3, -3}
S(7) = 3

max { S(1) , S(2), S(3), S(4), S(5), S(6), S(7) }
max { -2, -3, 4, 3, 1, 6, 3 } = 6 <----- the answer
