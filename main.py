from everyday import API
import csv

def create_csv():
    with open("ex2.csv", "w") as csvfile:
        writer = csv.writer(csvfile)

        # 先写入columns_name
        writer.writerow(["a", "b", "c", "d", "message"])
        writer.writerows([[1, 2, 3, 4, 'hello'], [5, 6, 7, 8, 'world'], [9, 10, 11, 12, 'foo']])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    create_csv()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
