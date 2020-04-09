#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import cv2
import matplotlib.pyplot as plt
import argparse
import os
import shutil
import projectMethod as pm
import sys
import csv
import codecs

#เรื่อง เรียน วันที่ นาย/นาง

def main():
    subject = []
    address = []
    date = []
    person = []
    text = codecs.open('output.txt','r','utf-8')
    for line in text.readlines():
        result1_1 = line.find("เรื่อง")
        result1_2 = line.find("เวื่อง")
        result2_1 = line.find("เรียน")
        result3_1 = line.find("วันที่")
        result4_1 = line.find("นาย")
        result4_2 = line.find("นาง")
        if result1_1 != -1:
            subject.append(line[result1_1:])
        if result1_2 != -1:
            subject.append(line[result1_2:])
        if result2_1 != -1:
            address.append(line[result2_1:])
        if result3_1 != -1:
            date.append(line[result3_1:])
        if result4_1 != -1:
            person.append(line[result4_1:])
        if result4_2 != -1:
            person.append(line[result4_2:])
    print(subject)
    print(address)
    print(date)
    print(person)

    with codecs.open('info.csv', 'w','utf-8') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
        csv_writer.writerow(subject)
        csv_writer.writerow(address)
        csv_writer.writerow(date)
        csv_writer.writerow(person)

if __name__ == "__main__":
    main()