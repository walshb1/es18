import os
import csv
import pandas as pd
import numpy as np


# Code for MI-08 (BW & SH)

# Load the file
dir = '/Users/brian/Desktop/analytics_info/vf/'
if not os.path.exists(dir):
    dir = '' # Sam point to your directory with the files here 
f1 = dir+'usc08.lst'
f2 = dir+'usc_AllHis.LST'

name_f, name_l, name_m, name_s = [],[],[],[]
year_birth, year_age, date_reg = [],[],[]



with open(f1) as f:
    reader = csv.reader(f)
    
    for row in reader:
        _str = str(row[0])
        #
        name_l.append(_str[ 0:34].replace(' ',''))# alpha, hyphens allowed
        name_f.append(_str[35:54].replace(' ',''))# alpha only (no spaces)
        name_m.append(_str[55:74].replace(' ',''))# alpha only (no spaces)
        name_s.append(_str[75:77].replace(' ',''))# JR, SR, or I-V
        #
        year_birth.append(int(_str[78:82]))# YYYY
        year_age.append(2018-year_birth[-1])# age on election date

print(year_age[0:20])

# Code developed for use in CO-7th district (BW)
assert(False)
myCols = ['VOTER_ID','COUNTY','REGISTRATION_DATE','EFFECTIVE_DATE','LAST_UPDATED_DATE','RESIDENTIAL_ZIP_CODE','RESIDENTIAL_CITY','VOTER_STATUS','PARTY','GENDER','BIRTH_YEAR','State Senate','State House','Congressional','MAILING_ADDRESS_1']

mydtype = {'BIRTH_YEAR':np.int32,'Congressional':np.int32}

dfa1 = pd.read_table('./adams/Voters_Voting_History/Voters_Voting_History_For_Last_5_Elections_of_Every_Type_Part1_05_19_2017_14_28_38.txt',sep=',',usecols=myCols,index_col=['VOTER_ID'])
dfa2 = pd.read_table('./adams/Voters_Voting_History/Voters_Voting_History_For_Last_5_Elections_of_Every_Type_Part2_05_19_2017_14_28_38.txt',sep=',',usecols=myCols,index_col=['VOTER_ID'])
dfa3 = pd.read_table('./adams/Voters_Voting_History/Voters_Voting_History_For_Last_5_Elections_of_Every_Type_Part3_05_19_2017_14_28_38.txt',sep=',',usecols=myCols,index_col=['VOTER_ID'])
#dfj  = pd.read_table('./jeffco/Voter_Details_5_31_2017.txt',sep=',',usecols=myCols,index_col='VOTER_ID')
dfj  = pd.read_table('./jeffco/Voter_Details_6_30_2017.txt',sep=',',usecols=myCols,index_col='VOTER_ID')

# Universe of all voters
uni = pd.concat([dfa1,dfa2,dfa3,dfj],join='outer').dropna(how='all').drop('VOTER_ID',axis=0)
uni[['State House','State Senate','Congressional','BIRTH_YEAR']] = uni[['State House','State Senate','Congressional','BIRTH_YEAR']].apply(pd.to_numeric,errors='ignore').fillna(value=-1)
uni['BIRTH_YEAR'] = uni['BIRTH_YEAR'].astype('int')

# CD7 voters
cd7 = uni.loc[uni.Congressional == 7]
#
n_t = cd7.shape[0]
n_a = cd7.loc[(cd7.VOTER_STATUS == 'Active')].shape[0]
n_i = cd7.loc[(cd7.VOTER_STATUS != 'Active')].shape[0]

# Active voters in CD7
cd7_av = cd7.loc[(cd7.VOTER_STATUS == 'Active')].copy()

print('n(Active Voters) = ', n_a)
print('n(Inactive Voters) = ', n_i)
assert(n_t == (n_a+n_i))

