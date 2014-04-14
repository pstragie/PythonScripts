if [ -f ~/.bashrc ]; then
 . ~/.bashrc
fi

#to reload this profile in your shell when making a change:
#source ~/.bash_profile

PATH=.:$PATH
#PATH=~/scripts:$PATH
#PATH=~/bioinf:$PATH
#PATH=~/bioinf/bin:$PATH

# Online promt generator http://www.kirsle.net/wizards/ps1.html
#PS1="\[\e[1;33m\][\u@\h]:\w$ \[\e[m\]" #color yellow=33, green=32, purple=35
PS1="\[$(tput bold)\]\[$(tput setaf 3)\][\u@\h]:\w\n\\$ \[$(tput sgr0)\]"

#set the color mode of your shell
d=true

#-------------------------------------------------------------
# The 'ls' family (this assumes you use a recent GNU ls).
#-------------------------------------------------------------
# Add colors for filetype and  human-readable sizes by default on 'ls':
alias ls='ls -h --color'
