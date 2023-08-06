from prettytable import PrettyTable


def findWaitingTime(processes, n, bt, wt, at):
    service_time = [0] * n
    service_time[0] = 0
    wt[0] = 0

    for i in range(1, n):
        service_time[i] = (service_time[i - 1] + bt[i - 1])

        wt[i] = service_time[i] - at[i]
        if (wt[i] < 0):
            wt[i] = 0


def findTurnAroundTime(processes, n, bt, wt, tat):
    # adding bt[i] + wt[i]
    for i in range(n):
        tat[i] = bt[i] + wt[i]


def avgFCFS_A_Time(processes, n, bt, at):
    wt = [0] * n
    tat = [0] * n
    findWaitingTime(processes, n, bt, wt, at)
    findTurnAroundTime(processes, n, bt, wt, tat)
    table = PrettyTable(["Processes", "Burst Time", "Arrival Time",
                        "Waiting Time", "Turn-Around Time", "Completion Time"])
    total_wt = 0
    total_tat = 0
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]
        compl_time = tat[i] + at[i]
        table.add_row([i + 1, bt[i], at[i], wt[i], tat[i], compl_time])
    print("\n----------------------------FCFS with Arrival ----------------------------")
    print("")
    print(table)
    print("")
    print("Average waiting time = %.5f " % (total_wt / n))
    print("Average turn around time = ", total_tat / n)


def avgFCFS_A_Time_waiting(processes, n, bt, at):
    wt = [0] * n
    tat = [0] * n
    findWaitingTime(processes, n, bt, wt, at)
    findTurnAroundTime(processes, n, bt, wt, tat)
    total_wt = 0
    total_tat = 0
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]
        compl_time = tat[i] + at[i]

    return total_wt / n


def avgFCFS_A_Time_turnRound(processes, n, bt, at):
    wt = [0] * n
    tat = [0] * n
    findWaitingTime(processes, n, bt, wt, at)
    findTurnAroundTime(processes, n, bt, wt, tat)
    total_wt = 0
    total_tat = 0
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]
        compl_time = tat[i] + at[i]

    return total_tat / n

def FCFS_A_Table(processes, n, bt, at):
    wt = [0] * n
    tat = [0] * n
    findWaitingTime(processes, n, bt, wt, at)
    findTurnAroundTime(processes, n, bt, wt, tat)
    table = PrettyTable(["Processes", "Burst Time", "Arrival Time",
                        "Waiting Time", "Turn-Around Time", "Completion Time"])
    total_wt = 0
    total_tat = 0
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]
        compl_time = tat[i] + at[i]
        table.add_row([i + 1, bt[i], at[i], wt[i], tat[i], compl_time])
    print("\n----------------------------FCFS with Arrival ----------------------------")
    print("")
    print(table)
    print("")