cd7_av.to_csv('~/Desktop/CO_7th/myvoters.csv')
# Active primary voters in CD7
cd7_pv = cd7_av.loc[(cd7_av.PARTY == 'DEM') | (cd7_av.PARTY == 'UAF')].copy()
n_p = cd7_pv.shape[0]
print('n(Primary voters) = ',n_p)
#
n_p_m = cd7_pv.loc[(cd7_pv.GENDER == 'Male')].shape[0]
n_p_f = cd7_pv.loc[(cd7_pv.GENDER == 'Female')].shape[0]
n_p_o = cd7_pv.loc[(cd7_pv.GENDER != 'Male') & (cd7_pv.GENDER != 'Female')].shape[0]

#
print('\nAmong primary voters: \n')
print(n_p_m,' male')
print(n_p_f,' female')
print(n_p_o,' other/unknown')
assert(n_p == (n_p_m+n_p_f+n_p_o))
print('Avg. age of DEMS:',round(2017.-np.mean(cd7_pv.loc[cd7_pv.PARTY == 'DEM','BIRTH_YEAR']),1))
print('Avg. age of DEMS-M:',round(2017.-np.mean(cd7_pv.loc[(cd7_pv.PARTY == 'DEM') & (cd7_pv.GENDER == 'Male'),'BIRTH_YEAR']),1))
print('Avg. age of DEMS-F:',round(2017.-np.mean(cd7_pv.loc[(cd7_pv.PARTY == 'DEM') & (cd7_pv.GENDER == 'Female'),'BIRTH_YEAR']),1))

print('Avg. age of INDS:',round(2017.-np.mean(cd7_pv.loc[cd7_pv.PARTY == 'UAF','BIRTH_YEAR']),1))
print('Avg. age of INDS-M:',round(2017.-np.mean(cd7_pv.loc[(cd7_pv.PARTY == 'UAF') & (cd7_pv.GENDER == 'Male'),'BIRTH_YEAR']),1))
print('Avg. age of INDS-F:',round(2017.-np.mean(cd7_pv.loc[(cd7_pv.PARTY == 'UAF') & (cd7_pv.GENDER == 'Female'),'BIRTH_YEAR']),1))

