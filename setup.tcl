#%Module 1.0 -*- tcl -*-

# Set some global variables that we need here and in the module file
set ::module_name [lrange [split [module-info name] /] 0 0]
set ::version [lrange [split [module-info name] /] 1 1]
set ::module_build [file tail [module-info name]]
set ::distro el6


# Log what's happening
exec $env(KAUST_MODULES_ROOT)/common/log.sh --mode [module-info mode] \
     --name [module-info name] --path $ModulesCurrentModulefile &


proc GetDirName { appsroot appname } {
    set dirlist [glob -nocomplain -directory $appsroot -tails *]
    return [lsearch -inline -nocase [split $dirlist] $appname]
}


proc SetAppDir { suffix_dir { app_dir_env 0 } } {
    #KAUST APPNAME
    set module_name_uc [string toupper $::module_name]
    regsub -all {[\-]} ${module_name_uc} "_" KAUST_APPNAME
    setenv KAUST_APPNAME ${KAUST_APPNAME}

    if { $app_dir_env == 0 } {
        set app_dir_env ${KAUST_APPNAME}_ROOT
    }

    # app_root
    if { [info exists ::env(KAUST_APPS_ROOT)] } {
        set ::apps_root $::env(KAUST_APPS_ROOT)
    } else {
        set ::apps_root /opt/share
    }

    set ::dir_name [GetDirName $::apps_root $::module_name]

    # app_dir
    if { [info exists ::env(${app_dir_env})] } {
        set ::app_dir $::env(${app_dir_env})
    } else {
        set ::app_dir $::apps_root/$::dir_name/$suffix_dir

        #Do we need to fallback
        if { [file exists $::app_dir] == 0 } {
            set ::app_dir [string map "/$::distro /el6" $::app_dir]
        }
    }

    # out of the if-stm, to be shown on "module show"
    setenv ${app_dir_env} $::app_dir
}


proc GeneralModulesHelp {} {
    puts stderr "\tThis module loads $::module_name version $::version\n"
}


proc SetWhatis {} {
    set curpath [file dirname $::ModulesCurrentModulefile]
    set desc_file [join [read [open "$curpath/.desc"]]]
    module-whatis "$desc_file"
}


proc ReportModuleUsage {} {
    switch [module-info mode] {
        load {
            puts stderr "Loading module $::module_name version $::version"
        }
        remove {
            puts stderr "Unloading module $::module_name version $::version"
        }
    }
}


proc GeneralAppSetup { { suffix_dir 0 } { app_dir_env 0 } } {
    proc ModulesHelp { } {
        GeneralModulesHelp
    }

    # Set default suffix_dir to Version/Build, e.g. 5.5.1/openmpi2.3.0-gcc4.9.0
    if { $suffix_dir == 0 } {
        set comparison [string compare ${::version} ${::module_build}]
        if {$comparison == 0} {
            set suffix_dir ${::version}
        } else {
            set suffix_dir ${::version}/${::module_build}
        }
    }

    SetAppDir $suffix_dir $app_dir_env

    SetWhatis

    ReportModuleUsage

    conflict $::module_name
}


proc GeneralCompilerSetup { { suffix_dir 0 } { app_dir_env 0 } } {
    if { $suffix_dir == 0 } { set suffix_dir ${::version} }
    GeneralAppSetup $suffix_dir $app_dir_env
}


proc GeneralLibSetup { { suffix_dir 0 } { app_dir_env 0 } } {
    if { $suffix_dir == 0 } { set suffix_dir ${::version} }
    GeneralAppSetup $suffix_dir $app_dir_env
}


proc is_cluster { cluster_name } {
    if { $::env(KAUST_CLUSTER) == $cluster_name } {
        return 1
    } else {
        return 0
    }
}


proc AddDeps { csv_list } {
    # Process dependancies
    set modules_to_load [split $csv_list ","]
    foreach line $modules_to_load {
        if { $line != "" } {
            set line [string trim $line]
            if ![is-loaded $line] {
                module add $line
            }
        }
    }
}


proc AddDepsBasedOnCompiler {} {
    # Load compiler based on module build
    set module_to_load [string map {- /} $::module_build]

    AddDeps "$module_to_load"
}


proc AddDepsBasedOnMpiCompiler {} {
    # Load compiler based on module build
    # Find last dash in the string
    set last_dash_index [expr [string last - $::module_build] - 1]
    # Get substring containing first two dashes
    set substring [string range $::module_build 0 $last_dash_index]
    set middle_dash_index [expr [string last - $substring] - 1]
    # Extract MPI library/compiler from module build
    set mpi [string range $::module_build 0 $middle_dash_index]
    # Extract compiler from module build. We have to readd offsets we took off before
    set compiler [string range $::module_build [expr $middle_dash_index + 2] end]
    set module_to_load [string map {- /} $mpi]/$compiler

    AddDeps "$module_to_load"
}
