import pandas as pd
import csv

def drop_ext_spaces(mystr):
    mystr = mystr.replace('  ','')
    if len(mystr)>0 and mystr[ 0] == ' ': mystr = mystr[1:]
    if len(mystr)>0 and mystr[-1] == ' ': mystr = mystr[:-1]
    return mystr  

def preprocessing(dir):
    f1 = dir+'usc08.lst'
    f2 = dir+'usc_AllHis.LST'

    name_f, name_l, name_m, name_s = [],[],[],[]
    year_birth, year_age, sex = [],[],[]
    id, date_reg = [],[]
    addr_pref, addr_num, addr_suff, addr_street, addr_ext, addr_city, addr_state, addr_zip = [],[],[],[],[],[],[],[]
    mail_1, mail_2, mail_3, mail_4, mail_5 = [],[],[],[],[]
    code_cty,code_jur,code_ward,code_sch,code_mih,code_mis,code_con,code_com,code_vil,code_vip,code_scp = [],[],[],[],[],[],[],[],[],[],[]
    bool_pa,code_status,code_uocava = [],[],[]

    with open(f1) as f:
        reader = csv.reader(f)
    
        for row in reader:
            _str = str(row[0])
            #
            name_l.append(_str[ 0:35].replace(' ',''))# alpha, hyphens allowed
            name_f.append(_str[35:55].replace(' ',''))# alpha only (no spaces)
            name_m.append(_str[55:75].replace(' ',''))# alpha only (no spaces)
            name_s.append(_str[75:78].replace(' ',''))# JR, SR, or I-V
            #
            year_birth.append(int(_str[78:82]))# YYYY
            year_age.append(2018-year_birth[-1])# age on election date
            #
            sex.append(_str[82:83])# sex (M or F)
            #
            date_reg.append(_str[83:91])# voter registration date (MMDDYYYY)
            #
            addr_pref.append(_str[91:92])# alpha prefix to house num
            addr_num.append(_str[92:99].replace(' ',''))# street number
            addr_suff.append(_str[99:103].replace(' ',''))# typically contains 1/2, direction, or hyphen
            #
            myst = _str[103:105].replace(' ','')+' '+drop_ext_spaces(_str[105:135])+' '+_str[135:141].replace(' ','')+' '+_str[141:143].replace(' ','')
            addr_street.append(drop_ext_spaces(myst.replace('  ',' ')))# street name+type+direction. elements separated by spaces inside string
            #
            addr_ext.append(drop_ext_spaces(_str[143:156]))# LOT#, APT#, etc. 
            addr_city.append(drop_ext_spaces(_str[156:191]))# city
            addr_state.append(_str[191:193])# state
            addr_zip.append(_str[193:198].replace(' ',''))
            #
            # Mailing address, if different from registration address
            mail_1.append(drop_ext_spaces(_str[198:248].replace('  ','')))
            mail_2.append(drop_ext_spaces(_str[248:298].replace('  ','')))
            mail_3.append(drop_ext_spaces(_str[298:348].replace('  ','')))
            mail_4.append(drop_ext_spaces(_str[348:398].replace('  ','')))
            mail_5.append(drop_ext_spaces(_str[398:448].replace('  ','')))        
            #
            id.append(_str[448:461].replace(' ','')) # ID number
            # ISSUE: 4460 voters (0.842%) seem not to have ID!
            # this also applies to other entries (eg, bool_pa)
            #
            code_cty.append(_str[461:463])# county
            code_jur.append(_str[463:468])# jurisdiction
            code_ward.append(_str[468:474])# ward precinct
            code_sch.append(_str[474:479])# school code
            code_mih.append(_str[479:484])# state house
            code_mis.append(_str[484:489])# state senate
            code_con.append(_str[489:494])# cd8
            code_com.append(_str[494:499])# county commissioner
            code_vil.append(_str[499:504])# village code
            code_vip.append(_str[504:510])# village precinct
            code_scp.append(_str[510:516])# school precinct
            #
            if _str[516:517] == 'Y': bool_pa.append(True)
            elif _str[516:517] == 'N': bool_pa.append(False)
            else: bool_pa.append(None)
            #
            code_status = _str[517:519].replace(' ','')
            code_uocava = _str[519:520].replace(' ','')

    df = pd.DataFrame({'age':year_age,'sex':sex,'cd':code_con,
                       'firstname':name_f,'lastname':name_l,'middlename':name_m,'suffixname':name_s,
                       'yearbirth':year_birth,'registrationdate':date_reg,
                       'addressnumprefix':addr_pref,'addressnum':addr_num,'addressnumsuffix':addr_suff,
                       'addressstreet':addr_street,'addressextension':addr_ext,'city':addr_city,'state':addr_state,'zip':addr_zip,
                       'mail1':mail_1,'mail2':mail_2,'mail3':mail_3,'mail4':mail_4,'mail5':mail_5,
                       'county':code_cty,'jurisdiction':code_jur,'ward_precinct':code_ward,
                       'school':code_sch,'statehouse':code_mih,'statesenate':code_mis,'countycommissioner':code_com,
                       'village':code_vil,'villageprecinct':code_vip,'schoolprecinct':code_scp,
                       'permabsentee':bool_pa,'statustype':code_status,'uocavastatus':code_uocava},index=id)

    df.to_csv(dir+'voter_file.csv')
