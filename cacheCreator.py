# -*- coding: utf-8 -*-

import os
import csv

cc1 = 0
cb1 = 0
ca1 = 0
cc2 = 0
cb2 = 0
ca2 = 0
ccc1 = 1
ccb1 = 1
cca1 = 1
ccc2 = 1
ccb2 = 1
cca2 = 1
x = 0

with open('data5.csv','ab') as f:
    writer=csv.writer(f)
    writer.writerow(['conjuntos il1','bytes il1','associativade il1','conjunto dl1','bytes dl1','associatividade dl1','tamanho il1','tamanho dl1','il1_hits','il1_misses','il1_writebacks','dl1_hits','dl1_misses','dl1_writebacks','TT','ET'])

while(True):
    
    # IL1
    if cc1 == 0:
        conjunto1 = 64
    elif cc1 == 1:
        conjunto1 = 128
    elif cc1 == 2:
        conjunto1 = 256

    if cb1 == 0:
        bpb1 = 32
    elif cb1 == 1:
        bpb1 = 64

    if ca1 == 0:
        assoc1 = 1
    elif ca1 == 1:
        assoc1 = 2
    elif ca1 == 2:
        assoc1 = 4
    
    # DL1
    if cc2 == 0:
        conjunto2 = 64
    elif cc2 == 1:
        conjunto2 = 128
    elif cc2 == 2:
        conjunto2 = 256

    if cb2 == 0:
        bpb2 = 32
    elif cb2 == 1:
        bpb2 = 64

    if ca2 == 0:
        assoc2 = 1
    elif ca2 == 1:
        assoc2 = 2
    elif ca2 == 2:
        assoc2 = 4

    # Gerador de cache DL1
    if cca2 == 1:
        ca2+=1
        if ca2>2:
            ca2 = 0
        cca2 = 0

    if ccb2 == 3:
        cb2+=1
        if cb2>1:
            cb2 = 0
        ccb2 = 0

    if ccc2 == 6:
        cc2+=1
        if cc2>2:
            cc2 = 0
        ccc2 = 0

    # Gerador de cache LD1
    if cca1 == 18:
        ca1+=1
        if ca1>2:
            ca1 = 0
        cca1 = 0

    if ccb1 == 54:
        cb1+=1
        if cb1>1:
            cb1 = 0
        ccb1 = 0

    if ccc1 == 108:
        cc1+=1
        if cc1>2:
            cc1 = 0
        ccc1 = 0 
    
    x+=1
    cca1+=1
    cca2+=1
    ccb1+=1
    ccb2+=1
    ccc1+=1
    ccc2+=1

    print "conjunto1: "+str(conjunto1)+" bpb1: "+str(bpb1)+" assoc1: "+str(assoc1)+" conjunto2: "+str(conjunto2)+" bpb2: "+str(bpb2)+" assoc2: "+str(assoc2)

    os.system("./sim-cache -cache:il1 il1:"+str(conjunto1)+":"+str(bpb1)+":"+str(assoc1)+":l -cache:il2 none -cache:dl1 dl1:"+str(conjunto2)+":"+str(bpb2)+":"+str(assoc2)+":l -cache:dl2 none -redir:sim Cache/relatorio.txt Cache/benchmarks/amp.ss") #-max:inst 40000000

    tamanho_il1 = conjunto1*bpb1*assoc1
    tamanho_dl1 = conjunto2*bpb2*assoc2

    file_object  = open("Cache/relatorio.txt", "r")

    relatorio = file_object.read()

    # IL1.HITS (NCH1)
    a,b = relatorio.split("il1.hits")   # split line
    c,d = b.split("il1.misses")         # split bottom

    il1_hits = c.replace(" ", "")
    il1_hits = il1_hits.replace("#totalnumberofhits", "")
    il1_hits = il1_hits.replace("\n", "")

    # IL1.MISSES (NCM1)
    a,b = relatorio.split("il1.misses")   # split line
    c,d = b.split("il1.replacements")     # split bottom

    il1_misses = c.replace(" ", "")
    il1_misses = il1_misses.replace("#totalnumberofmisses", "")
    il1_misses = il1_misses.replace("\n", "")

    # IL1.WRITEBACKS (NWB1)
    a,b = relatorio.split("il1.writebacks")   # split line
    c,d = b.split("il1.invalidations")        # split bottom

    il1_writebacks = c.replace(" ", "")
    il1_writebacks = il1_writebacks.replace("#totalnumberofwritebacks", "")
    il1_writebacks = il1_writebacks.replace("\n", "")

    # DL1.HITS (NCH2)
    a,b = relatorio.split("dl1.hits")   # split line
    c,d = b.split("dl1.misses")         # split bottom

    dl1_hits = c.replace(" ", "")
    dl1_hits = dl1_hits.replace("#totalnumberofhits", "")
    dl1_hits = dl1_hits.replace("\n", "")

    # DL1.MISSES (NCM2)
    a,b = relatorio.split("dl1.misses")   # split line
    c,d = b.split("dl1.replacement")      # split bottom

    dl1_misses = c.replace(" ", "")
    dl1_misses = dl1_misses.replace("#totalnumberofmisses", "")
    dl1_misses = dl1_misses.replace("\n", "")

    # DL1.WRITEBACKS (NWB2)
    a,b = relatorio.split("dl1.writebacks")   # split line
    c,d = b.split("dl1.invalidations")        # split bottom

    dl1_writebacks = c.replace(" ", "")
    dl1_writebacks = dl1_writebacks.replace("#totalnumberofwritebacks", "")
    dl1_writebacks = dl1_writebacks.replace("\n", "")

    print il1_hits
    print il1_misses
    print il1_writebacks
    print dl1_hits
    print dl1_misses
    print dl1_writebacks

    with open('cacti65/cache.cfg', 'r') as file:
        data = file.readlines()
    data[1] = "-size (bytes) "+str(tamanho_il1)+"\n"
    data[4] = "-block size (bytes) "+str(bpb1)+"\n"
    data[8] = "-associativity "+str(assoc1)+"\n"
    with open('cacti65/cache.cfg', 'w') as file:
        file.writelines( data )

    cacti = os.popen("./cacti65/cacti -infile cacti65/cache.cfg").read()

    # ACCESS TIME (ns)
    a,b = cacti.split("Access time (ns):")   # split line
    c,d = b.split("Cycle time (ns):")        # split bottom

    access_time1 = c.replace(" ", "")
    access_time1 = access_time1.replace("\n", "")

    # READ ENERGY (nJ)
    a,b = cacti.split("Read Energy (nJ):")   # split line
    c,d = b.split("Write Energy (nJ):")      # split bottom

    read_energy1 = c.replace(" ", "")
    read_energy1 = read_energy1.replace("\n", "")

    print access_time1
    print read_energy1

    with open('cacti65/cache.cfg', 'r') as file:
        data = file.readlines()
    data[1] = "-size (bytes) "+str(tamanho_dl1)+"\n"
    data[4] = "-block size (bytes) "+str(bpb2)+"\n"
    data[8] = "-associativity "+str(assoc2)+"\n"
    with open('cacti65/cache.cfg', 'w') as file:
        file.writelines( data )

    cacti = os.popen("./cacti65/cacti -infile cacti65/cache.cfg").read()

    # ACCESS TIME (ns)
    a,b = cacti.split("Access time (ns):")   # split line
    c,d = b.split("Cycle time (ns):")        # split bottom

    access_time2 = c.replace(" ", "")
    access_time2 = access_time2.replace("\n", "")

    # READ ENERGY (nJ)
    a,b = cacti.split("Read Energy (nJ):")   # split line
    c,d = b.split("Write Energy (nJ):")      # split bottom

    read_energy2 = c.replace(" ", "")
    read_energy2 = read_energy2.replace("\n", "")

    print access_time2
    print read_energy2

    nch1 = float(il1_hits)
    ncm1 = float(il1_misses)
    nwb1 = float(il1_writebacks)

    nch2 = float(dl1_hits)
    ncm2 = float(dl1_misses)
    nwb2 = float(dl1_writebacks)

    lamp = 13.6692
    eamp = 8.64848

    lac1 = float(access_time1)
    eac1 = float(read_energy1)
    lac2 = float(access_time2)
    eac2 = float(read_energy2)

    tt1 = nch1*lac1 + ncm1*lac1 + ncm1*lamp + nwb1*lamp
    et1 = nch1*eac1 + ncm1*eac1 + ncm1*eamp + nwb1*eamp

    tt2 = nch2*lac2 + ncm2*lac2 + ncm2*lamp + nwb2*lamp
    et2 = nch2*eac2 + ncm2*eac2 + ncm2*eamp + nwb2*eamp

    tt = tt1+tt2
    et = et1+et2

    print "tt: "+str(tt)
    print "et: "+str(et)

    with open('data5.csv','ab') as f:
        writer=csv.writer(f)
        writer.writerow([conjunto1,bpb1,assoc1,conjunto2,bpb2,assoc2,tamanho_il1,tamanho_dl1,il1_hits,il1_misses,il1_writebacks,dl1_hits,dl1_misses,dl1_writebacks,tt,et])

    if x == 324:
        break
