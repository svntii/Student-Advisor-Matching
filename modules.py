#!/opt/homebrew/opt/python@3.9/bin/python3.9
# modules.py

from config import *

##########################################

########## SETUP STARTS HERE #############

##########################################

def receive_email():
    
    # logging in to email
    mail = imaplib.IMAP4_SSL("imap.gmail.com", 993)
    mail.login(bot_email_id, bot_email_pass) # program's email id and password, stored as strings in config
    mail.select('"Inbox"')

    # searching for request email
    req_found = False
    _,data = mail.search(None, 'ALL')

    for email_id in data[0].split():
        _,data = mail.fetch(email_id, '(RFC822)')
        raw_email = data[0][1].decode('utf-8')
        email_content = email.message_from_string(raw_email)

        if subject_key in email_content['Subject']:
            req_found = True
            client_email = email.utils.parseaddr(email_content['From'])[1]
            print(f'Recived request from: {client_email}')
            break
    
    if not req_found:
        print('Error: request email not found.')
        return -1

    # email is found
    # moving on to downloading csv files

    for part in email_content.walk():
        if part.get_content_maintype() == 'multipart':
            continue
        if part.get('Content-Disposition') is None:
            continue

        filename = part.get_filename()
        if adv_file_key in filename:
            adv_csv = os.path.join(dir_path, 'advisor.csv')
            att_path = adv_csv
        elif stu_file_key in filename:
            stu_csv = os.path.join(dir_path, 'student.csv')
            att_path = stu_csv
        else:
            print('Error: invalid attachments')
            return

        if not os.path.isfile(att_path):
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
    
    # logging out of email
    mail.store(email_id, '+FLAGS', r'(\Deleted)') # flagging as read, will actually delete at logout

    try:
        mail.close()
    except:
        pass
    mail.logout()

    return adv_csv, stu_csv, client_email

def send_email(client_email='kkim24@nd.edu'):

    # creating a multipart message
    msg = MIMEMultipart()
    msg['Subject'] = 'Match Results'
    msg['From'] = bot_email_id
    msg['To'] = client_email

    # attaching csv file
    with open(dir_path+outf_name, 'rb') as file:
        msg.attach(MIMEApplication(file.read(), Name=outf_name))
    
    # establishing connection
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls() # for security measures
    server.login(bot_email_id, bot_email_pass)

    # sending email
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    print(f"Successfully emailed results to {client_email}")

    # terminate the session
    server.quit()

    return

def read_student_prefs(df):
    
    student_pref = {}
    
    for index, row in df.iterrows():
        net_id = row['Net ID']
        student_pref[net_id] = []
        i = 1
        while len(row.index[row==i]) != 0:
            student_pref[net_id].append(row.index[row==i][0].split('[')[-1][:-1])
            i += 1
    
    return student_pref

def read_advisor_prefs(df):
    
    adv_pref = {}
    df = df.drop(columns=['Capacity'], axis=1)

    for index, row in df.iterrows():
        net_id = row['Net ID']
        adv_pref[net_id] = []
        i = 1
        while len(row.index[row==i]) != 0:
            adv_pref[net_id].append(row.index[row==i][0].split('[')[-1][:-1])
            i += 1
    
    return adv_pref

def read_advisor_caps(df):
    adv_cap = {}
    for index, row in df.iterrows():
        net_id = row['Net ID']
        adv_cap[net_id] = int(row['Capacity'])
   
    return adv_cap

def generate_results_df(final_list):

    final_df = pd.DataFrame(final_list, columns = ['Students', 'Advisor'])

    # changing order of columns to advisor, student
    cols = ['Advisor', 'Students']
    final_df = final_df[cols]

    return final_df

def clean_up():
    try:
        os.remove(dir_path+outf_name)
        os.remove(dir_path+'advisor.csv')
        os.remove(dir_path+'student.csv')
    except:
        print('Failed to remove files from filesystem')
    return

##########################################

## PREFERENCE MATCHING ALGO STARTS HERE ##

##########################################

def pref_to_rank(pref, student_netid):
    # indexing advisors preferences
    final = { a: {s: idx for idx, s in enumerate(a_pref)}
    for a, a_pref in pref.items()}

    # gives any student not in advisors preferences a value of -1
    for student in student_netid:
        for advisor, pref in final.items():
            if student not in pref:
                final[advisor].update({student : -1})

    return final

def matching_algorithm(student_netid, advisors, student_pref, adv_pref, adv_cap):
    advisors_rank = pref_to_rank(adv_pref, student_netid)
    # create a deque for student_pref
    ask_list = {student: deque(adv) for student, adv in student_pref.items()}
    pair = {}
    remaining_students = set(student_netid)
    while len(remaining_students) > 0:
        # popping from set chooses a random student 
        student = remaining_students.pop()

        # sets students first pref to adv 
        adv = ask_list[student].popleft()
        if adv_cap[adv] > 0: # if student is not in list already
            # if advisor isnt in pair we need to consider cap
            pair_insert(pair, student, adv, adv_cap)
            adv_cap[adv] -= 1

        else:
            # student0 is least preferred student that adv is matched to
            student0 = pair[adv].pop() 
            adv_prefer_student0 = advisors_rank[adv][student0] <= advisors_rank[adv][student] # made this to less than or equal to 
            if adv_prefer_student0:
                remaining_students.add(student)
            else:
                remaining_students.add(student0)
                pair_insert(pair, student, adv, adv_cap)
        
        # if students don't have any more preferences but are not yet matched
        if not matches_remaining(remaining_students, ask_list):
            leftover_pairing(remaining_students, pair, adv_cap)
            break

    return [(student, adv) for adv, student in pair.items()]

def pair_insert(pair, student, adv, adv_cap):
    if adv not in pair:
        pair[adv] = [student]
    else:
        pair[adv].append(student)

def matches_remaining(remaining_students, ask_list):
    # remaining students will only have netid
    # ask_list to see if deque is empty
    # using remaining students to cross reference deque to kick out of loop
    for student in remaining_students:
        if ask_list[student]:
            return True
        else:
            pass

    return False

def leftover_pairing(remaining_students, pair, adv_cap):
    # inserts all the empty students in first come first serve for advisor
    while len(remaining_students) > 0:
        # sorting the dictionary by length of value
        sorted(pair, key=lambda advisor: len(pair[advisor]))
        for adv in pair:
            if adv_cap[adv] != 0:
                student = remaining_students.pop()
                pair_insert(pair, student, adv, adv_cap)
                adv_cap[adv] -= 1
                break # want to fill the least filled first and keep on going

