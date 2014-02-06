
/* Project: #2 DP
 *
 * Team RADZ:
 *  Rittie Chuaprasert (chuaprar)
 *  Austin Dubina (weila)
 *  Darren Baker (bakerdar)
 *  Zac Knudson (knudsoza)
 * 
 * CS 325-400
 * Winter 2014
 * 
*/

#include "ma.h"


/* Algorithm 3 for MaxSubArray */

// @param array given array of small integers
// @param start_index starting index of the subarray to be tested
// @param last_index ending index of the subarray to be tested
// @return max sum of all subarrays within the subarray to be tested
int _max_subarray(int *array, int start_index, int last_index) 
{

    int i, mid_index, max_firsthalf, max_secondhalf, curr_index, curr_straddle, max_straddle, function_val;

    //base case only 1 array member
    if (start_index == last_index)
   	 return array[start_index];

    else {
   	 mid_index = (start_index + last_index)/2;

   	 // (recursively) get max_subarray from first half of array
   	 max_firsthalf = _max_subarray(array, start_index, mid_index);

   	 // (recursively) get max_subarray from second half of array
   	 max_secondhalf = _max_subarray(array, mid_index+1, last_index);

   	 // get max_subarray containing 1st half suffix, 2nd half prefix
   	 //    	 get max_subarray from 1st half containing 1st half suffix
   	 curr_index = mid_index;
   	 max_straddle = curr_straddle = array[curr_index];;
   	 for (i=curr_index-1; i>=start_index; i--) {
   		 curr_straddle += array[i];
   		 if (curr_straddle > max_straddle) {
   			 max_straddle = curr_straddle;
   		 }
   	 }

   	 //    	 add max_subarray from 2nd half containing 2nd half prefix
   	 curr_index = mid_index+1;
   	 curr_straddle = max_straddle + array[curr_index];
   	 max_straddle = curr_straddle;
   	 for (i=curr_index+1; i<=last_index; i++) {
   		 curr_straddle += array[i];
   		 if (curr_straddle > max_straddle)
   			 max_straddle = curr_straddle;
   	 }
   	 // max_straddle is max_subarray w/ 1st half suffix, 2nd half prefix

   	 // return the function value
   	 if (max_firsthalf >= max_secondhalf) {
   		 if (max_firsthalf > max_straddle)
   			 function_val = max_firsthalf;
   		 else
   			 function_val = max_straddle;
   	 }
   	 else { //(max_firsthalf < max_secondhalf)
   		 if (max_secondhalf >= max_straddle)
   			 function_val = max_secondhalf;
   		 else
   			 function_val = max_straddle;
   	 }

   	 return function_val;
    }
}

int a3_maxsubarray(int a_size, int a[]) 
{
	int ans; 
	ans = _max_subarray(a, 0, a_size-1); 
	//printf("N=%d ans=%d\n", a_size, ans);
	return ans;
}


