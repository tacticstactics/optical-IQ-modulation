
#mach_zender_interferometer_time_def.py

import numpy as np


def propagate1(opl1=1, opl2=1, Ein=np.array([[1],[0]])):

    propagatematrix1 = np.array([[np.exp(1j*opl1),0],[0,np.exp(1j*opl2)]]);

    Eout = np.dot(propagatematrix1,Ein)
    
    return Eout



def beamsplitter(PT,Ein):

   # See Wikipedia for details. https://en.wikipedia.org/wiki/Beam_splitter       

    #Phi: Phase Shift

    #Dielectric Beamsplitter
    #phiT = 0
    #phiR = 0
    #phiO = 0
    #Symmetric Beamsplitter
    phiT = 0
    phiR = -0.5 * np.pi    
    phiO = 0.5 * np.pi
    
    T = np.sqrt(PT) # Transmission defined as Electric field
    
    PR = 1-PT 
    
    R = np.sqrt(PR) # Reflection defined as Electric field
    
    Theta1 = np.arctan(R/T) #Radian
    
    BSmatrix1 = np.dot(np.exp(1J*phiO),np.array([[np.sin(Theta1)*np.exp(1J*phiR),np.cos(Theta1)*np.exp(-1J*phiT)],[np.cos(Theta1)*np.exp(1j*phiT),-1*np.sin(Theta1)*np.exp(-1J*phiR)]]))
    Eout = np.dot(BSmatrix1, Ein)
    
    return Eout