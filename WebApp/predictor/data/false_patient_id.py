import random
from scipy.io import arff


def add_patient_id(file):
    data = arff.loadarff(file)[0]
    with open("colon.tsv", "w") as f:
        for row in data:
            f.write(str(random.randint(100000000, 999999999)) + "\t")
            row = list(row.tolist())[0:-1]
            for elem in row:
                f.write(str(elem) + "\t")
            f.write("\n")


if __name__ == '__main__':
    add_patient_id("colonTumor_test.arff")