print('Avg. age of REPS:',round(2017.-np.mean(cd7_av.loc[cd7_av.PARTY == 'REP','BIRTH_YEAR']),1))
print('Avg. age of REPS-M:',round(2017.-np.mean(cd7_av.loc[(cd7_av.PARTY == 'REP') & (cd7_av.GENDER == 'Male'),'BIRTH_YEAR']),1))
print('Avg. age of REPS-F:',round(2017.-np.mean(cd7_av.loc[(cd7_av.PARTY == 'REP') & (cd7_av.GENDER == 'Female'),'BIRTH_YEAR']),1))
#
# ALL ACTIVE VOTERS (not just primary voters)
print('\n')
n_a_20s = cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1987) & (cd7_av.BIRTH_YEAR < 1999)].shape[0]
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1987) & (cd7_av.PARTY == 'DEM')].shape[0]/n_a_20s*100.,2))+'% of av in 20s are DEM')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1987) & (cd7_av.PARTY == 'UAF')].shape[0]/n_a_20s*100.,2))+'% of av in 20s are UAF')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1987) & (cd7_av.PARTY == 'REP')].shape[0]/n_a_20s*100.,2))+'% of av in 20s are REP')
print('+'+str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1987) & (cd7_av.PARTY != 'REP')&(cd7_av.PARTY!='DEM')&(cd7_av.PARTY!='UAF')].shape[0]/n_a_20s*100.,2))+'% other')
print('\n')
n_a_30s = cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1977) & (cd7_av.BIRTH_YEAR < 1987)].shape[0]
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1977)&(cd7_av.BIRTH_YEAR < 1987)&(cd7_av.PARTY == 'DEM')].shape[0]/n_a_30s*100.,2))+'% of av in 30s are DEM')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1977)&(cd7_av.BIRTH_YEAR < 1987)&(cd7_av.PARTY == 'UAF')].shape[0]/n_a_30s*100.,2))+'% of av in 30s are UAF')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1977)&(cd7_av.BIRTH_YEAR < 1987)&(cd7_av.PARTY == 'REP')].shape[0]/n_a_30s*100.,2))+'% of av in 30s are REP')
print('+'+str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1977)&(cd7_av.BIRTH_YEAR < 1987)&(cd7_av.PARTY != 'REP')&(cd7_av.PARTY!='DEM')&(cd7_av.PARTY!='UAF')].shape[0]/n_a_30s*100.,2))+'% other')
print('\n')
n_a_40s = cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1967) & (cd7_av.BIRTH_YEAR < 1977)].shape[0]
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1967)&(cd7_av.BIRTH_YEAR < 1977)&(cd7_av.PARTY == 'DEM')].shape[0]/n_a_40s*100.,2))+'% of av in 40s are DEM')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1967)&(cd7_av.BIRTH_YEAR < 1977)&(cd7_av.PARTY == 'UAF')].shape[0]/n_a_40s*100.,2))+'% of av in 40s are UAF')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1967)&(cd7_av.BIRTH_YEAR < 1977)&(cd7_av.PARTY == 'REP')].shape[0]/n_a_40s*100.,2))+'% of av in 40s are REP')
print('+'+str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1967)&(cd7_av.BIRTH_YEAR < 1977)&(cd7_av.PARTY != 'REP')&(cd7_av.PARTY!='DEM')&(cd7_av.PARTY!='UAF')].shape[0]/n_a_40s*100.,2))+'% other')
print('\n')
n_a_50s = cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1957) & (cd7_av.BIRTH_YEAR < 1967)].shape[0]
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1957)&(cd7_av.BIRTH_YEAR < 1967)&(cd7_av.PARTY == 'DEM')].shape[0]/n_a_50s*100.,2))+'% of av in 50s are DEM')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1957)&(cd7_av.BIRTH_YEAR < 1967)&(cd7_av.PARTY == 'UAF')].shape[0]/n_a_50s*100.,2))+'% of av in 50s are UAF')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1957)&(cd7_av.BIRTH_YEAR < 1967)&(cd7_av.PARTY == 'REP')].shape[0]/n_a_50s*100.,2))+'% of av in 50s are REP')
print('+'+str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1957)&(cd7_av.BIRTH_YEAR < 1967)&(cd7_av.PARTY != 'REP')&(cd7_av.PARTY!='DEM')&(cd7_av.PARTY!='UAF')].shape[0]/n_a_50s*100.,2))+'% other')
print('\n')
n_a_60s = cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1947) & (cd7_av.BIRTH_YEAR < 1957)].shape[0]
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1947)&(cd7_av.BIRTH_YEAR < 1957)&(cd7_av.PARTY == 'DEM')].shape[0]/n_a_60s*100.,2))+'% of av in 60s are DEM')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1947)&(cd7_av.BIRTH_YEAR < 1957)&(cd7_av.PARTY == 'UAF')].shape[0]/n_a_60s*100.,2))+'% of av in 60s are UAF')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1947)&(cd7_av.BIRTH_YEAR < 1957)&(cd7_av.PARTY == 'REP')].shape[0]/n_a_60s*100.,2))+'% of av in 60s are REP')
print('+'+str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR >= 1947)&(cd7_av.BIRTH_YEAR < 1957)&(cd7_av.PARTY != 'REP')&(cd7_av.PARTY!='DEM')&(cd7_av.PARTY!='UAF')].shape[0]/n_a_60s*100.,2))+'% other')
print('\n')
n_a_70s = cd7_av.loc[(cd7_av.BIRTH_YEAR < 1947)].shape[0]
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR < 1947)&(cd7_av.PARTY == 'DEM')].shape[0]/n_a_70s*100.,2))+'% of av age 70+ are DEM')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR < 1947)&(cd7_av.PARTY == 'UAF')].shape[0]/n_a_70s*100.,2))+'% of av age 70+ are UAF')
print(str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR < 1947)&(cd7_av.PARTY == 'REP')].shape[0]/n_a_70s*100.,2))+'% of av age 70+ are REP')
print('+'+str(round(cd7_av.loc[(cd7_av.BIRTH_YEAR < 1947)&(cd7_av.PARTY != 'REP')&(cd7_av.PARTY!='DEM')&(cd7_av.PARTY!='UAF')].shape[0]/n_a_70s*100.,2))+'% other')
#
print('\n')
n_p_l18 = cd7_pv.loc[(cd7_pv.BIRTH_YEAR >= 1999)].shape[0]
n_p_20s = cd7_pv.loc[(cd7_pv.BIRTH_YEAR >= 1987) & (cd7_pv.BIRTH_YEAR < 1999)].shape[0]
n_p_30s = cd7_pv.loc[(cd7_pv.BIRTH_YEAR >= 1977) & (cd7_pv.BIRTH_YEAR < 1987)].shape[0]
n_p_40s = cd7_pv.loc[(cd7_pv.BIRTH_YEAR >= 1967) & (cd7_pv.BIRTH_YEAR < 1977)].shape[0]
n_p_50s = cd7_pv.loc[(cd7_pv.BIRTH_YEAR >= 1957) & (cd7_pv.BIRTH_YEAR < 1967)].shape[0]
n_p_60s = cd7_pv.loc[(cd7_pv.BIRTH_YEAR >= 1947) & (cd7_pv.BIRTH_YEAR < 1957)].shape[0]
n_p_70p = cd7_pv.loc[(cd7_pv.BIRTH_YEAR < 1947)].shape[0]
assert(n_p==(n_p_l18+n_p_20s+n_p_30s+n_p_40s+n_p_50s+n_p_60s+n_p_70p))
#
n_p_m_l18 = cd7_pv.loc[(cd7_pv.GENDER == 'Male') & (cd7_pv.BIRTH_YEAR >= 1999)].shape[0]
n_p_m_20s = cd7_pv.loc[(cd7_pv.GENDER == 'Male') & (cd7_pv.BIRTH_YEAR >= 1987) & (cd7_pv.BIRTH_YEAR < 1999)].shape[0]
n_p_m_30s = cd7_pv.loc[(cd7_pv.GENDER == 'Male') & (cd7_pv.BIRTH_YEAR >= 1977) & (cd7_pv.BIRTH_YEAR < 1987)].shape[0]
n_p_m_40s = cd7_pv.loc[(cd7_pv.GENDER == 'Male') & (cd7_pv.BIRTH_YEAR >= 1967) & (cd7_pv.BIRTH_YEAR < 1977)].shape[0]
n_p_m_50s = cd7_pv.loc[(cd7_pv.GENDER == 'Male') & (cd7_pv.BIRTH_YEAR >= 1957) & (cd7_pv.BIRTH_YEAR < 1967)].shape[0]
n_p_m_60s = cd7_pv.loc[(cd7_pv.GENDER == 'Male') & (cd7_pv.BIRTH_YEAR >= 1947) & (cd7_pv.BIRTH_YEAR < 1957)].shape[0]
n_p_m_70p = cd7_pv.loc[(cd7_pv.GENDER == 'Male') & (cd7_pv.BIRTH_YEAR < 1947)].shape[0]
assert(n_p_m==(n_p_m_l18+n_p_m_20s+n_p_m_30s+n_p_m_40s+n_p_m_50s+n_p_m_60s+n_p_m_70p))
#
n_p_f_l18 = cd7_pv.loc[(cd7_pv.GENDER == 'Female') & (cd7_pv.BIRTH_YEAR >= 1999)].shape[0]
n_p_f_20s = cd7_pv.loc[(cd7_pv.GENDER == 'Female') & (cd7_pv.BIRTH_YEAR >= 1987) & (cd7_pv.BIRTH_YEAR < 1999)].shape[0]
n_p_f_30s = cd7_pv.loc[(cd7_pv.GENDER == 'Female') & (cd7_pv.BIRTH_YEAR >= 1977) & (cd7_pv.BIRTH_YEAR < 1987)].shape[0]
n_p_f_40s = cd7_pv.loc[(cd7_pv.GENDER == 'Female') & (cd7_pv.BIRTH_YEAR >= 1967) & (cd7_pv.BIRTH_YEAR < 1977)].shape[0]
n_p_f_50s = cd7_pv.loc[(cd7_pv.GENDER == 'Female') & (cd7_pv.BIRTH_YEAR >= 1957) & (cd7_pv.BIRTH_YEAR < 1967)].shape[0]
n_p_f_60s = cd7_pv.loc[(cd7_pv.GENDER == 'Female') & (cd7_pv.BIRTH_YEAR >= 1947) & (cd7_pv.BIRTH_YEAR < 1957)].shape[0]
n_p_f_70p = cd7_pv.loc[(cd7_pv.GENDER == 'Female') & (cd7_pv.BIRTH_YEAR < 1947)].shape[0]
assert(n_p_f==(n_p_f_l18+n_p_f_20s+n_p_f_30s+n_p_f_40s+n_p_f_50s+n_p_f_60s+n_p_f_70p))
#
n_p_o_l18 = cd7_pv.loc[(cd7_pv.GENDER != 'Male') & (cd7_pv.GENDER != 'Female') & (cd7_pv.BIRTH_YEAR >= 1999)].shape[0]
n_p_o_20s = cd7_pv.loc[(cd7_pv.GENDER != 'Male') & (cd7_pv.GENDER != 'Female') & (cd7_pv.BIRTH_YEAR >= 1987) & (cd7_pv.BIRTH_YEAR < 1999)].shape[0]
n_p_o_30s = cd7_pv.loc[(cd7_pv.GENDER != 'Male') & (cd7_pv.GENDER != 'Female') & (cd7_pv.BIRTH_YEAR >= 1977) & (cd7_pv.BIRTH_YEAR < 1987)].shape[0]
n_p_o_40s = cd7_pv.loc[(cd7_pv.GENDER != 'Male') & (cd7_pv.GENDER != 'Female') & (cd7_pv.BIRTH_YEAR >= 1967) & (cd7_pv.BIRTH_YEAR < 1977)].shape[0]
n_p_o_50s = cd7_pv.loc[(cd7_pv.GENDER != 'Male') & (cd7_pv.GENDER != 'Female') & (cd7_pv.BIRTH_YEAR >= 1957) & (cd7_pv.BIRTH_YEAR < 1967)].shape[0]
n_p_o_60s = cd7_pv.loc[(cd7_pv.GENDER != 'Male') & (cd7_pv.GENDER != 'Female') & (cd7_pv.BIRTH_YEAR >= 1947) & (cd7_pv.BIRTH_YEAR < 1957)].shape[0]
n_p_o_70p = cd7_pv.loc[(cd7_pv.GENDER != 'Male') & (cd7_pv.GENDER != 'Female') & (cd7_pv.BIRTH_YEAR < 1947)].shape[0]
assert(n_p_o==(n_p_o_l18+n_p_o_20s+n_p_o_30s+n_p_o_40s+n_p_o_50s+n_p_o_60s+n_p_o_70p))
#
print(n_p_l18,' <= 18 yrs (',n_p_m_l18,' M, ',n_p_f_l18,' F, ',n_p_o_l18,' uk)')
print(n_p_20s,' 18-30 yrs (',n_p_m_20s,' M, ',n_p_f_20s,' F, ',n_p_o_20s,' uk)')
print(n_p_30s,' 30-40 yrs (',n_p_m_30s,' M, ',n_p_f_30s,' F, ',n_p_o_30s,' uk)')
print(n_p_40s,' 40-50 yrs (',n_p_m_40s,' M, ',n_p_f_40s,' F, ',n_p_o_40s,' uk)')
print(n_p_50s,' 50-60 yrs (',n_p_m_50s,' M, ',n_p_f_50s,' F, ',n_p_o_50s,' uk)')
print(n_p_60s,' 60-70 yrs (',n_p_m_60s,' M, ',n_p_f_60s,' F, ',n_p_o_60s,' uk)')
print(n_p_70p,  ' 70+ yrs (',n_p_m_70p,' M, ',n_p_f_70p,' F, ',n_p_o_70p,' uk)')

