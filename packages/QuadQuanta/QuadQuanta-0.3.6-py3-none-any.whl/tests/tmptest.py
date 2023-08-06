# -*-coding:utf-8-*-
import csv

if __name__ == '__main__':
    aa = ["ss", 'dfa', '32', 'ss']
    b = [[item] for item in aa]
    with open('eggs.csv', 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ',
                                quoting=csv.QUOTE_MINIMAL)
        #
        spamwriter.writerow(["证券代码"])
        for item in b:
            spamwriter.writerow(item)
