#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
int DEBUG = 1;
char* data;

int* get_list(int len) {

	int* suffix_list = (int*)malloc(len * sizeof(int));
	int i;

	for (i = 0; i < len; i++) {
		suffix_list[i] = i;
	}
	return suffix_list;
}

void quicksort(int* x, int first, int last) {
	int pivot, j, i;
	float temp;

	if (first < last) {
		pivot = first;
		i = first;
		j = last;

		while (i < j) {
			while (x[i] <= x[pivot] && i < last)
				i++;
			while (x[j] > x[pivot])
				j--;
			if (i < j) {
				temp = x[i];
				x[i] = x[j];
				x[j] = temp;
			}
		}

		temp = x[pivot];
		x[pivot] = x[j];
		x[j] = temp;
		quicksort(x, first, j - 1);
		quicksort(x, j + 1, last);

	}
}

void print_suffix_list(int* list, int len) {
	int i = 0;
	for (i = 0; i < len; i++) {
		printf("%d", list[i]);
		if (i != (len - 1)) printf(" ");
	}
	printf("\n");
}

//merge sort
void merge_sort(int i, int j, int a[], int aux[]) {
	if (j <= i) {
		return;     // the subsection is empty or a single element
	}
	int mid = (i + j) / 2;

	// left sub-array is a[i .. mid]
	// right sub-array is a[mid + 1 .. j]

	merge_sort(i, mid, a, aux);     // sort the left sub-array recursively
	merge_sort(mid + 1, j, a, aux);     // sort the right sub-array recursively

	int pointer_left = i;       // pointer_left points to the beginning of the left sub-array
	int pointer_right = mid + 1;        // pointer_right points to the beginning of the right sub-array
	int k;      // k is the loop counter

	// we loop from i to j to fill each element of the final merged array
	for (k = i; k <= j; k++) {
		if (pointer_left == mid + 1) {      // left pointer has reached the limit
			aux[k] = a[pointer_right];
			pointer_right++;
		}
		else if (pointer_right == j + 1) {        // right pointer has reached the limit
			aux[k] = a[pointer_left];
			pointer_left++;
		}
		else if (a[pointer_left] < a[pointer_right]) {        // pointer left points to smaller element
			aux[k] = a[pointer_left];
			pointer_left++;
		}
		else {        // pointer right points to smaller element
			aux[k] = a[pointer_right];
			pointer_right++;
		}
	}

	for (k = i; k <= j; k++) {      // copy the elements from aux[] to a[]
		a[k] = aux[k];
	}
}

int main(int argc, char* argv[]) {
	//quick sort sequential
	/*clock_t start, end;
	double runTime;
	int size = 10;

	start = clock();
	int* data = (int*)malloc((size + 1) * sizeof(int));
	for (int i = 0; i < size; i++) {
		data[i] = i;
	}

	quicksort(data, 0, size-1);
	print_suffix_list(data, size);

	end = clock();
	free(data);

	runTime = (end - start) / (double)CLOCKS_PER_SEC;
	printf("Quicksort sequential size: %d, and runtime: %f\n", size, runTime);*/
	

	clock_t start_m, end_m;
	double runTime_m;
	int size_m = 50;
	int a[100], aux[100], n, i, d, swap;

	for (int i = 0; i < size_m; i++) {
		a[i] = rand() % 50;
	}

	start_m = clock();

	merge_sort(0, size_m - 1, a, aux);

	end_m = clock();

	runTime_m = (end_m - start_m) / (double)CLOCKS_PER_SEC;

	printf("Printing the sorted array:\n");
	for (i = 0; i < size_m; i++)
		printf(" %d, ", a[i]);

	printf("\n");

	printf("Mergesort sequential size: %d, and runtime: %f\n", size_m, runTime_m);
}