#
print('\n')
print(cd7_pv.loc[(cd7_pv.PARTY == 'DEM')].shape[0],' Democrats')
print('-->',cd7_pv.loc[(cd7_pv.PARTY == 'DEM') & (cd7_pv.GENDER == 'Male')].shape[0],' Male Dems')
print('-->',cd7_pv.loc[(cd7_pv.PARTY == 'DEM') & (cd7_pv.GENDER == 'Female')].shape[0],' Female Dems')
print('\n')
print(cd7_pv.loc[(cd7_pv.PARTY == 'UAF')].shape[0],' Unaffiliated')
print('-->',cd7_pv.loc[(cd7_pv.PARTY == 'UAF') & (cd7_pv.GENDER == 'Male')].shape[0],' Male Inds')
print('-->',cd7_pv.loc[(cd7_pv.PARTY == 'UAF') & (cd7_pv.GENDER == 'Female')].shape[0],' Female Inds')
print('\n')
#

print('\n')
print('Breakdown of HD28 (BP\'s seat)')
cd7_pv_28 = cd7_pv.loc[cd7_pv['State House'] == 28]
print(cd7_pv_28.shape[0],' primary voters')

print(cd7_pv_28.loc[(cd7_pv_28.PARTY == 'DEM')].shape[0],' Democrats')
print('-->',cd7_pv_28.loc[(cd7_pv_28.PARTY == 'DEM') & (cd7_pv_28.GENDER == 'Male')].shape[0],' Male Dems')
print('-->',cd7_pv_28.loc[(cd7_pv_28.PARTY == 'DEM') & (cd7_pv_28.GENDER == 'Female')].shape[0],' Female Dems')
print('\n')
print(cd7_pv_28.loc[(cd7_pv_28.PARTY == 'UAF')].shape[0],' Independents')
print('-->',cd7_pv_28.loc[(cd7_pv_28.PARTY == 'UAF') & (cd7_pv_28.GENDER == 'Male')].shape[0],' Male Inds')
print('-->',cd7_pv_28.loc[(cd7_pv_28.PARTY == 'UAF') & (cd7_pv_28.GENDER == 'Female')].shape[0],' Female Inds')
print('\n')

