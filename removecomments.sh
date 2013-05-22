#!/bin/bash
#
#Chase Pettet 2009
#
#This script removes the comments from a config file.
#Usage is ./removecomments.sh Commented_file Uncommented_file
#
if [ $# -eq 0 ]  # Must have command-line args to demo script.
       then
               echo "This script requires two options separated by a space.  Ex. ORIGINAL-FILE and SANS-COMMENTS-FILE."
       exit 0
fi
#
sed '/^\#/d' $1 > $2
