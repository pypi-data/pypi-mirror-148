from prettytable import PrettyTable

def findWaitingTime(processes, n, bt, wt, quantum):
    rem_bt = [0] * n

    for i in range(n):
        rem_bt[i] = bt[i]
    t = 0
    while(1):
        done = True
        for i in range(n):
            if (rem_bt[i] > 0):
                done = False
                if (rem_bt[i] > quantum):
                    t += quantum
                    rem_bt[i] -= quantum
                else:
                    t = t + rem_bt[i]
                    wt[i] = t - bt[i]
                    rem_bt[i] = 0
        if (done == True):
            break

def findTurnAroundTime(processes, n, bt, wt, tat):
    for i in range(n):
        tat[i] = bt[i] + wt[i]

def findavgTime(processes, n, bt, quantum):
    wt = [0] * n
    tat = [0] * n
    findWaitingTime(processes, n, bt, wt, quantum)
    findTurnAroundTime(processes, n, bt, wt, tat)
    table = PrettyTable(["Processes","Burst Time","Waiting Time","Turn-Around Time"])
    total_wt = 0
    total_tat = 0
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]
        table.add_row([ i+1, bt[i], wt[i], tat[i]])

    print("\n----------------------------Round Robin----------------------------")
    print("")    
    print(table)
    print("")
    print("\nAverage waiting time = %.5f " % (total_wt / n))
    print("Average turn around time = %.5f " % (total_tat / n))

def avgRR_Time_waiting(processes, n, bt, quantum):
    wt = [0] * n
    tat = [0] * n
    findWaitingTime(processes, n, bt, wt, quantum)
    findTurnAroundTime(processes, n, bt, wt, tat)
    total_wt = 0
    total_tat = 0
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]

    return total_wt / n

def avgRR_Time_turnRound(processes, n, bt, quantum):
    wt = [0] * n
    tat = [0] * n
    findWaitingTime(processes, n, bt, wt, quantum)
    findTurnAroundTime(processes, n, bt, wt, tat)
    total_wt = 0
    total_tat = 0
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]

    return total_tat / n

def RR_Table(processes, n, bt, quantum):
    wt = [0] * n
    tat = [0] * n
    findWaitingTime(processes, n, bt, wt, quantum)
    findTurnAroundTime(processes, n, bt, wt, tat)
    table = PrettyTable(["Processes","Burst Time","Waiting Time","Turn-Around Time"])
    total_wt = 0
    total_tat = 0
    for i in range(n):
        total_wt = total_wt + wt[i]
        total_tat = total_tat + tat[i]
        table.add_row([ i+1, bt[i], wt[i], tat[i]])

    print("\n----------------------------Round Robin----------------------------")
    print("")    
    print(table)
    print("")