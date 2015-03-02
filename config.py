checkmass = True              #checks that E^2-\vec{p}^2=m^2, using all the numbers from the LHE
checkmomentum = True          #checks momentum conservation in particle decays
checkcharge = True            #checks charge conservation in particle decays
counthiggsdecaytype = True    #prints the breakup of Higgs decay types
count4levents = True          #counts the total number of events with 4 leptons
countVHdecaytype = True       #prints the breakup of VH decay types
checklnu2qcharge = False      #for H->WW->lnu2q, checks the charge on the leptons

raiseerror = False            #if this is true, raises an IOError when something is wrong
                              #otherwise just prints it

momentumtolerance = 1e-4
masstolerance = 7e-2
