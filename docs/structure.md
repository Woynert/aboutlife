

# plain list features

- daemon: Manages all features, it's always alive
- tray plugin: Allows to trigger some actions
- window plugin: Shows buttons and controls
    - terminal plugin: Allows the user to execute commands whilst in rest mode
- REST server: Allows web plugins to query the current state 
- Web plugin: Allows controlling the web browser remotelly

# plugins structure

var shared_data: a reference to the global state (shared data)

setup(): contains all callbacks this plugin may need

process(): runs every tick

health_check() -> bool: info useful for restarting the plugin

cleanup(): frees resources on exit


