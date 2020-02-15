#! /usr/bin/env python3
#  coding = utf-8
from decimal import Decimal as DEC, Context
import sys
from enum import Enum
################################################################
class Type(Enum): #                                            _
    dl = 1 # disjoint left : --(----)---a---------b----------- _
    dr = 2 # disjoint right: -----------a---------b---(----)-- _
    sp = 3 # superset      : -----------a--(---)--b----------- _
    sb = 4 # subset        : --------(--a---------b--)-------- _
    xl = 5 # cross left    : --------(--a--)------b----------- _
    xr = 6 # cross right   : -----------a------(--b--)-------- _
################################################################
from math import floor, ceil
from itertools import combinations as combinat
import numpy as np
class Period: #                                                _
    # Ok ve vant vhen say 3.14 to be sure that it's 3.14 and   _
    # not 3.14000000000000012434497875801753252744674682617187 _
    # such funky numbers appears from simple substractions and _
    # might lead to unexpected results. For example floor of   _
    # 2.999999999999999999999999999999999999999999999999999998 _
    # Thatz why ve use Decimal but the floats has to be passed _
    # as strings otherwise we'll have the funky floats again.  _
    def __init__(self, a, b, n=-1): #                          _
        self.t = [DEC(str(t)) for t in (a, b)] # --- endpoints _
        self.n = n # ------------------------ number of guards _
    #                                                          _
    def __str__(self): # printable representation              _
        # center t within 5 spaces:                            _
        s = [format(t.__str__(), '^5s') for t in self.t] #     _
        s = ','.join(s) #                                      _
        if self.n < 0: return s #                              _
        return s + f':{self.n}' #                              _
    #                                                          _
    def __repr__(self): return self.__str__() # ------ zebuger _
    #                                                          _
    def get_type(self, t): # t should be [DEC,DEC] as well     _
        (a, b), (c, d) = self.t, t #              # scenarios: _
        if d <= a: return Type.dl #                          2 _
        if c >= b: return Type.dr #                          2 _
        if c >= a and d <= b: return Type.sp #               4 _
        if c <= a and d >= b: return Type.sb #               3 _
        if c < a and d > a: return Type.xl #                 1 _
        return Type.xr #                                     1 _
################################################################
# F # U # N # C # S # P # E # C # ! # ! # ! ##############v:1.1#
################################################################
#Okay####take##as####input####2###args###:##first#####a###list##
################################################################
##vith###Period###instances##,#and#####second###a##guard###duty#
#####time###interval##,###something#####like####classify(ls, t)#
################################################################
##Zen###make###a##loop###over###list###elements#{p}#for###each##
#####pair####(p, t)###determine####their###relationship###by####
################################################################
##calling###p.get_type(t),#than#####for####each####type##take###
###the####appropriate####action:################################
################################################################
   #[dl v dr]###DO### Nothing ##################################
################################################################
   #[sp]#### Here #### We ####### Have #### 4 #### scenarios: ##
################################################################
####1### p.t ### and ##### t ### endpoints ## are #### same ####
####### action: #### increment #### p.n ### vith ### 1 #########
################################################################
### 2. ## p.t ## & ###t## left ### endpoints #### are ## same ##
######## action: ###split###p.t###into##2##intervals############
######(t[0],t[1])##(t[1],p.t[1])###in##ze##first##interval######
################################################################
## increment ### nof guardians ###### vith ### one #############
################################################################
### 3) ### right ## endpoints #### are ##ze###same:#############
################################################################
#####split###to##(p.t[0],t[0])###(t[0],t[1])##### increment ####
###nof guards####in###ze##second###interval###by##1#############
################################################################
### 4 ##proper###subset:###split# into ###3###intervals:########
################################################################
#####(p.t[0],t[0]),###(t[0],t[1]),####(t[1],p.t[1])##,##########
##increment#### nof guards #####in###ze##middle###interval######
######by###one##################################################
################################################################
   #sb]##increment####p.n####by####van########)#################
################################################################
   #[xl]######split####p###by###t[1]####and##increment##########
