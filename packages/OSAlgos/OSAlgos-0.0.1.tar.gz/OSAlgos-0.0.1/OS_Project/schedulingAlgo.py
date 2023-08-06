from RR import *
from FCFS_Arrival import *
from FCFS import *
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

# ------------------------------------FCFS------------------------------------- 

   def FCFS(self):
      avgFCFS_Time(self.proc, self.n, self.bt)

   def FCFS_waiting_time(self):
      ans = avgFCFS_Time_waiting(self.proc, self.n, self.bt)
      return ans

   def FCFS_turnRound_time(self):
      ans = avgFCFS_Time_turnRound(self.proc, self.n, self.bt)
      return ans

#-------------------------------FCFS With Arrival------------------------------

   def FCFS_Arrival(self):
      avgFCFS_A_Time(self.proc, self.n, self.bt, self.at)

   def FCFS_A_waiting_time(self):
       ans = avgFCFS_A_Time_waiting(self.proc, self.n, self.bt, self.at)
       return ans 

   def FCFS_A_turnRound_time(self):
      ans = avgFCFS_A_Time_turnRound(self.proc, self.n, self.bt, self.at)
      return ans

#---------------------------------Round Robin-----------------------------------

   def RR(self,quantum):
      findavgTime(self.proc, self.n, self.bt, quantum)

   def RR_waiting_time(self,quantum):
      ans = avgRR_Time_waiting(self.proc, self.n, self.bt, quantum)
      return ans

   def RR_turnRound_time(self,quantum):
      ans = avgRR_Time_turnRound(self.proc, self.n, self.bt, quantum)
      return ans

#------------------------------------SJF----------------------------------------

   def SJF(self):
      avgSJF_Time(self.n)
   
   def SJF_waiting_time(self):
      ans = avgSJF_Time_waiting(self.n)
      return ans

   def SJF_turnRound_time(self):
      ans = avgSJF_Time_turnRound(self.n)
      return ans

#----------------------------------------------------------------------------#

   def best_Waiting_time(self,quantum):
      FCFS_ans = self.FCFS_waiting_time()
      FCFS_A_ans = self.FCFS_A_waiting_time()
      RR_ans = self.RR_waiting_time(quantum)
      SJF_ans = self.SJF_waiting_time()
      return min(FCFS_ans,FCFS_A_ans,RR_ans,SJF_ans)

#-----------

   def best_TurnRound_time(self,quantum):
      FCFS_ans = self.FCFS_turnRound_time()
      FCFS_A_ans = self.FCFS_A_turnRound_time()
      RR_ans = self.RR_turnRound_time(quantum)
      SJF_ans = self.SJF_turnRound_time()
      return min(FCFS_ans,FCFS_A_ans,RR_ans,SJF_ans)

#-------AllAglo--------

   def showAllTable(self,quantum):
      FCFS_Table(self.proc, self.n, self.bt)
      FCFS_A_Table(self.proc, self.n, self.bt, self.at)
      RR_Table(self.proc, self.n, self.bt, quantum)
      SJF_Table(self.n)

   