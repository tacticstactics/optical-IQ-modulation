
import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import c 

import mach_zender_interferometer_time_def

print('')
print('mach-zender_interferometer_IQ modulation_main.py')
print('')

wl1 = 1550e-9
freq1 = c / wl1

samplerate = 2 ** 16 # NUmber of Points
stept = 2 ** -50 #[s]
print(stept)
tcol = np.linspace(0.0, stept * samplerate, samplerate, endpoint=False)

amp_sine = 0.5*np.pi
freq_sine1 = 1e12 # [Hz]
dc_offset = 0.5*np.pi # DC offset

amp_cosine = 0.5*np.pi
freq_cosine1 = 1e12 # [Hz]


#sine_signal
sine_signalcol = np.zeros(samplerate, dtype=complex)
for ii in range(samplerate):       
    t = tcol[ii]
    sinesignal = amp_sine * np.sin(2 * np.pi * freq_sine1 * t) + dc_offset
    sine_signalcol[ii] = sinesignal  


#cosine_signal
cosine_signalcol = np.zeros(samplerate, dtype=complex)
for ii in range(samplerate):       
    t = tcol[ii]
    cosinesignal = amp_cosine * np.cos(2 * np.pi * freq_cosine1 * t) + dc_offset
    cosine_signalcol[ii] = cosinesignal  



#prbs pseudo random signal
amp_prbs = 1*np.pi

# Random_signal generation

a1_range = [0, 1]
a1 = np.random.rand(samplerate) * (a1_range[1]-a1_range[0]) + a1_range[0] # range for amplitude

# Arm A
b1_range = [1000, 2000]
b1 = np.random.rand(samplerate) *(b1_range[1]-b1_range[0]) + b1_range[0] # range for frequency
b1 = np.round(b1)
b1 = b1.astype(int)

b1[0] = 0

for i in range(1,np.size(b1)):
    b1[i] = b1[i-1]+b1[i]

i=0
random_signal = np.zeros(samplerate, dtype=complex)
while b1[i]<np.size(random_signal):
    k = b1[i]
    random_signal[k:] = a1[i]
    i=i+1

a1 = np.zeros(samplerate, dtype=complex)
j = 0
while j < samplerate:
    a1[j] = amp_prbs
    a1[j+1] = 0
    j = j+2

i=0
prbs1 = np.zeros(samplerate, dtype=complex)
while b1[i]<np.size(prbs1):
    k = b1[i]
    prbs1[k:] = a1[i]
    i=i+1

# Arm B

b2_range = [2000, 4000]
b2 = np.random.rand(samplerate) *(b2_range[1]-b2_range[0]) + b2_range[0] # range for frequency
b2 = np.round(b2)
b2 = b2.astype(int)

b2[0] = 0

for i in range(1,np.size(b2)):
    b2[i] = b2[i-1]+b2[i]

i=0
random_signal2 = np.zeros(samplerate, dtype=complex)
while b2[i]<np.size(random_signal2):
    k = b2[i]
    random_signal2[k:] = a1[i]
    i=i+1

a2 = np.zeros(samplerate, dtype=complex)
j = 0
while j < samplerate:
    a2[j] = amp_prbs
    a2[j+1] = 0
    j = j+2

i=0
prbs2 = np.zeros(samplerate, dtype=complex)
while b2[i]<np.size(prbs2):
    k = b2[i]
    prbs2[k:] = a2[i]
    i=i+1

#
rand_int = 0.5*np.pi * np.random.randint(0, 4, samplerate) # 0 to 3

#Periodic signal
P1 = 2 ** 12  # period
D1 = 2 ** 11   # width of pulse
periodicsig1 = 1*np.pi*(np.arange(samplerate) % P1 < D1)

#
P2 = 2 ** 14  # period
D2 = 2 ** 12   # width of pulse
periodicsig2 = 1*np.pi*(np.arange(samplerate) % P2 < D2)


#----

#randomintcol = np.zeros(samplerate)
#for ii in range(samplerate):
#    randomintcol[ii] = np.random.random_integers(2)


