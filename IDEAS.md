IDEAS

* Port to Go or Rust
* Button to reset terminal
* Play sound, checking for these binaries aplay, paplay pw-play, ffplay
* Support multiple screens
* At night hours make the "close tabs" function automatic
* Show last activity info near input for comparison
* Make it so you have to press a button to exit the tomato break screen. Locate this button alongside the other buttons (such as close tabs, and shutdown). The order of these buttons will be shuffled every time so the user has to make the concious desicion to press it instead of the others.
* Allow internet usage in intervals of 5 minutes (ON/OFF).
* Make it so that for each minute without internet, you get a minute (or two) with internet. You start with 5 minutes each session.
    * Show the amout of internet time in the sticky module.
* A secondary service which only purpose is to ensure the aboutlife service is alive. It checks it every 10 minutes, and if the service has stayed dead more than 1 hour then it revives it.
* Add "tomato break" option to tray icon, this option would end the session and enter a tomato break.
* The ability to lock the sticky module in place.
* After setting a task to take more than 30 minutes, the next immediate task must be less than 30 minutes. This would discourage chaining long lasting tasks together (very common when procrastinating), and encourage to pick better scoped tasks.

OVERLAY IDEAS

    * Alongside the "need internet" button, add a "shutdown on finish" button.
    * Put something visually attractive in the tomato break screen, so that you don't look away and ignore the action buttons.
    * Terminal on it's own tab, so that the user has a big area to work with. It's always and ideal scenario if the task can be done on the terminal.
    * A module to visualize your pomodoro sessions and breaks.
    * task manager: A section that shows a list of the opened apps with icons and thumbnails and a way to close them.
    * Alternatively from being able to specify a custom "task". Allow the creation of "goals", goals are displayed in a list, so, the user can choose to work on a specific goal.
    * Before starting a task show a countdown screen for preparing. Like Mario Kart's intro: 3, 2, 1, GO!
    * The ability to skip the Obligatory break by writting text in a textbox, like: "systemctl stop aboutlife".
    * The ability to open the layout window in the middle of session through the tray icon.
        * This would allow to access future modules like, music, task history, motivational media, etc.
    * A section to watch motivational media, including: images, videos, music, and pdfs. This could use regulation.
    * Once in a while, after you obligatory break screen ends, you will get to a different screen with a 1 minute countdown, a message: "We're closing your webpages.. Take a break.", a button: "Acelerate closing", and another button: "Keep my pages this time". This last button you have to click very quickly to fill a bar, if you stop clicking the bar slowly returns back to zero.
        * The idea is, to keep your pages you have to make an extra effort. But to automatically remove them just relax and do nothing.
        * Maybe some motivational images could show during the event. I'm thinking on making a reusable image viewer widget that could be embedded in other relevant screens.

DONE

* obligatory break time dependent on the amount of time it took to finish the task. So if a 30 minute task is finished in 5 minutes, you would calculate the break time using the 5 minutes, no the 30.
* Require a minimum amount of words for the task description.
* Open a helpful/motivational webpage when targeted site detected.
* Close targeted site tabs for webpages there's no way I'm doing something productive there.
