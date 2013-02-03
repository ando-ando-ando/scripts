#! /usr/python/bin/python
#  -*- coding: utf-8 -*- 

import datetime
from commands import getstatusoutput
from ftplib import FTP

ZFS_SNAPSHOT_DIR   = 'rpool/export/zones/'
ZFS_SNAPSHOT_CMD   = 'zfs snapshot -r ' + ZFS_SNAPSHOT_DIR
ZFS_SEND_CMD       = 'zfs send -rc ' + ZFS_SNAPSHOT_DIR
ZFS_DESTROY_CMD    = 'zfs destroy -r ' + ZFS_SNAPSHOT_DIR
GZIP_CMD           = ' | gzip  > '
GZIP_NAME          = '.zfs.img.gz'
ZFS_BACKUP_DIR     = '/export/backup/'
FTP_HOST           = '*.*.*.*'
FTP_USERNAME       = 'hoge'
FTP_PASSWORD       = 'fuga'

TODAY = datetime.datetime.today().strftime("%Y%m%d") 

class zfs_backup(object):
    def __init__(self):
        self.zfs_list = []

    def zfs_snapshot(self):
        (status, output) = getstatusoutput('zoneadm list')
        if status != 0:
            print "zoneadm list error code %s" % (status)
        else:
            #snapshot
            self.zfs_list = output.split()
            self.zfs_list.remove("global")
            if self.zfs_list == []:
                print "zoneがありません"
            else:
                for zone in self.zfs_list:
                    print ZFS_SNAPSHOT_CMD + zone + "@"  + TODAY + zone
                    print ZFS_SEND_CMD + zone + "@"  + TODAY + zone + GZIP_CMD + ZFS_BACKUP_DIR + TODAY + zone + GZIP_NAME
                    print ZFS_DESTROY_CMD + zone + "@"  + TODAY + zone
                    
                    zfs_snapshot_exec =  ZFS_SNAPSHOT_CMD + zone + "@"  + TODAY + zone
                    zfs_send_exec = ZFS_SEND_CMD + zone + "@"  + TODAY + zone + GZIP_CMD + ZFS_BACKUP_DIR + TODAY + zone + GZIP_NAME
                    zfs_destroy_exec = ZFS_DESTROY_CMD + zone + "@"  + TODAY + zone

                    getstatusoutput(zfs_snapshot_exec)
                    getstatusoutput(zfs_send_exec)
                    getstatusoutput(zfs_destroy_exec)

                    ftpput(FTP_HOST, FTP_USERNAME, FTP_PASSWORD, ZFS_BACKUP_DIR + TODAY + zone + GZIP_NAME )

def ftpput(host, username, password, putfile):
    try:
        _ftp = FTP(host, username, password)  # open(username, password)
        _ftp.cwd("/export/backup")            # cd /export/backup/
        _file = open(putfile, 'rb')           # bin バイナリモード
        command = "STOR " + putfile
        _ftp.storbinary(command, _file)       # put putfile
        _file.close()
        _ftp.quit()                           # bye
    except:
        print "ftpput_failed :" + putfile

def main():
    zf = zfs_backup()
    zf.zfs_snapshot()

if __name__ == '__main__':
    main()
