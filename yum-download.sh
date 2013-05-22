#!/bin/bash
#This script grabs available yum updates
#and downloads them to a timestamp directory
#It also logs that this happened to /var/log/messages
#and creates log files for downloaded packages and currently
#installed packages

echo Running script $0 to cache yum updates

# Requests the current date and time from the OS and sets that as a variable
TIMESTAMP=`/bin/date '+%Y-%b-%d-%H%M'`

# Requests the hostname from the OS and sets that as a variable.
HOSTNAME=`/bin/hostname`

# Let the user know that the $TIMESTAMP and $HOSTNAME variables were set 
# correctly.
echo ""
echo Current host: $HOSTNAME
echo ""

# Clears all cached packages, dependency header files, package availability
# metadata, and metadata SQLite cache used by the yum process.
yum clean all

echo ""

# Make the current working /var/pkg directory. Make the /var/pkg and 
# /var/log/pkg directories if they do not exist.
/bin/mkdir -vp /var/pkg/$TIMESTAMP
/bin/mkdir -vp /var/log/pkg

# Create the log file.
echo $HOSTNAME-$TIMESTAMP > /var/log/pkg/$HOSTNAME-$TIMESTAMP-packages_updates.log

echo ""

# This line begins a foreach loop. More info on foreach loops can
# be found at http://en.wikipedia.org/wiki/Foreach. This particular
# loop will get a list of packages which need updating via 'yum check-update',
# grep for 'rhel-' to pull out any useless header or footer data, and send the
# list through awk to strip out everything except for the first field (which
# is the package name). The result is a list of packages suitable for use by
# the script.
for PACKAGE in `/usr/bin/yum check-update |/bin/grep 'rhel-' | /usr/bin/awk '{print $1}'`

# The first line has the script run the yumdownloader program for each package 
# in the list. yumdownloader is instructed to place the downloaded package into
# the new timestamped directory created above. 
#
# The second line appends a line to the log file for this iteration of the 
# script noting which package was downloaded.
do
/usr/bin/yumdownloader --destdir /var/pkg/$TIMESTAMP $PACKAGE
echo $PACKAGE >> /var/log/pkg/$HOSTNAME-$TIMESTAMP-packages_updates.log
echo ""

# At the end of the list, the loop is finished and should not continue to do 
# things.
done

#Creates a list of currently installed packages
echo $HOSTNAME-$TIMESTAMP > /var/log/pkg/$HOSTNAME-$TIMESTAMP-packages_current.log
/bin/rpm -qa >> /var/log/pkg/$HOSTNAME-$TIMESTAMP-packages_current.log

#Logs the script name and created updates directory to syslog /var/log/messages
/usr/bin/logger $0 created $TIMESTAMP

# Set a variable that is five less than the number of files in the /var/pkg
# directory.
ARCHCOUNT=$(( `/bin/ls -1 /var/pkg | /usr/bin/wc -l` - 5 ))

echo ""
echo "Removing stale packages from /var/pkg."

# It is now time for another foreach loop. This time we are starting by 
# generating a list that is all of the packages in /var/pkg minus the latest 
# five.
for STALEPACKAGE in `/bin/ls -1rt /var/pkg | /usr/bin/head -$ARCHCOUNT`

# For each package in the list, first we will let the user know that we're 
# going to remove it.
# 
# After we've let everyone know, we will then remove it.
do
#echo "Removing $STALEPACKAGE from /var/pkg."
/bin/rm -rf /var/pkg/$STALEPACKAGE && echo "Removed $STALEPACKAGE"
done

echo ""

# Set a variable that is ten less than the number of files in the /var/log/pkg
# directory.
LOGCOUNT=$(( `/bin/ls -1 /var/log/pkg | /usr/bin/wc -l` - 10 ))

echo "Removing stale logs from /var/log/pkg."

# Yet another foreach loop. This is the same stuff as above but we're doing it
# to the /var/log/pkg directory this time.
for STALELOG in `/bin/ls -1rt /var/log/pkg | /usr/bin/head -$LOGCOUNT`

# For each log file in the list, first we will let the user know that we're 
# going to remove it.
#
# After we've let everyone know, we will then remove it.
do
       #echo "Removing $STALELOG log data from /var/log/pkg."
       /bin/rm /var/log/pkg/$STALELOG && echo "Removed $STALELOG"
done
