import csv
import numpy

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
    length = len(VTres_left_under)
    sum_total = 0
    #temp = 0
    ans = numpy.multiply(VTres_left_under,VTres_right_upper)
    return sum(ans)

#result = createVecTup('UC.csv', 0, 'GaaUC.csv',1)

#print SumOfVecMulp('UC.csv', 'GaaUC.csv', 'UCaaUCS.csv')
#print SumOfVecMulp('UCS.csv', 'UCaaUCS.csv', 'UCSaaEC.csv')
#print SumOfVecMulp('EC.csv', 'UCSaaEC.csv', 'ECaaECS.csv')
#

def card_est(TableName_mid, TableName_left, TableName_right, TMName_left, TMName_right):
    SVM_LEFT_MID_RIGHT = SumOfVecMulp(TableName_mid, TMName_left, TMName_right)
    VTres_left_upper = createVecTup(TableName_left, 0, TMName_left, 0)
    VTres_right_under = createVecTup(TableName_right, 0, TMName_right, 1)
    len_left_upper = len(VTres_left_upper)
    len_right_under = len(VTres_right_under)
    sum_left_upper = sum(VTres_left_upper)
    sum_right_under = sum(VTres_right_under)
    card_left_upper_est = []
    card_right_under_est = []
    for i in range(0,len_left_upper):
        card_left_upper_est.append(SVM_LEFT_MID_RIGHT*float(VTres_left_upper[i])/sum_left_upper)
    for i in range(0,len_right_under):
        card_right_under_est.append(SVM_LEFT_MID_RIGHT*float(VTres_right_under[i])/sum_right_under)
    return SVM_LEFT_MID_RIGHT, card_left_upper_est, card_right_under_est



def comparePerf_std (TableName_mid, TableName_left, TableName_right,
                 TMName_left, TMName_right, TableName_joinRes):
    SVM_LEFT_MID_RIGHT, card_upper_est, card_lower_est = card_est(TableName_mid, TableName_left, TableName_right, TMName_left, TMName_right)
    card_upper_act = createVecTup(TableName_left, 0, TableName_joinRes, 0)
    card_lower_act = createVecTup(TableName_right, 0, TableName_joinRes, 1)
    upper = len(card_upper_act)
    lower = len(card_lower_act)
    
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
    for i in range(0,upper):
        temp = card_upper_act[i] - card_upper_est[i]
        std_upper = std_upper + (temp)**2
        std_upper_act += (card_upper_act[i]-mean_upper_act)**2
        std_upper_est += (card_upper_est[i]-mean_upper_est)**2
    std_upper_act = (float(std_upper_act)/(max(len(card_upper_act),1)))**0.5
    std_upper_est = (float(std_upper_est)/(max(len(card_upper_act),1)))**0.5

    mean_lower_act = float(sum(card_lower_act))/(max(len(card_lower_act),1))
    mean_lower_est = float(sum(card_lower_est))/(max(len(card_lower_est),1))
    mean_lower = 0
    std_lower_act = 0
    std_lower_est = 0
    std_lower = 0
    for i in range(0,lower):
        temp = card_lower_act[i] - card_lower_est[i]
        std_lower = std_lower + (temp)**2
        std_lower_act += (card_lower_act[i]-mean_lower_act)**2
        std_lower_est += (card_lower_est[i]-mean_lower_est)**2    
    std_lower_act = (float(std_lower_act)/(max(len(card_lower_act),1)))**0.5
    std_lower_est = (float(std_lower_est)/(max(len(card_lower_act),1)))**0.5

    print TableName_left, TableName_mid, TableName_right
    print '(std_upper_act, std_lower_act), (std_upper_est, std_lower_est)'
    print (std_upper_act, std_lower_act), (std_upper_est, std_lower_est)

    print '(std_upper_act/mean_upper_act, std_lower_act/mean_lower_act), (std_upper_est/mean_upper_est, std_lower_est/mean_lower_est)'
    return (std_upper_act/mean_upper_act, std_lower_act/mean_lower_act), (std_upper_est/mean_upper_est, std_lower_est/mean_lower_est)



print comparePerf_std('EC.csv', 'UCS.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv', 'UCSaaECS.csv')
#print comparePerf_diff('EC.csv', 'UCS.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv', 'UCSaaECS.csv')

#print comparePerf_std('UCS.csv', 'UC.csv', 'ECS.csv', 'UCaaUCS.csv', 'UCSaaECS.csv', 'UCaaECS.csv')
#print comparePerf_diff('UCS.csv', 'UC.csv', 'ECS.csv', 'UCaaUCS.csv', 'UCSaaECS.csv', 'UCaaECS.csv')



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






