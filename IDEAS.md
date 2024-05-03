IDEAS
* Port to Go or Rust
* Button to reset terminal
* Play sound, checking for these binaries aplay, paplay pw-play, ffplay
* Support multiple screens
* At night hours make the "close tabs" function automatic
* Show last activity info near input for comparison
* Make it so you have to press a button to exit the tomato break screen. Locate this button alongside the other buttons (such as close tabs, and shutdown). The order of these buttons will be shuffled every time so the user has to make the concious desicion to press it instead of the others.
* Put something visually attractive in the tomato break screen, so that you don't look away and ignore the action buttons.
* Plugins for the overlay plugin:
    * Terminal on it's own tab, so that the user has a big area to work with. It's always and ideal scenario if the task can be done on the terminal.
    * A module to visualize your pomodoro sessions and breaks.
    * task manager: A section that shows a list of the opened apps with icons and thumbnails and a way to close them.
    * Alternatively from being able to specify a custom "task". Allow the creation of "goals", goals are displayed in a list, so, the user can choose to work on a specific goal.
    * Before starting a task show a countdown screen for preparing. Like Mario Kart's intro: 3, 2, 1, GO!
    * A section to watch motivational media, including: images, videos, music, and pdfs. This could use regulation.
* Alongside the "need internet" button, add a "shutdown on finish" button.
* Allow internet usage in intervals of 5 minutes (ON/OFF).
* Make it so that for each minute without internet, you get a minute (or two) with internet. You start with 5 minutes each session.
    * Show the amout of internet time in the sticky module.
* A secondary service which only purpose is to ensure the aboutlife service is alive. It checks it every 10 minutes, and if the service has stayed dead more than 1 hour then it revives it.
* The ability to open the layout window in the middle of session through the tray icon.
    * This would allow to access future modules like, music, task history, motivational media, etc.
* The ability to skip the Obligatory break by writting text in a textbox, like: "systemctl stop aboutlife".
* Add "tomato break" option to tray icon, this option would end the session and enter a tomato break.

DONE
* obligatory break time dependent on the amount of time it took to finish the task. So if a 30 minute task is finished in 5 minutes, you would calculate the break time using the 5 minutes, no the 30.
* Require a minimum amount of words for the task description.