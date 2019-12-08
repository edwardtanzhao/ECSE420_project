import matplotlib.pyplot as plt
from multiprocessing import Pool
import time, random

# Graph merge sort
def graphMergeSort(list):
    processNum = []
    runTimeList = []
    for n in range(0, 9):
        print("Iteration: " + str(n) + "\n")
        start = time.time()
        list = parallel_mergesort(list, n)
        elapsed = time.time() - start
        runTimeList.append(elapsed)
        processNum.append((2 ** (n + 1) - 1))

    # Graphing speedup
    plt.figure(figsize=(10, 10))
    plt.scatter(processNum, runTimeList)
    plt.plot(processNum, runTimeList)
    plt.xlabel("Number of parallel processes")
    plt.xticks([0, 20, 40, 60, 80, 100, 120, 140, 180, 220, 260, 300, 340, 380, 420, 460, 500, 540])
    plt.ylabel("Run time")
    plt.title("Parallel Merge Sort Speedup")
    plt.savefig('Merge_Sort_Speedup.png')
    plt.show()

# Merging sublists
def merge(left, right):
    merged = []
    low = high = 0
    while low < len(left) and high < len(right):
        if left[low] <= right[high]:
            merged.append(left[low])
            low += 1
        else:
            merged.append(right[high])
            high += 1
    if low == len(left):
        merged.extend(right[high:])
    else:
        merged.extend(left[low:])
    return merged

# Merge sort
def mergesort(arr):
    if len(arr) <= 1:
        return arr
    index = len(arr) // 2
    return merge(mergesort(arr[:index]), mergesort(arr[index:]))

# returning tuple of sorted lists as pair
def wrapper(pair):
    el1, el2 = pair
    return merge(el1, el2)


def parallel_mergesort(arr, n):
    threads = 2 ** n
    ends = [int(x) for x in spacing(0, len(arr), threads + 1)]
    result = [arr[ends[i]:ends[i + 1]] for i in range(threads)]

    p = Pool(processes=threads)
    curr_sorted_list = p.map(mergesort, result)

    while len(curr_sorted_list) > 1:
        result = [(curr_sorted_list[i], curr_sorted_list[i + 1]) for i in range(0, len(curr_sorted_list), 2)]
        curr_sorted_list = p.map(wrapper, result)

    return curr_sorted_list[0]


def spacing(el1, el2, steps):
    length = float(el2 - el1) / (steps - 1)
    return [el1 + i * length for i in range(steps)]


def isSorted(arr):
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            return False
    return True


if __name__ == '__main__':

    N = 5000000

    random_list = [random.random() for x in range(N)]

    random_list_copy = list(random_list)
    start = time.time()
    random_list_copy = mergesort(random_list_copy)
    diff = time.time() - start
    
    if not isSorted(random_list_copy):
        print('LIST STILL NOT SORTED!!')
    print('Mergesort in Sequential : %f sec' % (diff))

    # graphMergeSort(random_list_copy)

    random_list_copy = list(random_list)
    start = time.time()
    # number of threads = 2^(n+1) - 1
    n = 2

    random_list_copy = parallel_mergesort(random_list_copy, n)

    diff = time.time() - start

    if not isSorted(random_list_copy):
        print('LIST STILL NOT SORTED!!')
    print('Mergesort in Parallel: %f sec' % (diff))