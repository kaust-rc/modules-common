# modules-common
Common module files for KAUST RC systems.

We're maintaining two major files in this repository:

* **setup.tcl** used to configure and give common functions to RC modules environment;
* **addlog.py** used by common setup machinery to log what is being used by users. Logs are written to a MySQL DB so we can then generate reports based on this data.
  * Logs are collected in background so normal module file flow will not be interrupted
  * Server running **server.py** needs the following:
    * Being reachable by all nodes on KAUST network
    * Having _Apache_ server running on port 80 configured to reverse proxy to _localhost:8087_
    * **MySQL DB** running with Python connector installed
    * Having **pythion-ldap** installed
