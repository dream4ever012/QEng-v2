import csv
import numpy

def csvRNS(csvName, col_num):
    import csv
    file = open(csvName)
    csv = csv.reader(file)

    col_val =[]
    i = True
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
    SVM_UCS_EC_ECS = SumOfVecMulp(TableName_mid, TMName_left, TMName_right)
    VTres_left_upper = createVecTup(TableName_left, 0, TMName_left, 0)
    VTres_right_under = createVecTup(TableName_right, 0, TMName_right, 1)
    len_left_upper = len(VTres_left_upper)
    len_right_under = len(VTres_right_under)
    sum_left_upper = sum(VTres_left_upper)
    sum_right_under = sum(VTres_right_under)
    card_left_upper_est = []
    card_right_under_est = []
    for i in range(0,len_left_upper):
        card_left_upper_est.append(SVM_UCS_EC_ECS*float(VTres_left_upper[i])/sum_left_upper)
    for i in range(0,len_right_under):
        card_right_under_est.append(SVM_UCS_EC_ECS*float(VTres_right_under[i])/sum_right_under)
    return SVM_UCS_EC_ECS, card_left_upper_est, card_right_under_est

def comparePerf_std (TableName_mid, TableName_left, TableName_right,
                 TMName_left, TMName_right, TableName_joinRes):
    SVM_UCS_EC_ECS, card_upper_est, card_under_est = card_est(TableName_mid, TableName_left, TableName_right, TMName_left, TMName_right)
    card_upper_act = createVecTup(TableName_left, 0, TableName_joinRes, 0)
    card_under_act = createVecTup(TableName_right, 0, TableName_joinRes, 1)
    upper = len(card_upper_act)
    under = len(card_under_act)

    print 'max(card_upper_act)',max(card_upper_act)
    print 'min(card_upper_act)', min(card_upper_act)
    print 'max(card_upper_est)',max(card_upper_est)
    print 'min(card_upper_est)', min(card_upper_est)

    print 'max(card_under_act)',max(card_under_act)
    print 'min(card_under_act)', min(card_under_act)
    print 'max(card_under_est)',max(card_under_est)
    print 'min(card_under_est)', min(card_under_est)

    temp = 0
    err_mean_upper = 0
    err_std_upper = 0
    for i in range(0,upper):
        temp = card_upper_act[i] - card_upper_est[i]
        err_mean_upper = err_mean_upper + (temp)
        err_std_upper = err_std_upper + (temp)**2
    err_std_upper = (float(err_std_upper)/(max(len(card_upper_act),1)))**0.5
    err_mean_upper = (float(err_mean_upper)/(max(len(card_upper_act),1)))

    err_mean_under = 0
    err_std_under = 0
    for i in range(0,under):
        temp = card_under_act[i] - card_under_est[i]
        err_mean_under = err_mean_under + (temp)**2
        err_std_under = err_std_under + temp        
    err_std_under = (float(err_std_under)/(max(len(card_under_act),1)))**0.5
    err_mean_under = (float(err_mean_under)/max(len(card_under_act),1))

    print '(err_std_upper/err_mean_upper, err_std_under/err_mean_under)'
    return err_std_upper/err_mean_upper, err_std_under/err_mean_under

def comparePerf_diff (TableName_mid, TableName_left, TableName_right,
                 TMName_left, TMName_right, TableName_joinRes):
    SVM_UCS_EC_ECS, card_upper_est, card_under_est = card_est(TableName_mid, TableName_left, TableName_right, TMName_left, TMName_right)
    card_upper_act = createVecTup(TableName_left, 0, TableName_joinRes, 0)
    card_under_act = createVecTup(TableName_right, 0, TableName_joinRes, 1)
    upper = len(card_upper_act)
    under = len(card_under_act)

    print 'max(card_upper_act)',max(card_upper_act)
    print 'min(card_upper_act)', min(card_upper_act)
    print 'max(card_upper_est)',max(card_upper_est)
    print 'min(card_upper_est)', min(card_upper_est)

    print 'max(card_under_act)',max(card_under_act)
    print 'min(card_under_act)', min(card_under_act)
    print 'max(card_under_est)',max(card_under_est)
    print 'min(card_under_est)', min(card_under_est)

    err_sum_upper = 0
    for i in range(0,upper):
        #err_sum_upper = err_sum_upper + abs(card_upper_act[i] - card_upper_est[i])
        err_sum_upper = err_sum_upper + (card_upper_act[i] - card_upper_est[i])
    err_std_upper = float(err_sum_upper)/(max(len(card_upper_act),1))
    
    err_sum_under = 0
    for i in range(0,under):
        #err_sum_under = err_sum_under + abs(card_under_act[i] - card_under_est[i])
        err_sum_under = err_sum_under + (card_under_act[i] - card_under_est[i])
    err_std_under = float(err_sum_under)/(max(len(card_under_act),1))

    #print '(avg_abs_diff_upper, avg_abs_diff_under)'
    print '(avg_diff_upper, avg_diff_under)'
    return err_std_upper, err_std_under
#    avg_card_upper_est = float(sum(res_left_mid_right[1])) / max(len(res_left_mid_right[1]), 1)
#    avg_card_under_est = float(sum(res_left_mid_right[2])) / max(len(res_left_mid_right[2]), 1)
#    avg_card_upper_act = float(sum(card_upper)) / max(len(card_upper), 1)
#    avg_card_under_act = float(sum(card_under)) / max(len(card_under), 1)


#print comparePerf_std('EC.csv', 'UCS.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv', 'UCSaaECS.csv')
#print comparePerf_diff('EC.csv', 'UCS.csv', 'ECS.csv', 'UCSaaEC.csv', 'ECaaECS.csv', 'UCSaaECS.csv')

print comparePerf_std('UCS.csv', 'UC.csv', 'ECS.csv', 'UCaaUCS.csv', 'UCSaaECS.csv', 'UCaaECS.csv')
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






