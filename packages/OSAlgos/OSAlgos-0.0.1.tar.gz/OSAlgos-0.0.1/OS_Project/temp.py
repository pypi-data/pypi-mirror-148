from RR import *
from FCFS_Arrival import *
from FCFS import *
from SRTF import *
from SJF import *

class scheduling_algo:
   def __init__(self,n):
      self.n=n
      self.at= []
      self.bt= []
      self.proc= []

   def add_process(self,index,at,bt):
      self.proc.append(index)
      self.at.append(at)
      self.bt.append(bt)

# ------------------------FCFS----------------------------- 

   def FCFS(self):
      avgFCFS_Time(self.proc, self.n, self.bt)

   def FCFS_waiting_time(self):
      ans = avgFCFS_Time_waiting(self.proc, self.n, self.bt)
      return ans

   def FCFS_turnRound_time(self):
      ans = avgFCFS_Time_turnRound(self.proc, self.n, self.bt)
      return ans

#----------------------FCFS With Arrival---------------------

   def FCFS_Arrival(self):
      avgFCFS_A_Time(self.proc, self.n, self.bt, self.at)

   def FCFS_A_waiting_time(self):
       ans = avgFCFS_A_Time_waiting(self.proc, self.n, self.bt, self.at)
       return ans 

   def FCFS_A_turnRound_time(self):
      ans = avgFCFS_A_Time_turnRound(self.proc, self.n, self.bt, self.at)
      return ans

#----------------------Round Robin-----------------------------

   def RR(self,quantum):
      findavgTime(self.proc, self.n, self.bt, quantum)

   def RR_waiting_time(self,quantum):
      ans = avgRR_Time_waiting(self.proc, self.n, self.bt, quantum)
      return ans

   def RR_turnRound_time(self,quantum):
      ans = avgRR_Time_turnRound(self.proc, self.n, self.bt, quantum)
      return ans



#     print("Enter the number of processes: ")
#     n = int(input())
#     proc = []
#     bt = []
#     at = []
#     for i in range(n):
#         print("Enter burst time for process ", i + 1)
#         bt.append(int(input()))
#         proc.append(i+1)
#     print("Enter the time quantum: ")
#     quantum = int(input())

# for i in range(n):
#     print("Enter Arrival Time for ",i+1)
#     at.append(int(input()))

# print("\n-----------------For FCFS with Arrival -------------------")
# print("")
# avgFCFS_A_Time(proc, n, bt, at)

# print("\n -----------------For Round Robin-------------------")
# print("")
# findavgTime(proc, n, bt, quantum)

# print("\n -----------------For FCFS -------------------")
# print("")
# avgFCFS_Time(proc, n, bt)

# print("-----------------For SJF -------------------")
# print("")
# avgSJF_Time(n)

# s = scheduling_algo(3)
# s.add_process(1,0,5)
# s.add_process(2,2,3)
# s.add_process(3,4,2)
# # s.FCFS()
# # s.RR(2)
# var = s.FCFS_waiting_time()
# print(var)