#signal1col = sine_signalcol
#signal1col = cosine_signalcol
#signal1col = randomintcol
#signal1col = random_signal
signal1col = prbs1
#signal1col = periodicsig1
#signal1col = np.zeros(samplerate, dtype=complex)


#signal2col = sine_signalcol
#signal2col = random_signal
signal2col = prbs2
#signal2col = periodicsig2
#signal2col = 0.5*np.pi*np.ones(samplerate)

#
oplcommon1 = 0 * np.pi #Common Path Length 1
oplcommon2 = 0 * np.pi #Common Path Length 2

#opl1 =100 
#opl2= 100
# Optical Path Length Difference (opl1-opl2) determines free spectral range as optical filter.

PT1 = 0.5 # PT: Power Transmission of first beam splitter

PT2_1 = 0.5 # PT: Power Transmission of second beam splitter of arm A
PT2_2 = 0.5 # PT: Power Transmission of second beam splitter of arm B

PT3_1 = 0.5 # PT: Power Transmission of third beam splitter of arm A
PT3_2 = 0.5 # PT: Power Transmission of third beam splitter of arm B

PT4 = 0.5 # PT: Power Transmission of 4th beam splitter
PT5 = 0.5 # PT: Power Transmission of 5th beam splitter

PT6_1 = 0.5 # PT: Power Transmission of 5th beam splitter
PT6_2 = 0.5 # PT: Power Transmission of 5th beam splitter

IPB1 = 0.5 * np.pi #In Phase Bias: Optical Phase delay between Arm A and B
IPB2 = 0 * np.pi #In Phase Bias: Optical Phase delay between Arm A and B

# Define Input Electric Field

# Input: Port 1 only
E1in = np.array([[1+0.j],[0-0.00j]])
#E1in = np.array([[0.707+0.707j],[0]])
#E1in = np.array([[-1+0j],[0-0.00j]])

# Input Both 1 and 2 port
#Ein1 = np.array([[1+0j],[1-0j]]) 
#Ein1 = np.array([[0.707+0.707j],[-0.707-0.707j]])
#Ein1 = np.array([[1 + 0j],[-1 - 0j]])

# Input Port 2 only
#Ein1 = np.array([[0],[1]]) 
#Ein1 = np.array([[0],[0.707+0.707j]])

E6out_p1_col = np.zeros(samplerate, dtype=complex)
E6out_p2_col = np.zeros(samplerate, dtype=complex)

E7out_p1_col = np.zeros(samplerate, dtype=complex)
E7out_p2_col = np.zeros(samplerate, dtype=complex)

E9_1out_port1col= np.zeros(samplerate, dtype=complex)
E9_1out_port2col= np.zeros(samplerate, dtype=complex)

E9_2out_port1col= np.zeros(samplerate, dtype=complex)
E9_2out_port2col= np.zeros(samplerate, dtype=complex)

#Tx

