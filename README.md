# modules-common
Common module files for KAUST RC systems.

We're maintaining, in this repository, all files necessary to load what modules are being loaded by who and from where:

* **setup.tcl** used to configure and give common functions to RC modules environment;
* **addlog.py** used by common setup machinery to log what is being used by users. Logs are written to a MySQL DB so we can then generate reports based on this data. We use ELK stack to generate these reports.
  * Logs are collected in background so normal module file flow will not be interrupted
  * Server running **server.py** needs the following:
    * Python 2.7 or higher with the packages:
      * **cherrypy**
      * **python-ldap**
    * Being reachable by all nodes on KAUST network
    * Having _Apache_ server running on port 80 configured to reverse proxy to _localhost:8080_
    * **MySQL DB** running with Python connector installed
    * Use **createtables.py** to load MySQL with logging table
