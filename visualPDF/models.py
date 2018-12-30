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

    """class that has function partonList which creates dictionary of partons selected in form"""

    def partonList(parts):
        """function that creates dictionary of partons selected in form.
        it takes one argument wich is a list of partons selected ([['g',True],['u',True]]) and creates a dictionary with key being
        parton sign and value that consists of lhapdf number for that parton and color used for plotting"""
        partons = {'g':[21,'r'],'d':[1,'g'],'u':[2,'b'],'s':[3,'m'],'c':[4,'y'],'b':[5,'c'],'t':[6,'k'],'tb':[-6,'Gray'],'bb':[-5,'DarkSlateBlue'],'cb':[-4,'OrangeRed'],'sb':[-3,'Maroon'],'ub':[-2,'DodgerBlue'],'db':[-1,'LawnGreen']}
        p = {}
        for i in range(len(parts)):
            if parts[i][1] == True:
                p[parts[i][0]]=partons[parts[i][0]]
        return p

class PdfFunction(models.Model):
    """class that creates PdfFunction object with gathered data.
    has functions __init__, __str__, plot, scale"""

    def __init__(self, functions, compare_with, Q2, xmin, xmax, points, ymin, ymax, g, u, d,scale):
        """used when creating object"""
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
        self.scale = scale

    def __str__(self):
        return self.functions, self.compare_with

    def scale(self):
        """creates a list of numbers used for plotting.
        list can be filled with log values or lin values
        self.scale is used for determining which one to use for creating the list
        self.scale determines the scale in plot() function"""
        if self.scale == 'log':
            space = numpy.logspace(math.log10(self.xmin),math.log10(self.xmax),self.points)
        else:
            space = numpy.linspace(self.xmin, self.xmax, self.points)
            self.scale = 'linear'

        return space

    def plot(self):
        """plot function that uses data from creted object and creates image that is returned to the view,
        image is created with matplotlib and lhapdf library and encoded with ByteIO with base64,
        """
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
        xp = PdfFunction.scale(self)

        if self.compare_with == 'none':
            titles = self.functions
            pdfsets = [self.functions]
        else:
            titles = self.functions + ' vs ' + self.compare_with
            pdfsets = [self.functions, self.compare_with]


        for num,pdfset in enumerate(pdfsets):

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
        plt.xscale(self.scale)
        plt.title(titles)
        plt.xlabel('x')
        plt.ylabel(' x f(x,Q^2)')

        pictureIO = BytesIO()
        plt.savefig(pictureIO, format = 'png', dpi = 100, bbox_inches = 'tight')
        return base64.encodebytes(pictureIO.getvalue()).decode()
