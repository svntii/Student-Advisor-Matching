#!/opt/homebrew/opt/python@3.9/bin/python3.9
# config.py

from collections import deque
import pdb
import numpy as np
import pandas as pd
import sys
import os
import imaplib
import base64
import email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

bot_email_id = 'matchmakernd@gmail.com'
bot_email_pass = '########'
subject_key = 'equest' # full protocol should be 'New Match Request'
adv_file_key = 'visor'
stu_file_key = 'udent'
dir_path = '/Users/solinakim/Desktop/CS_projects/preference-matcher/'
outf_name = 'match_results.csv'