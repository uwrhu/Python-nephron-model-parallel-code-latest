from defs import *
import copy
import set_params 
import flux
import numpy as np
import equations
import electrochemical
import water
from values import *
import Newton
import timeit
import boundaryBath
import time

def compute(N,filename,method,sup_or_jux=None,diabete='Non',humOrrat = 'human',sup_or_multi = 'superficial',inhibition=None,unx = 'Y'):

    start=timeit.default_timer()

    cell = [membrane() for i in range(N)]
    # initialize the species of cell: human or rat.
    if humOrrat == 'human':
        for i in range(N):
            cell[i].humOrrat = 'hum'
    elif humOrrat == 'rat':
        for i in range(N):
            cell[i].humOrrat = 'rat'
    # the diabetic status of cell.
    if diabete != None:
        for i in range(N):
            cell[i].diabete = diabete
    else:
        print('What is diabete status?')    
    # superficial nephron or juxtamedullary nephron
    for i in range(N):
        cell[i].type = sup_or_jux
    
    for i in range(N):
        if inhibition == None:
            cell[i].inhib = ''
        else:
            cell[i].inhib = inhibition
    for i in range(N):
        cell[i].unx = unx
    # initialize intersitital concentration and read parameters.
    for i in range(N):
        set_params.read_params(cell[i],filename,i)
        boundaryBath.boundaryBath(cell[i],i)

    if cell[0].segment == 'PT':
        # Initial concentrations in Lumen at entrance of PT should be the same as in Bath:
        # cell[0].conc[:,0] = cell[0].conc[:,5]
        if cell[0].diabete != 'Non' and cell[0].humOrrat == 'rat':
            if cell[0].sex == 'male':
                if cell[0].segment == 'PT' and cell[0].type == 'sup':
                    cell[0].vol[0] = 0.0075
                    cell[0].vol_init[0] = cell[0].vol[0]
                if cell[0].segment == 'PT' and cell[0].type != 'sup':
                    cell[0].vol[0] = 0.008775
                    cell[0].vol_init[0] = cell[0].vol[0]
            elif cell[0].sex == 'female':
                if cell[0].segment == 'PT' and cell[0].type == 'sup':
                    cell[0].vol[0] = 0.004*1.5
                    cell[0].vol_init[0] = cell[0].vol[0]
                if cell[0].segment == 'PT' and cell[0].type != 'sup':
                    cell[0].vol[0] = 0.006*1.17
                    cell[0].vol_init[0] = cell[0].vol[0]
  
    # read data from output of previous segement.
    if cell[0].segment == 'S3':
        inputfile = open('PToutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','r')
        for i in range(NS):
            line = inputfile.readline()
            conclist = line.split(' ')
            cell[0].conc[i,0] = float(conclist[0])
            cell[0].conc[i,1] = float(conclist[1])
            cell[0].conc[i,4] = float(conclist[2])
        line_vol = inputfile.readline()
        vollist = line_vol.split(' ')
        cell[0].vol[0] = float(vollist[0])
        cell[0].vol[1] = float(vollist[1])
        cell[0].vol[4] = float(vollist[2])
        line_ep = inputfile.readline()
        eplist = line_ep.split(' ')
        cell[0].ep[0] = float(eplist[0])
        cell[0].ep[1] = float(eplist[1])
        cell[0].ep[4] = float(eplist[2])
        line_pres = inputfile.readline()
        preslist = line_pres.split(' ')
        cell[0].pres[0] = float(preslist[0])

    if cell[0].segment == 'SDL':
        inputfile = open('S3outlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','r')
        for i in range(NS):
            line = inputfile.readline()
            conclist = line.split(' ')
            cell[0].conc[i,0] = float(conclist[0])
        line_vol = inputfile.readline()
        vollist = line_vol.split(' ')
        cell[0].vol[0] = float(vollist[0])
        line_ep = inputfile.readline()
        eplist = line_ep.split(' ')
        cell[0].ep[0] = float(eplist[0])
        line_pres = inputfile.readline()
        preslist = line_pres.split(' ')
        cell[0].pres[0] = float(preslist[0])
        for i in range(N):
            cell[i].conc[:,1] = cell[i].conc[:,5]
            cell[i].conc[:,4] = cell[i].conc[:,5]

    if cell[0].segment == 'LDL':
        inputfile = open('SDLoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','r')
        for i in range(NS):
            line = inputfile.readline()
            conclist = line.split(' ')
            cell[0].conc[i,0] = float(conclist[0])
        line_vol = inputfile.readline()
        vollist = line_vol.split(' ')
        cell[0].vol[0] = float(vollist[0])
        line_ep = inputfile.readline()
        eplist = line_ep.split(' ')
        cell[0].ep[0] = float(eplist[0])
        line_pres = inputfile.readline()
        preslist = line_pres.split(' ')
        cell[0].pres[0] = float(preslist[0])

    if cell[0].segment == 'LAL':
        inputfile = open('LDLoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','r')
        for i in range(NS):
            line = inputfile.readline()
            conclist = line.split(' ')
            cell[0].conc[i,0] = float(conclist[0])
        line_vol = inputfile.readline()
        vollist = line_vol.split(' ')
        cell[0].vol[0] = float(vollist[0])
        line_ep = inputfile.readline()
        eplist = line_ep.split(' ')
        cell[0].ep[0] = float(eplist[0])
        line_pres = inputfile.readline()
        preslist = line_pres.split(' ')
        cell[0].pres[0] = float(preslist[0])

    if cell[0].segment == 'mTAL':
        if cell[0].type == 'sup':
            inputfile = open('SDLoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','r')
        else:
            inputfile = open('LALoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','r')
        for i in range(NS):
            line = inputfile.readline()
            conclist = line.split(' ')
            cell[0].conc[i,0] = float(conclist[0])
        line_vol = inputfile.readline()
        vollist = line_vol.split(' ')
        cell[0].vol[0] = float(vollist[0])
        line_ep = inputfile.readline()
        eplist = line_ep.split(' ')
        cell[0].ep[0] = float(eplist[0])
        line_pres = inputfile.readline()
        preslist = line_pres.split(' ')
        cell[0].pres[0] = float(preslist[0])

    if cell[0].segment == 'cTAL':
        inputfile = open('mTALoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','r')
        for i in range(NS):
            line = inputfile.readline()
            conclist = line.split(' ')
            cell[0].conc[i,0] = float(conclist[0])
        line_vol = inputfile.readline()
        vollist = line_vol.split(' ')
        cell[0].vol[0] = float(vollist[0])
        line_ep = inputfile.readline()
        eplist = line_ep.split(' ')
        cell[0].ep[0] = float(eplist[0])
        line_pres = inputfile.readline()
        preslist = line_pres.split(' ')
        cell[0].pres[0] = float(preslist[0])

    if cell[0].segment == 'MD':
        inputfile = open('cTALoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','r')
        for i in range(NS):
            line = inputfile.readline()
            conclist = line.split(' ')
            cell[0].conc[i,0] = float(conclist[0])
        line_vol = inputfile.readline()
        vollist = line_vol.split(' ')
        cell[0].vol[0] = float(vollist[0])
        line_ep = inputfile.readline()
        eplist = line_ep.split(' ')
        cell[0].ep[0] = float(eplist[0])
        line_pres = inputfile.readline()
        preslist = line_pres.split(' ')
        cell[0].pres[0] = float(preslist[0])    

    if cell[0].segment == 'DCT':
        inputfile = open('cTALoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','r')
        for i in range(NS):
            line = inputfile.readline()
            conclist = line.split(' ')
            cell[0].conc[i,0] = float(conclist[0])
        line_vol = inputfile.readline()
        vollist = line_vol.split(' ')
        cell[0].vol[0] = float(vollist[0])
        line_ep = inputfile.readline()
        eplist = line_ep.split(' ')
        cell[0].ep[0] = float(eplist[0])
        line_pres = inputfile.readline()
        preslist = line_pres.split(' ')
        cell[0].pres[0] = float(preslist[0])

    if cell[0].segment == 'CNT':
        #print(cell[0].sex,cell[0].humOrrat,sup_or_jux)
        inputfile = open('DCToutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','r')
        for i in range(NS):
            line = inputfile.readline()
            conclist = line.split(' ')
            cell[0].conc[i,0] = float(conclist[0])
        line_vol = inputfile.readline()
        vollist = line_vol.split(' ')
        cell[0].vol[0] = float(vollist[0])
        for k in range(N):
            cell[k].vol_init[0] = cell[0].vol[0]
        line_ep = inputfile.readline()
        eplist = line_ep.split(' ')
        cell[0].ep[0] = float(eplist[0])
        line_pres = inputfile.readline()
        preslist = line_pres.split(' ')
        cell[0].pres[0] = float(preslist[0])

    if cell[0].segment == 'CCD':
        if sup_or_multi == 'multiple':
            nephs = ['sup','jux1','jux2','jux3','jux4','jux5']
            soluts_flow = [0 for i in range(NS)]
            if humOrrat == 'rat':
                neph_weight = [2/3,(1/3)*0.4,(1/3)*0.3,(1/3)*0.15,(1/3)*0.1,(1/3)*0.05]
            elif humOrrat == 'human':
                neph_weight = [0.85,(0.15)*0.4,(0.15)*0.3,(0.15)*0.15,(0.15)*0.1,(0.15)*0.05]
            water_vol = []
            for neph in nephs:
                soluts_conc = []
                inputfile = open('CNToutlet'+cell[0].sex+cell[0].humOrrat+'_'+neph+'.txt','r')
                for i in range(NS):
                    line = inputfile.readline()
                    conclist = line.split(' ')
                    soluts_conc.append(float(conclist[0]))
            
                line_vol = inputfile.readline()
                vollist = line_vol.split(' ')
                water_vol.append(float(vollist[0]))
                soluts_flow = [soluts_flow[i]+neph_weight[nephs.index(neph)]*soluts_conc[i]*float(vollist[0]) for i in range(NS)]
                
                line_ep = inputfile.readline()
                line_pres = inputfile.readline()
            cell[0].vol[0] = 0
            for i in range(len(nephs)):
                cell[0].vol[0]=cell[0].vol[0]+neph_weight[i]*water_vol[i]

            cell[0].pres[0] = 6.2
            for i in range(NS):
                cell[0].conc[i,0] = soluts_flow[i]/cell[0].vol[0]

            for k in range(N):
                cell[k].vol_init[0] = cell[0].vol[0]
        elif sup_or_multi == 'superficial':
            inputfile = open('CNToutlet'+cell[0].sex+cell[0].humOrrat+'_sup.txt','r')
            for i in range(NS):
                line = inputfile.readline()
                conclist = line.split(' ')
                cell[0].conc[i,0] = float(conclist[0])
            line_vol = inputfile.readline()
            vollist = line_vol.split(' ')
            cell[0].vol[0] = float(vollist[0])
            for k in range(N):
                cell[k].vol_init[0] = cell[0].vol[0]
            line_ep = inputfile.readline()
            eplist = line_ep.split(' ')
            cell[0].ep[0] = float(eplist[0])
            line_pres = inputfile.readline()
            preslist = line_pres.split(' ')
            cell[0].pres[0] = float(preslist[0])

    if cell[0].segment == 'OMCD':
        inputfile = open('CCDoutlet'+cell[0].sex+cell[0].humOrrat+'.txt','r')
        for i in range(NS):
            line = inputfile.readline()
            conclist = line.split(' ')
            cell[0].conc[i,0] = float(conclist[0])
        line_vol = inputfile.readline()
        vollist = line_vol.split(' ')
        cell[0].vol[0] = float(vollist[0])
        for k in range(N):
            cell[k].vol_init[0] = cell[0].vol[0]
        line_ep = inputfile.readline()
        eplist = line_ep.split(' ')
        cell[0].ep[0] = float(eplist[0])
        line_pres = inputfile.readline()
        preslist = line_pres.split(' ')
        cell[0].pres[0] = float(preslist[0])

    if cell[0].segment == 'IMCD':
        inputfile = open('OMCDoutlet'+cell[0].sex+cell[0].humOrrat+'.txt','r')
        for i in range(NS):
            line = inputfile.readline()
            conclist = line.split(' ')
            cell[0].conc[i,0] = float(conclist[0])
        line_vol = inputfile.readline()
        vollist = line_vol.split(' ')
        cell[0].vol[0] = float(vollist[0])
        line_ep = inputfile.readline()
        eplist = line_ep.split(' ')
        cell[0].ep[0] = float(eplist[0])
        line_pres = inputfile.readline()
        preslist = line_pres.split(' ')
        cell[0].pres[0] = float(preslist[0])

    # initial guess of unknowns
    for i in range(N-1):
        print(i+1)
        celln = copy.deepcopy(cell[i+1])
        dx = 1.0e-3
        if cell[0].segment == 'PT' or cell[0].segment == 'S3' or cell[0].segment =='SDL' or cell[0].segment == 'LDL' or cell[0].segment == 'LAL' or cell[0].segment == 'mTAL' or cell[0].segment == 'cTAL' or cell[0].segment == 'MD' or cell[0].segment == 'DCT' or cell[0].segment == 'IMCD':
            x = np.zeros(3*NS+7)

            x[0:NS] = cell[i].conc[:,0]
            x[NS:2*NS] = cell[i].conc[:,1]
            x[2*NS:3*NS] = cell[i].conc[:,4]
    
            x[3*NS] = cell[i].vol[0]
            x[3*NS+1] = cell[i].vol[1]
            x[3*NS+2] = cell[i].vol[4]
 
            x[3*NS+3] = cell[i].ep[0]
            x[3*NS+4] = cell[i].ep[1]
            x[3*NS+5] = cell[i].ep[4]
    
            x[3*NS+6] = cell[i].pres[0]

        elif cell[0].segment == 'CNT' or cell[0].segment == 'CCD' or cell[0].segment == 'OMCD':
            x=np.zeros(5*NS+11)
            for j in range(15):
                x[5*j]=cell[i].conc[j,0]
                x[5*j+1]=cell[i].conc[j,1]
                x[5*j+2]=cell[i].conc[j,2]
                x[5*j+3]=cell[i].conc[j,3]
                x[5*j+4]=cell[i].conc[j,4]
            for j in range(NC-1):
                x[5*NS+j]=cell[i].vol[j]
                x[5*NS+5+j]=cell[i].ep[j]
            x[5*NS+10]=cell[i].pres[0]
    
        else:
            x = np.zeros(NS+3)
            x[0:NS] = cell[i].conc[:,0]
            x[NS] = cell[i].vol[0]
            x[NS+1] = cell[i].pres[0]
            x[NS+2] = -1 
    
        # set up nonlinear system
        equations.conservation_init (cell[i],cell[i+1],celln,dx)
        fvec = equations.conservation_eqs (x,i)
        
        # if cell[i].segment == 'PT':
        #     print(fvec)
        #     pause = input()

        # solving the system
        if method == 'Newton':
            if humOrrat == 'human':
                sol = Newton.newton_human(equations.conservation_eqs,x,i,cell[i])
            elif humOrrat == 'rat':
                sol = Newton.newton_rat(equations.conservation_eqs,x,i,cell[i])
            else:
                print('humOrrat: '+humOrrat)
                raise Exception('human or rat required')
        elif method == 'Broyden':
            sol = Newton.broyden(equations.conservation_eqs,x,i,cell[i].segment)
    
        if cell[0].segment == 'PT' or cell[0].segment == 'S3' or cell[0].segment =='SDL' or cell[0].segment == 'LDL' or cell[0].segment == 'LAL' or cell[0].segment == 'mTAL' or cell[0].segment == 'cTAL' or cell[0].segment == 'MD' or cell[0].segment == 'DCT' or cell[0].segment == 'IMCD':
            cell[i+1].conc[:,0] = sol[0:NS]
            cell[i+1].conc[:,1] = sol[NS:NS*2]
            cell[i+1].conc[:,4] = sol[NS*2:NS*3]

            cell[i+1].vol[0] = sol[3*NS]
            cell[i+1].vol[1] = sol[3*NS+1]
            cell[i+1].vol[4] = sol[3*NS+2]
    
            cell[i+1].ep[0] = sol[3*NS+3]
            cell[i+1].ep[1] = sol[3*NS+4]
            cell[i+1].ep[4] = sol[3*NS+5]
    
            cell[i+1].pres[0] = sol[3*NS+6]
        elif cell[0].segment == 'CNT' or cell[0].segment == 'CCD' or cell[0].segment == 'OMCD':
            for j in range(15):
                cell[i+1].conc[j,0] = sol[5*j]
                cell[i+1].conc[j,1] = sol[5*j+1] 
                cell[i+1].conc[j,2] = sol[5*j+2]
                cell[i+1].conc[j,3] = sol[5*j+3]
                cell[i+1].conc[j,4] = sol[5*j+4]

            for j in range(NC-1):
                cell[i+1].vol[j] = sol[5*NS+j]
                cell[i+1].ep[j] = sol[5*NS+5+j]
    
            cell[i+1].pres[0] = sol[5*NS+10]        
    
        print('\n')
        