for ii in range(samplerate):

    t = tcol[ii]
    opl1 = 2*np.pi * freq1 * t

    E1out = mach_zender_interferometer_time_def.propagate1(opl1, opl1, E1in)
    E2in = E1out
    
    E2out = mach_zender_interferometer_time_def.beamsplitter(PT1, E2in)
    E3_1in = np.array([[E2out[0,0]],[0+0j]])

    #Arm 1

    E3_1out = mach_zender_interferometer_time_def.beamsplitter(PT2_1, E3_1in)  

    E4_1in = E3_1out       

    signal1 = signal1col[ii]  


    E4_1out = mach_zender_interferometer_time_def.propagate1(oplcommon1, oplcommon1+signal1, E4_1in) # Each path experience different path length
    E5_1in = E4_1out
    
    E5_1out = mach_zender_interferometer_time_def.beamsplitter(PT3_1, E5_1in) # Each path enter second beam splitter
    E6_1in = E5_1out

    E6_1out = mach_zender_interferometer_time_def.propagate1(oplcommon1, oplcommon1, E6_1in) # no delay for arm A

    E6out_port1 = E6_1out[0,0] #trans
    E6out_p1_col[ii] = E6out_port1 


    #Arm 2

    #E3_2in = np.array([[0+0j], [E2out[1,0]]])
    E3_2in = np.array([[E2out[1,0]], [0+0j]])   

    E3_2out = mach_zender_interferometer_time_def.beamsplitter(PT2_2, E3_2in)
    E4_2in = E3_2out
 
    signal2 = signal2col[ii]        

    E4_2out = mach_zender_interferometer_time_def.propagate1(oplcommon1, oplcommon1+signal2, E4_2in) # Each path experience different path length
    E5_2in = E4_2out

    E5_2out = mach_zender_interferometer_time_def.beamsplitter(PT3_2, E5_2in) # Each path enter second beam splitter
    E6_2in = E5_2out

    E6_2out = mach_zender_interferometer_time_def.propagate1(oplcommon1+IPB1, oplcommon1+IPB1, E6_2in) # Delay for arm B. Actually only one path couple to fourth beam splitter

    E6out_port2 = E6_2out[0,0] #trans
    E6out_p2_col[ii] = E6out_port2


    # Combine I + Q using fourth beam splitter

    E7_in = np.array([[E6_1out[0,0]], [E6_2out[0,0]]])

    E7_out = mach_zender_interferometer_time_def.beamsplitter(PT4, E7_in) # Each path enter fourth beam splitter
    
    #print(E7_out)
    #print("")

    E7out_port1 = E7_out[0,0] #trans
    E7out_p1_col[ii] = E7out_port1 

    #print(E7out_port1)
    #print("")

    E7out_port2 = E7_out[1,0] #reflect
    E7out_p2_col[ii] = E7out_port2

    #print(E7out_port2)
    #print("")

    #Receiver 

    E8_in = E7out_port1

    E8_out = mach_zender_interferometer_time_def.beamsplitter(PT5, E8_in) # Each path enter fifth beam splitter   
    
    #Local Oscillator
    losc_I_phase = opl1
    losc_Q_phase = losc_I_phase + IPB2

    Elosc_I = mach_zender_interferometer_time_def.propagate1(losc_I_phase, losc_I_phase, np.array([[0.25+0.0j],[0.0-0.0j]]))
    # Actually only one path couple to fourth beam splitter
    # 
    Elosc_Q = mach_zender_interferometer_time_def.propagate1(losc_Q_phase, losc_Q_phase, np.array([[0.25+0.0j],[0.0-0.0j]]))

    E9_1in = np.array([[E8_out[0,0]], [Elosc_I[0,0]]])

    #print(E9_1in)
    #print("")

    E9_2in = np.array([[E8_out[1,0]], [Elosc_Q[0,0]]])

    #print(E9_2in)
    #print("")


    E9_1out = mach_zender_interferometer_time_def.beamsplitter(PT6_1, E9_1in) # Each path enter sixth beam splitter   
    
    E9_2out = mach_zender_interferometer_time_def.beamsplitter(PT6_2, E9_2in) # Each path enter sixth beam splitter

    E9_1out_port1 = E9_1out[0,0] #trans
    E9_1out_port1col[ii] = E9_1out_port1

    E9_1out_port2 = E9_1out[1,0] #Reflect
    E9_1out_port2col[ii] = E9_1out_port2


    E9_2out_port1 = E9_2out[0,0] #trans
    E9_2out_port1col[ii] = E9_2out_port1

    E9_2out_port2 = E9_2out[1,0] #Reflect
    E9_2out_port2col[ii] = E9_2out_port2



fig1 = plt.figure(figsize = (10,8), facecolor='lightblue')

ax1 = fig1.add_subplot(6, 1, 1)
ax2 = fig1.add_subplot(6, 1, 2)
ax3 = fig1.add_subplot(6, 1, 3)
ax4 = fig1.add_subplot(6, 1, 4)
ax5 = fig1.add_subplot(6, 1, 5)
ax6 = fig1.add_subplot(6, 1, 6)

ax1.plot(tcol,signal1col, "-", color="c")
ax1.set_ylabel("digital signal [a.u.]")
#ax1.set_ylim(-1*np.pi,np.pi)
ax1.grid()

ax2.plot(tcol,np.real(E6out_p1_col), "-",color="c")
ax2.set_ylabel("Electric Field")

