from django.db import models
from io import StringIO, BytesIO
import lhapdf
import matplotlib
import numpy
import math
import matplotlib.pyplot as plt
import base64
from matplotlib.font_manager import FontProperties
from matplotlib.patches import Rectangle

# Create your models here.
class Parton(models.Model):

    """class that has function partonList which creates dictionary of partons selected in form"""

    def partonList(parts):
        """function that creates dictionary of partons selected in form.
        it takes one argument wich is a list of partons selected ([['g',True],['u',True]]) and creates a dictionary with key being
        parton sign and value that consists of lhapdf number for that parton and color used for plotting and hatch
        p = {'parton_name':[parton_number,color,color_error,hatch_error]}"""
        partons = {'g':[21,'r','k','//'],'d':[1,'g','k','\\'],'u':[2,'b','k','||'],'s':[3,'m','k','--'],'c':[4,'y','k','++'],'b':[5,'c','k','xx'],'t':[6,'k','k','--\\'],'tb':[-6,'Gray','k','||--'],'bb':[-5,'DarkSlateBlue','k','oo'],'cb':[-4,'OrangeRed','k','||\\'],'sb':[-3,'Maroon','k','OO--'],'ub':[-2,'DodgerBlue','k','**'],'db':[-1,'LawnGreen','k','....']}
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

    def errorplot(self):
        """error plot function that uses data from creted object and creates image that is returned to the view,
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
        rect = []
        ps = []
        partons = Parton.partonList(self.parts)
        xp = PdfFunction.scale(self)

        if self.compare_with == 'none':
            titles = self.functions
            pdfsets = [self.functions]
            alpha = 1
        else:
            titles = self.functions + ' vs ' + self.compare_with
            pdfsets = [self.functions, self.compare_with]
            alpha = 0.3

        for num,pdfset in enumerate(pdfsets):
            pdf_vectors = []
            pdf = lhapdf.getPDFSet(pdfset)
            pdf_vectors = pdf.mkPDFs()

            for key in partons:
                x_data = []
                y_data_min = []
                y_data_max = []

                for x in xp:
                    parton_values = []
                    for i in range(pdf.size):
                        parton_values.append(pdf_vectors[i].xfxQ2(partons[key][0],x,self.Q2))
                    error = pdf.uncertainty(parton_values)
                    x_data.append(x)
                    if 'abkm09' in pdf.name:
                        if '+' in pdf.errorType:
                            y_data_min.append(error.central - error.errsymm_pdf)
                            y_data_max.append(error.central + error.errsymm_pdf)
                        else:
                            y_data_min.append(error.central - error.errsymm)
                            y_data_max.append(error.central + error.errsymm)
                    else:
                        if '+' in pdf.errorType:
                            y_data_min.append(error.central - error.errminus_pdf)
                            y_data_max.append(error.central + error.errplus_pdf)
                        else:
                            y_data_min.append(error.central - error.errminus)
                            y_data_max.append(error.central + error.errplus)

                if num == 0:
                    plt.fill_between(x_data,y_data_min,y_data_max,facecolor=partons[key][1], edgecolor=partons[key][1], alpha=alpha)
                    rect.append(Rectangle((0,0),1,1,fc=partons[key][1], alpha=alpha))
                    ps.append(key+' '+pdfset)
                else:
                    plt.fill_between(x_data,y_data_min,y_data_max,facecolor='none', hatch=partons[key][3], edgecolor='k', alpha=0.6)
                    rect.append(Rectangle((0,0),1,1,fc='none', hatch=partons[key][3], edgecolor='k'))
                    ps.append(key+' '+pdfset)

        plt.legend(rect,ps,loc = 2, prop =fontP,bbox_to_anchor = (1.0,1.0))
        plt.axis([self.xmin,self.xmax,self.ymin, self.ymax])
        plt.xscale(self.scale)
        plt.title(titles)
        plt.xlabel('x')
        plt.ylabel(' x f(x,Q^2)')

        pictureIO = BytesIO()
        plt.savefig(pictureIO, format = 'png', dpi = 100, bbox_inches = 'tight')
        return base64.encodebytes(pictureIO.getvalue()).decode()
