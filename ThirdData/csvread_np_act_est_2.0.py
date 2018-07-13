import csv
import numpy as np

def csvRNS(csvName, col_num):
    import csv
    file = open(csvName)
    csv = csv.reader(file)

    col_val =[]
    i = True
    # col_val.append(csv[0][col_num])
    for row in csv:
        if (i == False):
            col_val.append(row[col_num])
        if (i == True):
            col_names = row
            i = False
    col_val.sort()
    return col_val

def cardCnt (csvName):
    len(csvRNS(csvName, 0))
    return len(csvRNS(csvName, 0))

def vectorTup(col_val_table, col_val_TM):
    tmp = 0
    NDV_tup_cnt = []
    len_TM = len(col_val_TM)
    row_val = ''
    hold = 0

    for j in col_val_table:
        for k in range(hold, len_TM):
            hold = hold + 1
            row_val = col_val_TM[k]
            if (j != row_val): # j does not exist in k
                hold = hold - 1
                break
            elif (j==row_val):
                tmp = tmp + 1
                if (hold == len_TM):
                    break
        #temp_tup = j, tmp
        temp_tup = tmp
        NDV_tup_cnt.append(tmp)
        tmp = 0
    return NDV_tup_cnt

def createVecTup(TableName, col_num_T, TMName, col_num_TM):
    col_val_T = csvRNS(TableName, col_num_T)
    col_val_TM = csvRNS(TMName, col_num_TM)
    return vectorTup(col_val_T, col_val_TM)

def SumOfVecMulp(TableName, TMName_left, TMName_right):
    VTres_left_under = createVecTup(TableName, 0, TMName_left, 1)
    VTres_right_upper = createVecTup(TableName, 0, TMName_right, 0)
    return sum(np.multiply(VTres_left_under,VTres_right_upper))

#result = createVecTup('UC.csv', 0, 'GaaUC.csv',1)

#print SumOfVecMulp('UC.csv', 'GaaUC.csv', 'UCaaUCS.csv')
#print SumOfVecMulp('UCS.csv', 'UCaaUCS.csv', 'UCSaaEC.csv')
#print SumOfVecMulp('EC.csv', 'UCSaaEC.csv', 'ECaaECS.csv')
#

def card_est(TableName_left, TableName_mid, TableName_right, TMName_left, TMName_right):
    SVM_LEFT_MID_RIGHT = SumOfVecMulp(TableName_mid, TMName_left, TMName_right)
    VTres_left_upper = createVecTup(TableName_left, 0, TMName_left, 0)
    VTres_right_lower = createVecTup(TableName_right, 0, TMName_right, 1)
    len_left_upper = len(VTres_left_upper)
    len_right_lower = len(VTres_right_lower)
    sum_left_upper = sum(VTres_left_upper)
    sum_right_lower = sum(VTres_right_lower)
    card_upper_est = []
    card_lower_est = []

    card_upper_est = np.multiply(VTres_left_upper, float(SVM_LEFT_MID_RIGHT)/sum_left_upper)
    card_lower_est = np.multiply(VTres_right_lower, float(SVM_LEFT_MID_RIGHT)/sum_right_lower)
    return SVM_LEFT_MID_RIGHT, card_upper_est.tolist(), card_lower_est.tolist()

def cardComp(TableName_left, TableName_mid, TableName_right, TMName_left, TMName_right, TableName_joinRes):
    (SVM_EST, card_upper_est, card_lower_est) = card_est(TableName_left, TableName_mid, TableName_right, TMName_left, TMName_right)
    SVM_ACTUAL = cardCnt (TableName_joinRes)
    print TMName_left, ' join ', TMName_right
    print 'SVM_ACTUAL', 'SVM_EST'
    return SVM_ACTUAL, SVM_EST

def card_est_interimIsBoth(TableName_left, TableName_mid, TableName_right, v_TM_left_upper, v_TM_left_lower, v_TM_right_upper, v_TM_right_lower):
    VTres_left_lower = v_TM_left_lower
    VTres_right_upper =  v_TM_right_upper
    SVM_LEFT_MID_RIGHT = sum(np.multiply(VTres_left_lower,VTres_right_upper))
    VTres_left_upper = v_TM_left_upper
    VTres_right_lower = v_TM_right_lower
    len_left_upper = len(VTres_left_upper)
    len_right_lower = len(VTres_right_lower)
    sum_left_upper = sum(VTres_left_upper)
    sum_right_lower = sum(VTres_right_lower)
    card_left_upper_est = []
    card_right_lower_est = []
    card_left_upper_est = np.multiply(VTres_left_upper, float(SVM_LEFT_MID_RIGHT)/sum_left_upper)
    card_right_lower_est = np.multiply(VTres_right_lower, float(SVM_LEFT_MID_RIGHT)/sum_right_lower)
    return SVM_LEFT_MID_RIGHT, card_left_upper_est.tolist(), card_right_lower_est.tolist()