print('\n')
print('Breakdown of SD22 (AK\'s seat)')
cd7_pv_22 = cd7_pv.loc[(cd7_pv['State Senate'] == 22)]
print(cd7_pv_22.shape[0],' primary voters')

print(cd7_pv_22.loc[(cd7_pv_22.PARTY == 'DEM')].shape[0],' Democrats')
print('-->',cd7_pv_22.loc[(cd7_pv_22.PARTY == 'DEM') & (cd7_pv_22.GENDER == 'Male')].shape[0],' Male Dems')
print('-->',cd7_pv_22.loc[(cd7_pv_22.PARTY == 'DEM') & (cd7_pv_22.GENDER == 'Female')].shape[0],' Female Dems')
print('\n')
print(cd7_pv_22.loc[(cd7_pv_22.PARTY == 'UAF')].shape[0],' Independents')
print('-->',cd7_pv_22.loc[(cd7_pv_22.PARTY == 'UAF') & (cd7_pv_22.GENDER == 'Male')].shape[0],' Male Inds')
print('-->',cd7_pv_22.loc[(cd7_pv_22.PARTY == 'UAF') & (cd7_pv_22.GENDER == 'Female')].shape[0],' Female Inds')
print('\n')

print('\n')
cd7_pv_22a28 = cd7_pv.loc[(cd7_pv['State Senate'] == 22) & (cd7_pv['State House'] == 28)]
print('Voters in both HD28 & SD22:')
print(cd7_pv_22a28.loc[(cd7_pv_22a28.PARTY == 'DEM')].shape[0],' Democrats')
print('-->',cd7_pv_22a28.loc[(cd7_pv_22a28.PARTY == 'DEM') & (cd7_pv_22a28.GENDER == 'Male')].shape[0],' Male Dems')
print('-->',cd7_pv_22a28.loc[(cd7_pv_22a28.PARTY == 'DEM') & (cd7_pv_22a28.GENDER == 'Female')].shape[0],' Female Dems')
print('\n')
print(cd7_pv_22a28.loc[(cd7_pv_22a28.PARTY == 'UAF')].shape[0],' Independents')
print('-->',cd7_pv_22a28.loc[(cd7_pv_22a28.PARTY == 'UAF') & (cd7_pv_22a28.GENDER == 'Male')].shape[0],' Male Inds')
print('-->',cd7_pv_22a28.loc[(cd7_pv_22a28.PARTY == 'UAF') & (cd7_pv_22a28.GENDER == 'Female')].shape[0],' Female Inds')
print('\n')

