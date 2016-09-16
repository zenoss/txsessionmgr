# txsessionmgr
Manager for keeping track of single login sessions

* SessionManager is the class that will keep track of sessions for all devices
* There will be one SESSION_MANAGER created during the first import of module
* A Client will:
** Keep track of the single SESSION_MANAGER
** Contain a unique key for each device
** Initiate the login procedure by calling init_connection in the SESSION_MANAGER
** Initiate the close procedure by calling close_connection in the SESSION_MANAGER
* A Session will:
** Perform the login/logout procedures
** Send/Receive requests
** Handle responses