#================================OUTPUT IN TO FILE================================

    if cell[0].segment == 'PT':
        file=open('PToutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4],cell[N-1].conc[j,5]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))
        file.close()

    elif cell[0].segment == 'S3':
        file=open('S3outlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))
        file.close()
    elif cell[0].segment == 'SDL':
        file=open('SDLoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))
        file.close()
    elif cell[0].segment == 'LDL':
        file=open('LDLoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4],cell[N-1].conc[j,5]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))
        file.close()
    elif cell[0].segment == 'LAL':
        file=open('LALoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4],cell[N-1].conc[j,5]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))
        file.close()
    elif cell[0].segment == 'mTAL':
        file=open('mTALoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))
        file.close()
    elif cell[0].segment == 'cTAL':
        file=open('cTALoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4],cell[N-1].conc[j,5]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))
        file.close()
    elif cell[0].segment == 'MD':
        file=open('MDoutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))
        file.close()
    elif cell[0].segment == 'DCT':
        file=open('DCToutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))
        file.close()
    elif cell[0].segment == 'CNT':
        file=open('CNToutlet'+cell[0].sex+cell[0].humOrrat+'_'+sup_or_jux+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,2],cell[N-1].conc[j,3],cell[N-1].conc[j,4]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[2],cell[N-1].vol[3],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[2],cell[N-1].ep[3],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))        
        file.close()
    elif cell[0].segment == 'CCD':
        file=open('CCDoutlet'+cell[0].sex+cell[0].humOrrat+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,2],cell[N-1].conc[j,3],cell[N-1].conc[j,4]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[2],cell[N-1].vol[3],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[2],cell[N-1].ep[3],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))    
        file.close()
    elif cell[0].segment == 'OMCD':
        file=open('OMCDoutlet'+cell[0].sex+cell[0].humOrrat+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,2],cell[N-1].conc[j,3],cell[N-1].conc[j,4]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[2],cell[N-1].vol[3],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[2],cell[N-1].ep[3],cell[N-1].ep[4]))        
        file.write(str(cell[N-1].pres[0]))
        file.close()
    elif cell[0].segment == 'IMCD':
        file=open('IMCDoutlet'+cell[0].sex+cell[0].humOrrat+'.txt','w')
        for j in range(NS):
            file.write('{} {} {} \n'.format(cell[N-1].conc[j,0],cell[N-1].conc[j,1],cell[N-1].conc[j,4]))
        file.write('{} {} {} \n'.format(cell[N-1].vol[0],cell[N-1].vol[1],cell[N-1].vol[4]))
        file.write('{} {} {} \n'.format(cell[N-1].ep[0],cell[N-1].ep[1],cell[N-1].ep[4]))
        file.write(str(cell[N-1].pres[0]))
        file.close()
    

    number_of_cell = [i for i in range(1,200)]
    solute = ['Na','K','Cl','HCO3','H2CO3','CO2','HPO4','H2PO4','urea','NH3','NH4','H','HCO2','H2CO2','glu']
    compart = ['Lumen','Cell','ICA','ICB','LIS','Bath']

    stop=timeit.default_timer()
    ComputationTime=stop-start
    if cell[0].segment == 'CCD' or cell[0].segment == 'OMCD' or cell[0].segment == 'IMCD':
        print('Computation Time for %s = %f'%(cell[0].segment, ComputationTime))
    else:
        print('Computation Time for %s %s = %f'%(cell[0].type, cell[0].segment,ComputationTime))
    print('\n')

    file=open('ComputationTime.txt','a')
    if cell[0].segment == 'CCD' or cell[0].segment == 'OMCD' or cell[0].segment == 'IMCD':
        file.write('Computation Time for %s: %f \n' %(cell[0].segment, ComputationTime))
    else:
        file.write('Computation Time for %s %s: %f \n' %(cell[0].type,cell[0].segment,ComputationTime))
    file.close()


    return cell
