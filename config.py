import globalvariables

#syntax checks
checkfirstline = True         #check that the first line in each event has the right syntax, and that the number of particles is correct
checkstatus = True            #check that the particle status is correct

#kinematic checks
checkinvmass = True           #check that E^2-\vec{p}^2=m^2, using all the numbers from the LHE
checkPDGmass = True           #check that the LHE mass = the PDG mass for the particle types in checkPDGmasslist
                              #   (configured below)
checkmomentum = True          #check momentum conservation in particle decays
checkcharge = True            #check charge conservation in particle decays
checkcolor = True             #check that the color lines make sense

#decay counts and checks
checkZZorWWassignment = True  #check that, in symmetric decays, the Zs/Ws are assigned so that one has mass as close as possible to m_Z/m_W
counthiggsdecaytype = True    #prints the breakup of Higgs decay types
count4levents = True          #counts the total number of events with 4 leptons
count2l2levents = True        #counts the total number of events with l+l- l+l-, where the first flavor and the second flavor
                              #  could be the same or different
counttauaseormu = True        #When looking for l+l- l+l-, allow tau to stand in place of either e or mu, because taus can decay to either
countallleptonnumbers = False #count events with 1 lepton, 2 leptons, ...
countVHdecaytype = True       #prints the breakup of VH decay types
checklnu2qcharge = False      #for H->WW->lnu2q, check the charge on the leptons instead of the lepton flavor

raiseerror = False            #if this is true, raise an IOError when something is wrong
                              #otherwise just print it

#Make tree
makedecayanglestree = True    #For ZZ->4l events, makes a tree of costheta1, costheta2, and Phi
makeZZmassestree    = True    #For ZZ->4l events, makes a tree of the Z1, Z2, Higgs masses
tree = any([makedecayanglestree, makeZZmassestree])


#tolerances
momentumtolerance = 1e-4      #GeV
invmasstolerance = 7e-2       #GeV
PDGmasstolerance = 0.01       #relative


#mostly internal, until the row of #####
startedinit = False
finishedinit = False

def init():
    global startedinit, finishedinit
    global checkPDGmasslist
    if not startedinit:
        startedinit = True
        globalvariables.init()
####################################################
#the stuff in here is configurable
        checkPDGmasslist = globalvariables.globalvariables.leptons
####################################################
        finishedinit = True