def card_est_interimIsRight(TableName_left, TableName_mid, TableName_right, TMName_left, v_TM_right_upper, v_TM_right_lower):
    VTres_left_lower = createVecTup(TableName_mid, 0, TMName_left, 1)
    VTres_right_upper = v_TM_right_upper
    SVM_LEFT_MID_RIGHT = sum(np.multiply(VTres_left_lower,VTres_right_upper))   
    VTres_left_upper = createVecTup(TableName_left, 0, TMName_left, 0)
    VTres_right_lower = v_TM_right_lower    
    len_left_upper = len(VTres_left_upper)
    len_right_lower = len(VTres_right_lower)
    sum_left_upper = sum(VTres_left_upper)
    sum_right_lower = sum(VTres_right_lower)
    card_left_lower_est = []
    card_right_lower_est = []
    card_left_upper_est = np.multiply(VTres_left_upper, float(SVM_LEFT_MID_RIGHT)/sum_left_upper)
    card_right_lower_est = np.multiply(VTres_right_lower, float(SVM_LEFT_MID_RIGHT)/sum_right_lower)
    return SVM_LEFT_MID_RIGHT, card_left_upper_est.tolist(), card_right_lower_est.tolist()

#(TableName_left, TableName_mid, TableName_right, TMName_left, v_TM_right_upper, v_TM_right_lower)=('UC.csv', 'UCS.csv', 'ECS.csv', 'UCaaUCS.csv', card_upper_UCS_ECS_est, card_lower_UCS_ECS_est)
#VTres_left_lower = createVecTup(TableName_left, 0, TMName_left, 1)
#VTres_right_upper = v_TM_right_upper

def card_est_interimIsLeft(TableName_left, TableName_mid, TableName_right, v_TM_left_upper, v_TM_left_lower, TMName_right):
    VTres_left_lower = v_TM_left_lower
    VTres_right_upper =  createVecTup(TableName_mid, 0, TMName_right, 0)
    SVM_LEFT_MID_RIGHT = sum(np.multiply(VTres_left_lower,VTres_right_upper))
    VTres_left_upper = v_TM_left_upper
    VTres_right_lower = createVecTup(TableName_right, 0, TMName_right, 1)
    len_left_upper = len(VTres_left_upper)
    len_right_lower = len(VTres_right_lower)
    sum_left_upper = sum(VTres_left_upper)
    sum_right_lower = sum(VTres_right_lower)
    card_left_upper_est = []
    card_right_lower_est = []
    card_left_upper_est = np.multiply(VTres_left_upper, float(SVM_LEFT_MID_RIGHT)/sum_left_upper)
    card_right_lower_est = np.multiply(VTres_right_lower, float(SVM_LEFT_MID_RIGHT)/sum_right_lower)
    return SVM_LEFT_MID_RIGHT, card_left_upper_est.tolist(), card_right_lower_est.tolist()

## R-ECS chain
#SVM_R_SCP_ACT, card_upper_R_SCP_est, card_lower_R_SCP_est = card_est('RQ.csv', 'CP.csv', 'SCP.csv', 'RQaaCP.csv', 'CPaaSCP.csv')
SVM_CP_CC_ACT, card_upper_CP_CC_est, card_lower_CP_CC_est = card_est('CP.csv', 'SCP.csv', 'CC.csv', 'CPaaSCP.csv', 'SCPaaCC.csv')
#SVM_SCP_UCS_ACT, card_upper_SCP_UCS_est, card_lower_SCP_UCS_est = card_est('SCP.csv', 'CC.csv', 'UCS.csv', 'SCPaaCC.csv', 'CCaaUCS.csv')
#SVM_CC_EC_ACT, card_upper_CC_EC_est, card_lower_CC_EC_est = card_est('CC.csv', 'UCS.csv', 'EC.csv', 'CCaaUCS.csv', 'UCSaaEC.csv')
#SVM_UCS_ECS_ACT, card_upper_UCS_ECS_est, card_lower_UCS_ECS_est = card_est('UCS.csv', 'EC.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv')

SVM_R__CP_CC_EST, card_upper_R__CP_CC_est, card_lower_R__CP_CC_est = card_est_interimIsRight('RQ.csv', 'CP.csv', 'CC.csv', 'RQaaCP.csv', card_upper_CP_CC_est, card_lower_CP_CC_est)
SVM_R__CP_CC___UCS_EST, card_upper_R__CP_CC___UCS_est, card_lower_R__CP_CC___UCS_est = card_est_interimIsLeft('RQ.csv', 'CC.csv', 'UCS.csv', card_upper_R__CP_CC_est, card_lower_R__CP_CC_est, 'CCaaUCS.csv')
SVM_CC_EC_ACT, card_upper_CC_EC_est, card_lower_CC_EC_est = card_est('CC.csv', 'UCS.csv', 'EC.csv', 'CCaaUCS.csv', 'UCSaaEC.csv')

