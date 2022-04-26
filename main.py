#!/opt/homebrew/opt/python@3.9/bin/python3.9
# main.py

from config import *
from modules import *

# PUT EVERYTHING TOGETHER :)

def main():
    #
    adv_csv, stu_csv, client_email = receive_email()

    adv_df = pd.read_csv(adv_csv)
    stu_df = pd.read_csv(stu_csv)

    student_pref = read_student_prefs(stu_df)
    adv_pref = read_advisor_prefs(adv_df)
    adv_cap = read_advisor_caps(adv_df)

    student_netid = student_pref.keys()
    advisors = adv_pref.keys()

    print(student_pref)
    print(adv_pref)
    print(adv_cap)
    print(student_netid)
    print(advisors)
    print('\nSETUP COMPLETE\n')

    #pref_to_rank( adv_pref, student_netid )
    final_matches = matching_algorithm(student_netid, advisors, student_pref, adv_pref, adv_cap)
    final_df = generate_results_df(final_matches)

    print('MATCHING COMPLETE\n')
    print(final_df)

    final_df.to_csv(dir_path+outf_name)
    send_email(client_email)

    # cleaning up...

    clean_up()
    
    return

main()