import random, time
from multiprocessing import Process, Pipe
import matplotlib.pyplot as plt


def graphParallelQuickSort(list):
    timingList = []
    processList = []
    # add to the run time list then we could graph them
    for n in range(0, 9):
        print("Iteration: " + str(n) + "\n")
        start = time.time()
        pconn, cconn = Pipe()
        p = Process(target=quicksortParallel, args=(list, cconn, n))
        p.start()
        list = pconn.recv()
        p.join()
        elapsed = time.time() - start
        timingList.append(elapsed)
        processList.append((2 ** (n + 1) - 1))
    # Graphing speedup
    plt.figure(figsize=(10, 10))
    plt.scatter(processList, timingList)
    plt.plot(processList, timingList)
    plt.xlabel("Number of parallel processes")
    plt.xticks([0, 20, 40, 60, 80, 100, 120, 140, 180, 220, 260, 300, 340, 380, 420, 460, 500, 540])
    plt.ylabel("Run time")
    plt.title("Parallel Quick Sort Speedup")
    plt.savefig('Quick_Sort_Speedup.png')
    plt.show()


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pvt = arr.pop(random.randint(0, len(arr) - 1))
    return quicksort([x for x in arr if x < pvt]) + [pvt] + quicksort([x for x in arr if x >= pvt])


def quicksortParallel(arr, connection, threads):
    if threads <= 0 or len(arr) <= 1:
        connection.send(quicksort(arr))
        connection.close()
        return

    pvt = arr.pop(random.randint(0, len(arr) - 1))

    left = [x for x in arr if x < pvt]
    right = [x for x in arr if x >= pvt]

    conn1_left, conn2_left = Pipe()
    left_thread = Process(target=quicksortParallel, args=(left, conn2_left, threads - 1))

    pconnRight, cconnRight = Pipe()
    right_thread = Process(target=quicksortParallel, args=(right, cconnRight, threads - 1))

    left_thread.start()
    right_thread.start()

    connection.send(conn1_left.recv() + [pvt] + pconnRight.recv())
    connection.close()

    left_thread.join()
    right_thread.join()


def isSorted(arr):
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            return False
    return True


if __name__ == '__main__':

    N = 5000000

    random_list = [random.randint(0, N) for x in range(N)]
    # graphParallelQuickSort(random_list_copy)

    # Sequential QuickSort

    random_list_copy = list(random_list)  # copy the list
    start = time.time()  # start time
    print("\n sequential Quick Sort is starting...")
    random_list_copy = quicksort(random_list_copy)
    print("sequential Quick Sort...Done")
    diff = time.time() - start
    if not isSorted(random_list_copy):
        print('\n LIST STILL NOT SORTED!!')
    print('Sequential Quick Sort time: %f sec' % (diff))

    # Parallel quicksort
    random_list_copy = list(random_list)
    start = time.time()
    print("\nParallel Quick Sort starting...")
    # choose n where number of processors = 2^(n+1) - 1
    n = 5
    conn1, conn2 = Pipe()
    p = Process(target=quicksortParallel, args=(random_list_copy, conn2, n))
    p.start()
    random_list_copy = conn1.recv()
    p.join()
    diff = time.time() - start
    print("Parallel Quick Sort done execution!")

    if not isSorted(random_list_copy):
        print('\n LIST STILL NOT SORTED!!')
    print('Parallel QuickSort time: %f sec' % (diff))