SVM_R__CP_CC___UCS____EC_EST, card_upper_R__CP_CC___UCS____EC_est, card_lower_R__CP_CC___UCS____EC_est = card_est_interimIsBoth('RQ.csv', 'CC.csv', 'EC.csv', card_upper_R__CP_CC_est, card_lower_R__CP_CC_est, card_upper_CC_EC_est, card_lower_CC_EC_est)
SVM_CC_EC__ECS_EST, card_upper_CC_EC__ECS_est, card_lower_CC_EC__ECS_est = card_est_interimIsLeft('CC.csv', 'EC.csv', 'ECS.csv', card_upper_CC_EC_est, card_lower_CC_EC_est, 'ECaaECS.csv')



#SVM_R__CP_CC_EST
#7672.3341360124696
#JoinRtoCC(myAW); // 7552

#SVM_R__CP_CC___UCS_EST
#123888.6020187767
#JoinRtoUCS(myAW); // 121301



#SVM_R_SCP_ACT, SVM_CP_CC_ACT, SVM_SCP_UCS_ACT, SVM_CC_EC_ACT, SVM_UCS_ECS_ACT
#(9760, 9467, 192526, 12875, 362219)
#### SVM_CP_CC_ACT cheapest join

## G-ECS chain
#SVM_EST, card_upper_est, card_lower_est = card_est(TableName_left, TableName_mid, TableName_right, TMName_left, TMName_right)
#SVM_G_UCS_ACT, card_upper_G_UCS_est, card_lower_G_UCS_est = card_est('G.csv', 'UC.csv', 'UCS.csv', 'GaaUC.csv', 'UCaaUCS.csv')
#SVM_UC_EC_ACT, card_upper_UC_EC_est, card_lower_UC_EC_est = card_est('UC.csv', 'UCS.csv', 'EC.csv', 'UCaaUCS.csv', 'UCSaaEC.csv')
#SVM_UCS_ECS_ACT, card_upper_UCS_ECS_est, card_lower_UCS_ECS_est = card_est('UCS.csv', 'EC.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv')

#>>> SVM_G_UCS_ACT
#12715
#>>> SVM_UC_EC_ACT
#12622
#>>> SVM_UCS_ECS_ACT
#362219
#witnin the 10 percent range

#SVM_G__UC_EC_EST, card_upper_G__UC_EC_est, card_lower_G__UC_EC_est = card_est_interimIsRight('G.csv', 'UC.csv', 'EC.csv', 'GaaUC.csv', card_upper_UC_EC_est, card_lower_UC_EC_est)
#SVM_G_EC__ECS_EST, card_upper_G_EC__ECS_est, card_lower_G_EC__ECS_est = card_est_interimIsLeft('G.csv', 'EC.csv', 'ECS.csv', card_upper_G__UC_EC_est, card_lower_G__UC_EC_est, 'ECaaECS.csv')

#SVM_UC_EC__ECS_EST, card_upper_UC_EC__ECS_est, card_lower_UC_EC__ECS_est = card_est_interimIsLeft('UC.csv', 'EC.csv', 'ECS.csv', card_upper_UC_EC_est, card_lower_UC_EC_est, 'ECaaECS.csv')

#SVM_UCS_ECS_ACT, card_upper_UCS_ECS_est, card_lower_UCS_ECS_est = card_est('UCS.csv', 'EC.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv')
# estimate UC_ECS
#SVM_UC_ECS_EST, card_upper_UC_ECS_est, card_lower_UC_ECS_est = card_est_interimIsRight('UC.csv', 'UCS.csv', 'ECS.csv', 'UCaaUCS.csv', card_upper_UCS_ECS_est, card_lower_UCS_ECS_est)
# actual UC_ECS
#SVM_UC_ECS_ACT, card_UC_ECS_upper_ACT, card_UC_ECS_lower_ACT = card_est('UC.csv', 'UCS.csv', 'ECS.csv', 'UCaaUCS.csv','UCSaaECS.csv')

#print 'SVM_UC_ECS_ACT, SVM_UC_ECS_EST'
#print SVM_UC_ECS_ACT, ', ', SVM_UC_ECS_EST





    
# cardinality exactly identified
#print cardComp('UCS.csv', 'EC.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv', 'UCSaaECS.csv')
#print cardComp('UC.csv', 'UCS.csv', 'ECS.csv', 'UCaaUCS.csv', 'UCSaaECS.csv', 'UCaaECS.csv')