####### nof guards ###in###ze##first###interval###by##1#########
################################################################
   #[xr]####split####p###by####t[0]###and##increment##ze########
#######nof guards###in##ze##second###interval###by###one########
################################################################
def classify(ls, t):
    j = 0 # ve are modifying ls on the fly zo ve are going to
          # use a vile loof vit an loofing index
    def insert_coin(a, b, n):
        nonlocal j
        ls.insert(j, Period(a, b, n))
        j += 1
    while j < len(ls): # wet'z gou
        p = ls[j]
        y = p.get_type(t).name
        j += 1
        if y is 'dl' or y is 'dr':
            continue ################################# do nofing
        elif y is 'sp': # here ve haaf 4 scenarios zo ve have to
                        # consider them each by turn:
            if p.t == t: #################### scenario namba uan
                p.n += 1
            elif p.t[0] == t[0]: ############ scenario namba tuu
                insert_coin(t[1], p.t[1], p.n)
                p.t[1] = t[1]
                p.n += 1
            elif p.t[1] == t[1]: ########### scenario namba dree
                insert_coin(t[0], t[1], p.n + 1)
                p.t[1] = t[0]
            else: ############################# scenario namba 4
                insert_coin(t[0], t[1], p.n + 1)
                insert_coin(t[1], p.t[1], p.n)
                p.t[1] = t[0]
        elif y is 'sb':
            p.n += 1
        elif y is 'xl':
            insert_coin(t[1], p.t[1], p.n)
            p.t[1] = t[1]
            p.n += 1
        else:
            insert_coin(t[0], p.t[1], p.n + 1)
            p.t[1] = t[0]
#########################################################_thats:
#   #   #   ####   ##   ##   ##   ############   ###   ###   ###
# C # A # T #### s ## p ## e ## c ############ v ### : ### 0 ###
#   #   #   ####   ##   ##   ##   ############   ###   ###   ###
################################################################
# yeah #########################################################
################################################################
#### O ### K ### A ### Y ###   ### L ### O ### O ### F ###   ###
# O ### V ### E ### R ###   ### l ### s ###   ### C ### O ### N
#### C ### A ### T ### E ### N ### A ### T ### E ###   ### A ###
# D ### J ### A ### C ### E ### N ### T ###   ### P ### e ### r
#### i ### o ### d ### s ###   ### W ### I ### T ### H ###   ###
# E ### Q ### U ### A ### L ###   ### n ###   ### U ### S ### E
####   ### A ### N ###   ### A ### U ### X ### I ### L ### A ###
# R ### Y ###   ### S ### T ### A ### C ### K ###   ### A ### N
#### D ###   ### 2 ###   ### V ### I ### L ### E ###   ### L ###
# O ### O ### F ### S ###   ###   ###   ###   ###   ###   ###
def cat(ls): ############################ I should have used con
    aux = [] ###################################################
    j = 0 ######################################################
    siz = len(ls) ##############################################
    while j < siz: #############################################
        p = ls[j] ##############################################
        while True: ############################################
            j += 1 #############################################
            if j < siz and ls[j].n == p.n: continue ############
            break ##############################################
        p.t[1] = ls[j - 1].t[1] ################################
        aux.append(p) ##########################################
        pass ###################################### take a break
    ls[:] = aux ################################################
################################################################
def getlistStr(ls): ############################################
    s = "" #####################################################
    for p in ls: s += p.__str__() + "\n" #######################
    return s[:-1] ######################## discard last new line
################################################################
def dmplist(msg, ls): print(msg, getlistStr(ls), sep='\n') #####
################################################################
# Okay # split # undercova # to # islands # such # that # each #
################################################################
# element's # neighborz # are # within # patch_size # range ####
################################################################
def archipelago(patch_size, undercova): ########################
    islands = [[undercova[0]]] #################################
    for p in undercova[1:]: ####################################
        if p.t[0] - islands[-1][-1].t[1] < patch_size: #########
            islands[-1].append(p) ##############################
        else: ##################################################
            islands.append([p]) ################################
    return islands #############################################
