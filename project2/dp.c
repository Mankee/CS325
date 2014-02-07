/* Project: #2 Dynamic Programming
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

#include "dp.h"

int dp_maxsubarray(int a_size, int a[]) 
{
	int i, max = 0, curr = 0, max_array[a_size];
	
	if (a_size > 0)
	{
		max_array[0] = a[0];
	
		/* Fill the max array */
		for(i = 1; i < a_size; i++)
		{
			curr = max_array[i-1] + a[i];
			max_array[i] = (curr > 0 ? curr : 0);
		}
		
		/* Find the maximum value */
		for(i = 0; i < a_size; i++)
		{
			max = (max > max_array[i] ? max : max_array[i]); 
		
		}
	}
	return max;
}

