import csv
import sys
import numpy as np
import math
import matplotlib.pyplot as plt

class X_t_Function:
    def __init__(self, a: float, b: float, K: float) -> None:
        self.a = a
        self.b = b
        self.K = K
        pass

    def get(self, t: float) -> float:
        return self.K / (1+math.exp(self.a - self.b * t))

def readAndReturn(filename: str) -> list:
    data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            list_of_floats = [float(x) for x in row]
            data.append(list_of_floats)
    
    return data

def processData(data: list) -> list:
    xnextdiff = []
    xder = []
    xsquare = []
    for index in range(len(data[1])-1):
        xnextdiff.append(data[1][index+1]-data[1][index])
        xder.append(xnextdiff[-1]/data[1][index])
        xsquare.append(data[1][index]**2)
    
    data.append(xnextdiff)
    data.append(xder)
    data.append(xsquare)

    return data

def sumList(data: list) -> float:
    sum = 0
    counter = 0
    while counter < len(data):
        sum += data[counter]
        counter += 1
    return sum

def findSolution(data) -> X_t_Function:
    # for entry in data:
    #     print(data)

    A = np.array(
        [
            [
                len(data[0])-1,
                sumList(data[1][:-1])
            ],
            [
                sumList(data[1][:-1]),
                sumList(data[4])
            ]
        ]
    )

    B = np.array(
        [
            sumList(data[3]),
            sumList(data[2])
        ]
    )

    # print(A, B)

    solution = np.linalg.solve(A, B)
    K = -solution[0]/solution[1]

    a = calculate_a(data=data, K=K, b=solution[0])
    print("a = ", a)
    print("Solution: b =", solution[0], ", q =", solution[1])
    print("K = ", K)
    return X_t_Function(a, solution[0], K)

def calculate_a(data: list, K: float, b: float) -> float:
    a = 0
    for index in range(len(data[0])):
        a += math.log(K/data[1][index]-1)+ b*(len(data[0])+1)/2
    return a/len(data[0])

def average_diff(data, func: X_t_Function) -> (float, float):
    diffs = []
    counter = 0
    while counter < len(data[1]):
        diffs.append(
            100*((func.get(counter+1) - data[1][counter])/data[1][counter])
        )
        counter += 1
    
    std_dev = np.std(diffs)
    return sumList(diffs)/len(data[1]), std_dev

def plot_solution_in_range(sol: X_t_Function, start: int, stop: int, data: list) -> None:
    x_values = [x for x in range(start, stop)]
    y_values = [sol.get(y) for y in x_values]
    plt.plot(x_values, y_values, label='solution')

    plt.plot(data[0], data[1], label="initial")

    plt.xlabel('Time')
    plt.ylabel('Estimate')
    plt.title('Solution Estimates')
    plt.grid(True)  
    plt.legend()
    plt.show()

if __name__=="__main__":
    fileName = sys.argv[1]
    data = processData(
        readAndReturn(filename=fileName)
    )
    sol = findSolution(data)
    metrics = average_diff(data, sol)
    print(
        "Average difference: ", metrics[0], "\n"
        "Standart deviation: ", metrics[1]
    )
    plot_solution_in_range(sol, 0, 15, data)

