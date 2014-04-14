# 12-2-2013 bart.verheyde@ugent.be v1.0
# example for .bash_profile in your hpc root
#

if [ -f ~/.bashrc ]; then
 . ~/.bashrc
fi

# Add current directorty to PATH
PATH=.:$PATH

# Add specific directortys to PATH
PATH=~/scripts:$PATH
PATH=~/bioinf:$PATH

#Format prompt so you know who and where you are
PS1="\u@\h:\w$ "

#set the color mode of your shell
d=true

#-------------------------------------------------------------
# The 'ls' family (this assumes you use a recent GNU ls).
#-------------------------------------------------------------
# Add colors for filetype and  human-readable sizes by default on 'ls':
alias ls='ls -h --color'
