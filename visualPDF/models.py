from django.db import models
from io import StringIO, BytesIO
import lhapdf
import matplotlib
import numpy
import math
import matplotlib.pyplot as plt
import base64
from matplotlib.font_manager import FontProperties

# Create your models here.
class Parton(models.Model):

    def partonList(parts):

        partons = {'g':[21,'r'],'d':[1,'g'],'u':[2,'b'],'s':[3,'m'],'c':[4,'y'],'b':[5,'c'],'t':[6,'k'],'tb':[-6,'Gray'],'bb':[-5,'DarkSlateBlue'],'cb':[-4,'OrangeRed'],'sb':[-3,'Maroon'],'ub':[-2,'DodgerBlue'],'db':[-1,'LawnGreen']}
        p = {}
        for i in range(len(parts)):
            if parts[i][1] == True:
                p[parts[i][0]]=partons[parts[i][0]]
        return p

class PdfFunction(models.Model):

    def __init__(self, functions, compare_with, Q2, xmin, xmax, points, ymin, ymax, g, u, d):
        self.functions = functions
        self.compare_with = compare_with
        self.Q2 = Q2
        self.xmin = xmin
        self.xmax = xmax
        self.points = points
        self.ymin = ymin
        self.ymax = ymax
        self.g = ['g',g]
        self.u = ['u',u]
        self.d = ['d',d]
        self.parts = [self.g, self.u, self.d]

    def __str__(self):
        return self.functions, self.compare_with

    def plot(self):

        matplotlib.use('Agg')
        plt.figure(figsize=(6,5),dpi=100)
        plt.subplots_adjust(right=0.8)
        plt.subplots_adjust(left=0.2)
        plt.subplots_adjust(bottom=0.2)
        fontP = FontProperties()
        fontP.set_size('small')

        pdfsets = []
        lst = ['-','--']
        partons = Parton.partonList(self.parts)
        xp = numpy.linspace(self.xmin, self.xmax, self.points)

        if self.compare_with == 'none':
            titles = self.functions
            pdfsets = [self.functions]
        else:
            titles = self.functions + ' vs ' + self.compare_with
            pdfsets = [self.functions, self.compare_with]


        for num,pdfset in enumerate(pdfsets):

            #lhapdf.pathsAppend('/home/vedran/.local/share/lhapdf')
            pdf = lhapdf.mkPDF(pdfset,0)

            for key in partons:
                x_data = []
                y_data = []
                for x in xp:
                    xfx = pdf.xfxQ2(partons[key][0],x,self.Q2)
                    x_data.append(x)
                    y_data.append(xfx)
                plt.plot(x_data,y_data,partons[key][1],ls = lst[num], label = key + ' ' + pdfset)
            plt.legend(loc = 2, prop =fontP,bbox_to_anchor = (1.0,1.0))

        plt.axis([self.xmin,self.xmax,self.ymin, self.ymax])
        plt.xscale('log')
        plt.title(titles)
        plt.xlabel('x')
        plt.ylabel(' x f(x,Q^2)')

        pictureIO = BytesIO()
        plt.savefig(pictureIO, format = 'png', dpi = 100, bbox_inches = 'tight')
        return base64.encodebytes(pictureIO.getvalue()).decode()
