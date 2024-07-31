import time
import process_division

if __name__ == '__main__':
    start_time = time.time()
    data_list = []
    divisions = [i for i in range(1, 18)]

    for i in divisions:
        data_list.extend(process_division.process_division(i))

    print("final: ", len(data_list))
    print("--- %s 초 ---" % (time.time() - start_time))
