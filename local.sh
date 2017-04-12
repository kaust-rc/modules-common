export MANPATH=:

export KAUST_APPS_ROOT=/opt/share

export KAUST_MODULES_ROOT=$KAUST_APPS_ROOT/modules

rel=$(lsb_release -d | gawk -F"\t" '{print $2}')
os=$([[ $rel == *"Ubuntu"* ]] && echo ubuntu || echo centos)
# Order is important here, paths first in thew list have precedence
MODULEPATH=~/local/modulefiles:$KAUST_MODULES_ROOT/$os:$KAUST_MODULES_ROOT/applications
MODULEPATH=$MODULEPATH:$KAUST_MODULES_ROOT/compilers:$KAUST_MODULES_ROOT/libs:$KAUST_MODULES_ROOT/sets
export MODULEPATH