cd7_pv_22o28 = cd7_pv.loc[(cd7_pv['State Senate'] == 22) | (cd7_pv['State House'] == 28)]
print('Voters in either HD28 OR SD22:',cd7_pv_22o28.shape[0])
print(cd7_pv_22o28.loc[(cd7_pv_22o28.PARTY == 'DEM')].shape[0],' Democrats')
print('-->',cd7_pv_22o28.loc[(cd7_pv_22o28.PARTY == 'DEM') & (cd7_pv_22o28.GENDER == 'Male')].shape[0],' Male Dems')
print('-->',cd7_pv_22o28.loc[(cd7_pv_22o28.PARTY == 'DEM') & (cd7_pv_22o28.GENDER == 'Female')].shape[0],' Female Dems')
print('\n')
print(cd7_pv_22o28.loc[(cd7_pv_22o28.PARTY == 'UAF')].shape[0],' Independents')
print('-->',cd7_pv_22o28.loc[(cd7_pv_22o28.PARTY == 'UAF') & (cd7_pv_22o28.GENDER == 'Male')].shape[0],' Male Inds')
print('-->',cd7_pv_22o28.loc[(cd7_pv_22o28.PARTY == 'UAF') & (cd7_pv_22o28.GENDER == 'Female')].shape[0],' Female Inds')
print('\n')

