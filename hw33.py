import numpy as np
import pandas as pd
import random

class K_means:
    def __init__(self,dataFile,k):
      self.raw_input = pd.read_csv(dataFile, sep = "|", header = None)
      self.k = k

    def preprocess(self):
      self.df = self.raw_input
      self.df.drop(self.df.columns[[0,1]],axis=1,inplace=True)
      self.df = self.df.replace('#','', regex=True)
      self.df = self.df.replace(':','', regex=True)
      self.df = self.df.replace('$','', regex=True)
      self.df = self.df.replace('%','', regex=True)
      self.df = self.df.replace('@\w+','', regex=True)
      self.df = self.df.replace('http\S+','',regex=True)
      self.df[2] = self.df[2].str.lower()
      print(self.df)
      return self.df
    
    def jaccard_distance(self, A, B):
      A = set(A)
      B = set(B)
      jaccard = 1 - (len(A & B)) / len(A | B)
      return jaccard

    def initial_centroid(self, k):
      n = len(self.df)
      random.seed(50)
      centroid = np.array(random.sample(range(0, n),k))
      return centroid

    def convergent(self, k, old_centroid, new_centroid):
      old_centroid = sorted(old_centroid)
      new_centroid = sorted(new_centroid)
      if (new_centroid != old_centroid):
        return False
      else:
        return True
    
    def clustering(self, k, centroid):
        n = len(self.df)
        n_k = k
        new_centroid = []
        print(centroid)
        oldcentroid = centroid
        status = True
        sse = 0
        while(status):
            matrix = [[] for i in range(n)]
            index = []
            for i in range(0, n):
                for j in range(0, k):
                    distance = self.jaccard_distance(self.df[2][oldcentroid[j]], self.df[2][i])
                    matrix[i] = np.append(matrix[i], distance)
            for i in range(0, n):
                index.append(np.argmin(matrix[i]))
        #print(index)
            real_index = [[] for i in range(k)]
            for i in range(k):
                for j in range(n):
                    if(i == index[j]):
                        real_index[i] = np.append(real_index[i], j)
        #for j in range(k):
          # print(len(real_index[j]))
            count = []
            new_centroid = []
            for i in range(0, k):
                count.append(index.count(i))
            for i in range(k):
                new_centroid.append(self.get_new_centroid(real_index[i]))
           # for i in range(k):
            se = self.sse(k, new_centroid)
            sse = sse + se
            print(sorted(new_centroid))
            if(self.convergent(k, oldcentroid, new_centroid)):
               status = False
               for j in range(k):
                    if (j==0):
                       print("1 : ", len(real_index[j]), "tweets")
                    if (j==1):
                       print("2 : ", len(real_index[j]), "tweets")
                    if (j==k-1):
                       print(k,": ", len(real_index[j]), "tweets")
                    
               print("centroid", sorted(new_centroid))
               print("SSE", sse)
               return new_centroid
            else:
               oldcentroid = new_centroid

    
    def new_centroid(self, k):
       centroid = self.initial_centroid(k)
       self.clustering(k, centroid)

    def sse(self, k, centroid):
        sse = 0
        n = len(self.df)
        for i in range(n):
          for j in range(k):
            se = (self.jaccard_distance(self.df[2][centroid[j]], self.df[2][i]))**2
            sse = sse + se
        return sse
             
    def get_new_centroid(self, index):
        n = len(index)
        past_dist = 1
        centroid = 0
        for i in range(n):
           for j in range(n):
                if (i==j) | (i > j):
                    continue
                else:
                    jaccard_dist = self.jaccard_distance(self.df[2][index[i]], self.df[2][index[j]])
                    if(jaccard_dist < past_dist) & (jaccard_dist != 0):
                        #print(jaccard_dist)
                        past_dist = jaccard_dist
                        #print(past_dist)
                        centroid = index[i]
        return centroid

    

if __name__ == "__main__":
    k = 5

    kmeans = K_means("https://raw.githubusercontent.com/rlagkdms4372/cs4375/main/usnewshealth.txt", k)
    kmeans.preprocess()
    #kmeans.initial_centroid(k)
    kmeans.new_centroid(k) # put in path to your file
