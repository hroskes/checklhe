import globalvariables

checkfirstline = True         #check that the first line in each event has the right syntax, and that the number of particles is correct
checkinvmass = True           #checks that E^2-\vec{p}^2=m^2, using all the numbers from the LHE
checkPDGmass = True           #checks that the LHE mass = the PDG mass for the particle types in checkPDGmasslist
checkmomentum = True          #checks momentum conservation in particle decays
checkcharge = True            #checks charge conservation in particle decays
checkcolor = True             #check that the color lines make sense
checkZZorWWassignment = True  #check that, in symmetric decays, the Zs/Ws are assigned so that one has mass as close as possible to m_Z/m_W

counthiggsdecaytype = True    #prints the breakup of Higgs decay types
count4levents = True          #counts the total number of events with 4 leptons
count2l2levents = True        #counts the total number of events with l+l- l+l-, where the first flavor and the second flavor
                              #  could be the same or different
countVHdecaytype = True       #prints the breakup of VH decay types
checklnu2qcharge = False      #for H->WW->lnu2q, checks the charge on the leptons

raiseerror = False            #if this is true, raises an IOError when something is wrong
                              #otherwise just prints it

makedecayanglestree = True    #For ZZ->4l events, makes a tree of costheta1, costheta2, and Phi
makeZZmassestree    = True    #For ZZ->4l events, makes a tree of the Z1, Z2, Higgs masses
tree = any([makedecayanglestree, makeZZmassestree])


momentumtolerance = 1e-4      #GeV
invmasstolerance = 7e-2       #GeV
PDGmasstolerance = 0.01       #relative



startedinit = False
finishedinit = False

def init():
    global startedinit, finishedinit
    global checkPDGmasslist
    if not startedinit:
        startedinit = True
        globalvariables.init()
        checkPDGmasslist = globalvariables.leptons
        finishedinit = True
