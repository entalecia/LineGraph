import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from celluloid import Camera
import sys
import random

class LineGraph:
    def __init__(self) -> None:
        self.FilePath = "./IO/total_cases.csv"
        self.HeaderRow = 1
        self.ReadRows = 200 #Number of rows read in the file. **None** for all rows
        self.intervals = 100
        self.fps = 30
        self.File = self.ReadFile()
        self.Headers = self.File.columns
        # self.IndexTitle = self.Headers[1::] 
        self.IndexTitle = ["World", "China","United States", "France"] #countries whose data are to be processed
        self.IndexTitle_Colors = self.get_random_hex()
        XAxisIndex = self.Headers[0]
        self.XAxis = self.File[XAxisIndex].tolist()
        self.XLabel = "Year"
        self.YLabel = "Number Of Case"
        self.Title = "Covid Cases"
        self.LineStyle = "solid" #solid, dotted, dashed, dashdot
        self.extension = ".mp4" #In case of lack of ffmpeg, use .gif extension


        #Extra Changes
        self.figsize = (16,10)
        self.XLabel_Size = 20
        self.YLabel_Size = 20
        self.NumOfX = 20
        self.XAxisRotation = -15
        self.Marker = ''
        self.Grid = False
        if self.Grid:
            self.GridColor = "Black"
            self.GridLineStyle = "-" #'-', '--', '-.', ';', '', 
            self.GridLineWidth = 1
        self.Handles = True
        if self.Handles:
            self.IndexPosition = "best" #{upper, lower, center} {right, left, center}, center, best


    def main(self):
        print("Plotting starting.")
        for i in range(1,len(self.XAxis)+1):
            NewXAxis = self.XAxis[:i]
            for Title in self.IndexTitle:
                TitleData = self.File[Title].fillna(0) # Default is 0
                self.plot_graph(TitleData, Title, NewXAxis, i)
            self.camera.snap()
        print("Plotting complete.")
        plt.xticks(self.get_Xinterval(), rotation=self.XAxisRotation)
        if self.Handles:
            self.HandelIndex()
        
        print("Animation Starting.")
        self.AnimateGraph()
        print("Animation Completed.")


    def Define(self): #plots the constants like x,y,grid,bg
        fig = plt.figure(figsize=self.figsize)
        self.camera = Camera(fig)
        plt.style.use('dark_background')
        plt.xlabel(self.XLabel,fontsize=self.XLabel_Size)
        plt.ylabel(self.YLabel,fontsize=self.YLabel_Size)
        plt.title(label=self.Title)
        plt.ticklabel_format(style='plain') #plain or sci 
        if self.Grid:
            plt.grid(color=self.GridColor, linestyle=self.GridLineStyle, linewidth = self.GridLineWidth )
        
        self.main()

    def plot_graph(self, TitleData, Country, NewXAxis,i): #loops and plots everytime
        Color = self.IndexTitle_Colors[Country]
        NewYAxis = TitleData[:i]
        plt.plot(NewXAxis,NewYAxis,linestyle=self.LineStyle, marker=self.Marker, color=Color)


    def ReadFile(self):
        if self.ReadRows:
            self.ReadRows += 1 #Adjusting indexing for 0

        TOTAL_CASES = pd.read_csv('./IO/total_cases.csv',
              header=self.HeaderRow-1,
              nrows=self.ReadRows)
        return TOTAL_CASES


    def get_Xinterval(self): #selects specific x axis to avoid collision mess
        Length = len(self.XAxis)
        TotalNum = self.NumOfX
        num = Length / TotalNum
        if type(num) == float:
            num = int(num) + 1
        Interval = [count for count in range(0,Length,num)] 
        return Interval

    def get_random_hex(self) -> str: #hex for the index of the title
        TitleHex = {}
        for Title in self.IndexTitle:
            TitleHex[Title] = "#{:06x}".format(random.randint(0,0xFFFFFF))
        return TitleHex
    
    def HandelIndex(self): #plotting the index
        handles = []
        TitleColors = self.IndexTitle_Colors
        for Title in TitleColors:
            patch = mpatches.Patch(color=TitleColors[Title], label=Title)
            handles.append(patch)
        plt.legend(handles=handles, loc=self.IndexPosition)

    def AnimateGraph(self):
        animation = self.camera.animate(interval=self.intervals, repeat=True) 
        animation.save(f'./IO/World{self.extension}', fps=self.fps) 
    

if __name__ == "__main__":
    Graph = LineGraph()
    Graph.Define()