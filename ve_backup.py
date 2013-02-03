#!/usr/local/bin/python
# -*- coding; utf-8 -*-

import argparse, commands, smtplib
from email.MIMEText import MIMEText
from email.Utils import formatdate

# Parse create
parser = argparse.ArgumentParser(description='vzbackup')

# Optional arguments
parser.add_argument('-e', '--ctid', required=True, type=int,help='list of CTs to backup')
parser.add_argument('-type', '--type', required=True, help='backup type')
parser.add_argument('-state', '--state', required=True, default='', help='ve state backup')
parser.add_argument('-d', '--dest', required=True,help='backup target node')

def backup_start(args):
    val = {'ctid':args.ctid,
           'type':args.type,
           'state':args.state,
           'dest':args.dest }

    cod = "-%(type)s -%(state)s %(dest)s -e %(ctid)s" % val
    cmd = "/usr/sbin/vzbackup -Cg -p --no-split " + cod

    return commands.getstatusoutput(cmd)

def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg

def send(from_addr, to_addr, msg):
    s = smtplib.SMTP('127.0.0.1')
    s.sendmail(from_addr, [to_addr], msg.as_string())
    s.close()

if __name__ == "__main__":

    # The argument of a command line is interpreted
    args = parser.parse_args()

    (res, msg) = backup_start(args)
    message = "%d %s" % (res,msg)
    print message

    from_addr = 'hoge@hoge'
    to_addr = 'hoge@hoge'
    subject = 'hoge'
    body = message
    msg = create_message(from_addr, to_addr, subject, body)
    send(from_addr, to_addr, msg)