################################################################
# There a bunch of time intervals (grp) vhich have to be covered
# by a sequence of patches starting from the either end (align).
# To each patch interval corresponds a guard or two depending on
# the underlying periods. The function will return the total sum
# of guards needed to cover ze grp. The align argument takes two
# logical values: 0 for left and 1 for right alignment.
def cova(patch_size, grp, align): ##############################
    T = grp[-1].t[1] - grp[0].t[0] ################### time span
    _p = patch_size ################################### shortcut
    Np = ceil( T /_p ) ############################# nof patches
    p0 = grp[0].t[0] ######################## cova left endpoint
    if align: p0 -= Np*_p - T ###################### right align
    def GPI(t): return floor(( t - p0 )/_p) #### get patch index
    nof_guards = [1]*Np ############# number of guards per patch
    for g in grp: ##############################################
        if g.n == 1: continue ##################################
        ### Here we use the next_minus method to handle the case 
        # vhen t's right endpoint is on a patch boundary. ######
        j = [GPI(g.t[0]), ######################################
             GPI(g.t[1].next_minus(Context(prec=4)))] #########<
        for i in range(j[0], j[1] + 1): ########################
            nof_guards[i] = 2 ##################################
    return nof_guards, p0 ######################################
################################################################
## divide island according with the combo indices c, for example
###### div([1], ['a', 'b', 'c']) will return [['a'], ['b', 'c']]
def div(c, island): ############################################
    grp = [] ###################################################
    i = 0 #############################              ###########
    for j in c: #######################    x    x    ###########
        grp.append(island[i:j]) #######      oo      ###########
        i = j #########################      ""      ###########
    grp.append(island[i:]) ############    Yeah!?    ###########
    return grp ########################              ###########
################################################################
def fourfor(psiz, island): #####################################
    n = len(island) # nof periods ##############################
    slots = range(1, n) # division slots #######################
    stk = [] # stack ###########################################
    aux = [] # auxilary stack ##################################
    for k in range(n): ########################### division loop
        for c in list(combinat(slots, k)): ########## combo loop
            grp = div(c, island) ###############################
            for alignment in range(1 << (k + 1)): ### align loop
                for j in range(len(grp)): ########### group loop
                    align = ((1 << j) & alignment) >> j ########
                    stk.append(cova(psiz, grp[j], align)) ######
                # total number of guards #######################
                total = sum([sum(g[0]) for g in stk]) ##########
                aux.append((total, list(stk))) #################
                stk[:] = [] ####################################
    ###### Now we have to find and return the entry at aux which
    ########## corresponds to the minimum total number of guards
    j = np.argmin([a[0] for a in aux]) #########################
    return aux[j] ##############################################
################################################################
def _estTzone():
    #### Your code goes here, .. mua-ha-ha-ha ..
    ###############                 ^^
    sys.exit() ####                 ..  
################################################################
if __name__ == "__main__":
    end_time = 10
    ls = [Period(0, end_time, 0)]
    print(f"artGallery (OPEN/CLOSE): (0, {end_time})")
    guard_shedule = [Period(0, 3),
                     Period(2, 4),
                     Period(1, 5.2),
                     Period(4, 6),
                     Period(7, end_time)]
    dmplist("Guard Shedule:", guard_shedule)
    for duty in guard_shedule: classify(ls, duty.t)
    dmplist("After classify:", ls)
    cat(ls)
    dmplist("After cat(aka con):", ls)
    ########### filter only periods which has nof guards 0 or 1:
    ls = list(filter(lambda p: p.n < 2, ls))
    dmplist("Undercova:", ls) # nog nepeKpuTue!
    patch_size = DEC('.5')
    arch = archipelago(patch_size, ls)
    for i, island in enumerate(arch):
        dmplist(f"Island {i}", island)
        total, stk = fourfor(patch_size, island)
        print(f"{total} extra guards needed")
        for g in stk:
            print(f"Starting from {g[1]}:", g[0])
########################################################### log:
