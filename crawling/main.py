import time
import csv
import process_division
import database.connect_db, database.insert_data

# def save_to_csv(data_list, filename):
#     headers = ["widearea_name", "basarea_name", "theater_id", "theater_name", "movie_title", "movie_time_str", "movie_date_str"]
#     with open(filename, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow(headers)
#         writer.writerows(data_list)
#
# def load_from_csv(filename):
#     data_list = []
#     with open(filename, mode='r', newline='', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         next(reader)
#         for row in reader:
#             data_list.append(row)
#     return data_list

if __name__ == '__main__':
    start_time = time.time()
    data_list = []
    divisions = [i for i in range(1, 18)]

    for i in divisions:
        data_list.extend(process_division.process_division(i))

    print("final: ", len(data_list))
    print("--- %s 초 ---" % (time.time() - start_time))

    # csv_filename = 'output_data.csv'

    # Save data to CSV file
    # save_to_csv(data_list, 'output_data.csv')

    # print("finished")
    # loaded_data = load_from_csv(csv_filename)

    # database.connect_db.create_tables()
    # database.insert_data.insert_data(loaded_data)

    database.connect_db.create_tables()
    database.insert_data.insert_data(data_list)

    print("--- %s 초 ---" % (time.time() - start_time))
