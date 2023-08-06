class GetMetadata:
   empCount = 0
   def __init__(self, latitude, longitude):
      self.latitude = latitude
      self.longitude = longitude
      GetMetadata.empCount += 1
   def displayCount(self):
      print("Total Employee %d" % GetMetadata.empCount)
   def displayEmployee(self):
      print("Name : ", self.latitude, ", Salary: ", self.longitude)