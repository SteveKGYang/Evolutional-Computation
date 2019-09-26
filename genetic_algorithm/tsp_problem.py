#coding:utf-8

class TSPProblem:

    def __init__(self,filename):
        self.filename = filename
        self.coordinate = []
        self.distance = []
        with open(self.filename,"r") as f:
            for line in f:
                data = line.strip().split(" ")
                if len(data) == 3 and ":" not in line:
                    self.coordinate.append([data[1],data[2]])

    def cal_distance_in_between(self,x1,x2,y1,y2):
        return round(((float(x2)-float(x1))**2+(float(y2)-float(y1))**2)**0.5)

    def cal_distance(self):
        for i in range(len(self.coordinate)):
            dis_line = []
            for j in range(len(self.coordinate)):
                x1 = self.coordinate[i][0]
                y1 = self.coordinate[i][1]
                x2 = self.coordinate[j][0]
                y2 = self.coordinate[j][1]
                dis_line.append(str(self.cal_distance_in_between(x1,x2,y1,y2)))
            self.distance.append(dis_line)


    def write_to_file(self,filename):
        with open(filename,"w+") as f:
            for item in self.distance:
                f.write(",".join(item)+"\n")

    def get_distance(self):
        return self.distance