cd7_pv_22o28o32 = cd7_pv.loc[(cd7_pv['State Senate'] == 22) | (cd7_pv['State House'] == 28) | (cd7_pv['State House'] == 32)]
print('Voters in HD28 OR SD22 OR HD32:',cd7_pv_22o28o32.shape[0])
print(cd7_pv_22o28o32.loc[(cd7_pv_22o28o32.PARTY == 'DEM')].shape[0],' Democrats')
print('-->',cd7_pv_22o28o32.loc[(cd7_pv_22o28o32.PARTY == 'DEM') & (cd7_pv_22o28o32.GENDER == 'Male')].shape[0],' Male Dems')
print('-->',cd7_pv_22o28o32.loc[(cd7_pv_22o28o32.PARTY == 'DEM') & (cd7_pv_22o28o32.GENDER == 'Female')].shape[0],' Female Dems')
print('\n')
print(cd7_pv_22o28o32.loc[(cd7_pv_22o28o32.PARTY == 'UAF')].shape[0],' Independents')
print('-->',cd7_pv_22o28o32.loc[(cd7_pv_22o28o32.PARTY == 'UAF') & (cd7_pv_22o28o32.GENDER == 'Male')].shape[0],' Male Inds')
print('-->',cd7_pv_22o28o32.loc[(cd7_pv_22o28o32.PARTY == 'UAF') & (cd7_pv_22o28o32.GENDER == 'Female')].shape[0],' Female Inds')
print('\n')

