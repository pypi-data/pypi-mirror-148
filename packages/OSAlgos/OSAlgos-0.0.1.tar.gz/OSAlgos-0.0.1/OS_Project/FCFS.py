from prettytable import PrettyTable


def findWaitingTime(processes, n, bt, wt):
    wt[0] = 0
    for i in range(1, n):
        wt[i] = bt[i - 1] + wt[i - 1]


def findTurnAroundTime(processes, n, bt, wt, tat):
    for i in range(n):
        tat[i] = bt[i] + wt[i]


def avgFCFS_Time(processes, n, bt):
    wt = [0] * n
    tat = [0] * n
    total_wt = 0
    total_tat = 0
    findWaitingTime(processes, n, bt, wt)
    findTurnAroundTime(processes, n, bt, wt, tat)
    table = PrettyTable(
        ["Processes", "Burst time", "Waiting time", "Turn around time"])
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]
        table.add_row([str(i + 1), str(bt[i]), str(wt[i]), str(tat[i])])

    print("\n----------------------------FCFS----------------------------")
    print("")
    print(table)
    print("")
    print("Average waiting time = " + str(total_wt / n))
    print("Average turn around time = " + str(total_tat / n))


def avgFCFS_Time_waiting(processes, n, bt):
    wt = [0] * n
    tat = [0] * n
    total_wt = 0
    total_tat = 0
    findWaitingTime(processes, n, bt, wt)
    findTurnAroundTime(processes, n, bt, wt, tat)
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]

    return total_wt / n


def avgFCFS_Time_turnRound(processes, n, bt):
    wt = [0] * n
    tat = [0] * n
    total_wt = 0
    total_tat = 0
    findWaitingTime(processes, n, bt, wt)
    findTurnAroundTime(processes, n, bt, wt, tat)
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]

    return total_tat / n


def FCFS_Table(processes, n, bt):
    wt = [0] * n
    tat = [0] * n
    total_wt = 0
    total_tat = 0
    findWaitingTime(processes, n, bt, wt)
    findTurnAroundTime(processes, n, bt, wt, tat)
    table = PrettyTable(
        ["Processes", "Burst time", "Waiting time", "Turn around time"])
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]
        table.add_row([str(i + 1), str(bt[i]), str(wt[i]), str(tat[i])])

    print("\n----------------------------FCFS----------------------------")
    print("")
    print(table)
    print("")