ax3.plot(tcol,signal2col, "-",color="y")
ax3.set_ylabel("digital signal [a.u.]")
ax3.grid()

ax4.plot(tcol,np.real(E6out_p2_col), "-",color="y")
ax4.set_ylabel("Electric Field")



ax5.plot(tcol,np.real(E7out_p1_col), "-",color="m")
ax5.set_ylim(-1.1,1.1)
ax5.set_ylabel("Electric Field")
ax5.grid()

ax6.plot(tcol,(np.abs(E7out_p1_col))**2, "-",color="m")
ax6.set_ylim(-0.1,1.1)
ax6.set_ylabel("Optical Power (Not measured)",{"fontsize": 6})
ax6.grid()



fig2 = plt.figure(figsize = (10,8), facecolor='lightblue')

ax21 = fig2.add_subplot(6, 1, 1)
ax22 = fig2.add_subplot(6, 1, 2)
ax23 = fig2.add_subplot(6, 1, 3)
ax24 = fig2.add_subplot(6, 1, 4)
ax25 = fig2.add_subplot(6, 1, 5)
ax26 = fig2.add_subplot(6, 1, 6)

ax21.plot(tcol, np.real(E9_2out_port1col), "-",color="c")
ax21.set_ylabel("Electric Field")
ax21.grid()

ax22.plot(tcol, (np.abs(E9_2out_port1col))**2, "-",color="c")
ax22.set_ylabel("Optical Power",{"fontsize": 6})
ax22.grid()


ax23.plot(tcol, np.real(E9_2out_port2col), "-",color="y")
ax23.set_ylabel("Electric Field")
ax23.grid()

ax24.plot(tcol, -1*(np.abs(E9_2out_port2col))**2, "-",color="y")
ax24.set_ylabel("Optical Power",{"fontsize": 6})
ax24.set_ylim(-0.1,0.21)
ax24.grid()

ax25.plot(tcol, (np.abs(E9_2out_port1col))**2, tcol, (np.abs(E9_2out_port2col))**2, "-")
ax25.set_ylabel("Optical Power",{"fontsize": 6})
ax25.grid()

ax26.plot(tcol, (np.abs(E9_2out_port1col))**2 - (np.abs(E9_2out_port2col))**2, "-",color="c")
ax26.set_ylabel("Optical Power (Balanced Photo Diode)",{"fontsize": 6})
ax26.grid()



fig3 = plt.figure(figsize = (10,8), facecolor='lightblue')

ax31 = fig3.add_subplot(6, 1, 1)
ax32 = fig3.add_subplot(6, 1, 2)
ax33 = fig3.add_subplot(6, 1, 3)
ax34 = fig3.add_subplot(6, 1, 4)
ax35 = fig3.add_subplot(6, 1, 5)
ax36 = fig3.add_subplot(6, 1, 6)

ax31.plot(tcol, np.real(E9_1out_port1col), "-",color="c")
ax31.set_ylabel("Electric Field")
ax31.grid()

ax32.plot(tcol, (np.abs(E9_1out_port1col))**2, "-",color="c")
ax32.set_ylabel("Optical Power",{"fontsize": 6})
ax32.grid()


ax33.plot(tcol, np.real(E9_1out_port2col), "-",color="y")
ax33.set_ylabel("Electric Field")
ax33.grid()

ax34.plot(tcol, -1*(np.abs(E9_1out_port2col))**2, "-",color="y")
ax34.set_ylabel("Optical Power",{"fontsize": 6})
ax34.set_ylim(-0.1,0.21)
ax34.grid()

ax35.plot(tcol, (np.abs(E9_1out_port1col))**2, tcol, (np.abs(E9_1out_port2col))**2, "-")
ax35.set_ylabel("Optical Power",{"fontsize": 6})
ax35.grid()

ax36.plot(tcol, (np.abs(E9_1out_port1col))**2 - (np.abs(E9_1out_port2col))**2, "-",color="c")
ax36.set_ylabel("Optical Power (Balanced Photo Diode)",{"fontsize": 6})
ax36.grid()


plt.show()