print('\n')
print('Breakdown of HD32 (DM\'s seat)')
cd7_pv_32 = cd7_pv.loc[(cd7_pv['State House'] == 32)]
print(cd7_pv_32.shape[0],' primary voters')

print(cd7_pv_32.loc[(cd7_pv_32.PARTY == 'DEM')].shape[0],' Democrats')
print('-->',cd7_pv_32.loc[(cd7_pv_32.PARTY == 'DEM') & (cd7_pv_32.GENDER == 'Male')].shape[0],' Male Dems')
print('-->',cd7_pv_32.loc[(cd7_pv_32.PARTY == 'DEM') & (cd7_pv_32.GENDER == 'Female')].shape[0],' Female Dems')
print('\n')
print(cd7_pv_32.loc[(cd7_pv_32.PARTY == 'UAF')].shape[0],' Independents')
print('-->',cd7_pv_32.loc[(cd7_pv_32.PARTY == 'UAF') & (cd7_pv_32.GENDER == 'Male')].shape[0],' Male Inds')
print('-->',cd7_pv_32.loc[(cd7_pv_32.PARTY == 'UAF') & (cd7_pv_32.GENDER == 'Female')].shape[0],' Female Inds')
print('\n')

#for aZip in set(cd7_pv['RESIDENTIAL_ZIP_CODE']):
#    #if cd7_pv.loc[cd7_pv.RESIDENTIAL_ZIP_CODE == aZip].shape[0] > 1e4:
#    #if cd7_pv.loc[(cd7_pv.RESIDENTIAL_ZIP_CODE == aZip) & (cd7_pv['State House'] == 28)].shape[0]:
#    print(cd7_pv.loc[(cd7_pv.RESIDENTIAL_ZIP_CODE == aZip)].shape[0],'in',aZip)

   


#  VOTER_ID,"COUNTY","FIRST_NAME","MIDDLE_NAME","LAST_NAME","NAME_SUFFIX","REGISTRATION_DATE","EFFECTIVE_DATE","LAST_UPDATED_DATE","OLD_VOTER_ID","PHONE_NUM","HOUSE_NUM","HOUSE_SUFFIX","PRE_DIR","STREET_NAME","STREET_TYPE","POST_DIR","UNIT_TYPE","UNIT_NUM","RESIDENTIAL_ADDRESS","RESIDENTIAL_CITY","RESIDENTIAL_STATE","RESIDENTIAL_ZIP_CODE","RESIDENTIAL_ZIP_PLUS","MAILING_ADDRESS_1","MAILING_ADDRESS_2","MAILING_ADDRESS_3","MAILING_CITY","MAILING_STATE","MAILING_ZIP_CODE","MAILING_ZIP_PLUS","MAILING_COUNTRY","VOTER_STATUS","STATUS_REASON","PARTY","GENDER","BIRTH_YEAR","PRECINCT_CODE","PRECINCT_NAME","Federal","Congressional","Statewide","State Board of Education - At Large","State Board of Education","University of Colorado Regents - At Large","University of Colorado Regents","State Senate","State House","Judicial","Regional Transportation","County Commissioner","Countywide","Municipality","City Ward and Precinct","City Sub","City Ward/District","School","Ambulance","Fire Protection","Fire Protection 2","Fire Protection 3","Local Improvement","Metropolitan","Metropolitan 2","Metropolitan 3","Park and Recreation","Park and Recreation 2","Park and Recreation 3","Park and Recreation Sub","Proposed","Proposed 2","Sanitation","Sanitation 2","Scientific Cultural Facilities","Water and Sanitation","Water and Sanitation 2","Water and Sanitation 3","Water Conservancy","Water","Water 2"