# print comparePerf_std('UCS.csv', 'EC.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv', 'UCSaaECS.csv')

#card_upper_act = createVecTup('UCS.csv', 0,  'UCSaaECS.csv', 0)
#card_lower_act = createVecTup('ECS.csv', 0,  'UCSaaECS.csv', 1)

#print comparePerf_std('UCS.csv', 'UC.csv', 'ECS.csv', 'UCaaUCS.csv', 'UCSaaECS.csv', 'UCaaECS.csv')



       # 'EC.csv', 'UCS.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv'
#print (TableName_mid, TableName_left, TableName_right, TMName_left, TMName_right)

    
#VM_UCS_EC_ECS, card_left_upper_est, card_right_under_est = card_est('EC.csv', 'UCS.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv')

#res_UCS_EC_ECS = card_est('EC.csv', 'UCS.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv')
#card_upper = createVecTup('UCS.csv', 0, 'UCSaaECS.csv', 0)
#card_under = createVecTup('ECS.csv', 0, 'UCSaaECS.csv', 1)

#print len(card_upper) == len(res_UCS_EC_ECS[1])
#print len(card_under) == len(res_UCS_EC_ECS[2])

#VTres_EC_UCS_EC = createVecTup('EC.csv', 0, 'UCSaaEC.csv', 1)
#VTres_EC_EC_ECS = createVecTup('EC.csv', 0, 'ECaaECS.csv', 1)

#col_val_ECT = csvRNS('EC.csv', 0)
#col_val_UCSaaECTM = csvRNS('UCSaaEC.csv',1)



#col_val_GT = csvRNS('G.csv', 0)
#col_val_GTM = csvRNS('GaaUC.csv',0)
#NDV_tup_cnt = vectorTup(col_val_GT, col_val_GTM)


#for row in col_val:
    #temp = col_val.count(x)
#print col_names

def comparePerf_std(TableName_left, TableName_mid, TableName_right,
                 TMName_left, TMName_right, TableName_joinRes):
    SVM_LEFT_MID_RIGHT, card_upper_est, card_lower_est = card_est(TableName_left, TableName_mid, TableName_right, TMName_left, TMName_right)
    card_upper_act = createVecTup(TableName_left, 0, TableName_joinRes, 0)
    card_lower_act = createVecTup(TableName_right, 0, TableName_joinRes, 1)
    
    print 'max(card_upper_act)',max(card_upper_act)
    print 'min(card_upper_act)', min(card_upper_act)
    print 'max(card_upper_est)',max(card_upper_est)
    print 'min(card_upper_est)', min(card_upper_est)

    print 'max(card_lower_act)',max(card_lower_act)
    print 'min(card_lower_act)', min(card_lower_act)
    print 'max(card_lower_est)',max(card_lower_est)
    print 'min(card_lower_est)', min(card_lower_est)

    mean_upper_act = float(sum(card_upper_act))/(max(len(card_upper_act),1))
    mean_upper_est = float(sum(card_upper_est))/(max(len(card_upper_est),1))
    mean_upper = 0
    std_upper_act = 0
    std_upper_est = 0
    std_upper = 0
    
    #temp = np.array(card_upper_act,float) - np.array(card_upper_est)
    std_upper_act = float(sum(np.subtract(card_upper_act, mean_upper_act)**2))
    std_upper_act = (std_upper_act/(max(len(card_upper_act),1)))**0.5
    std_upper_est = float(sum(np.subtract(card_upper_est, mean_upper_est)**2))
    std_upper_est = (std_upper_est/(max(len(card_upper_est),1)))**0.5
    
           
    mean_lower_act = float(sum(card_lower_act))/(max(len(card_lower_act),1))
    mean_lower_est = float(sum(card_lower_est))/(max(len(card_lower_est),1))
    mean_lower = 0
    std_lower_act = 0
    std_lower_est = 0
    std_lower = 0
    std_lower_act = float(sum(np.subtract(card_lower_act, mean_lower_act)**2))
    std_lower_act = (std_lower_act/(max(len(card_lower_act),1)))**0.5
    std_lower_est = float(sum(np.subtract(card_lower_est, mean_lower_est)**2))
    std_lower_est = (std_lower_est/(max(len(card_lower_est),1)))**0.5

    print '(std_upper_act, std_lower_act), (std_upper_est, std_lower_est)'
    print (std_upper_act, std_lower_act), (std_upper_est, std_lower_est)

    print '(std_upper_act/mean_upper_act, std_lower_act/mean_lower_act), (std_upper_est/mean_upper_est, std_lower_est/mean_lower_est)'
    return (std_upper_act/mean_upper_act, std_lower_act/mean_lower_act), (std_upper_est/mean_upper_est, std_lower_est/mean_lower_est)




