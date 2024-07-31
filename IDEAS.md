IDEAS


* (core) Port to Go, Rust, or Zig
* (core) Play sounds on common events, checking for these binaries: aplay, paplay pw-play, ffplay
* (core) Allow internet usage in intervals of 5 minutes (ON/OFF).
* (core) Make it so that for each minute without internet, you get a minute (or two) with internet. You start with 5 minutes each session.
    * (sticky) Show the amout of internet time in the sticky module.
* (core) A secondary service which only purpose is to ensure the aboutlife service is alive. It checks it every 10 minutes, and if the service has stayed dead more than 1 hour then it revives it.
* (core) After setting a task to take more than 30 minutes, the next immediate task must be less than 30 minutes. This would discourage chaining long lasting tasks together (very common when procrastinating), and encourage to pick better scoped tasks.
* (core) A "need youtube" setting. This would require integrating the "Youtube puzzle" web extension.
* (core) Increase the obligatory break time at late hours (like do nothing for 2 minutes webpage)
* (core) An option to start a task inside the overlay plugin. So the task can be completed with it opened.


* (overlay) (terminals) Button to reset terminal
* (overlay) Support multiple screens
* (overlay) Show last activity info near input for comparison
    * Additionaly it could suggest you to take a tomato break, after it detects that you have been having working nonstop.
* (overlay) Make it so you have to press a button to exit the tomato break screen. Locate this button alongside the other buttons (such as close tabs, and shutdown). The order of these buttons will be shuffled every time so the user has to make the concious desicion to press it instead of the others.
* (overlay) Alongside the "need internet" button, add a "shutdown on finish" button.
* (overlay) A module to visualize your pomodoro sessions and breaks.
* (overlay) task manager: A section that shows a list of the opened apps with icons and thumbnails and a way to close them. Similar to what GNOME does.
* (overlay) Before starting a task show a countdown screen for gettin ready and hyped up. Like Mario Kart's intro: 3, 2, 1, GO!
* (overlay) The ability to skip the Obligatory break by writting text in a textbox, like: "systemctl stop aboutlife".
* (overlay) The ability to open the layout window in the middle of session through the tray icon.
    * This would allow to access future modules like, music, task history, motivational media, etc.
* (overlay) A section to watch motivational media, including: images, videos, music, and pdfs. This could use regulation.
* (overlay) A simple seccion that shows a motivational image/quote each day or every 12/8 hours.
    * A section specifically made to encourage action, to address the fear to start, to take the first step. Like a quote with a pretty background maybe.
* (overlay) Once in a while, after you obligatory break screen ends, you will get to a different screen with a 1 minute countdown, a message: "We're closing your webpages.. Take a break.", a button: "Acelerate closing", and another button: "Keep my pages this time". This last button you have to click very quickly to fill a bar, if you stop clicking the bar slowly returns back to zero.
    * The idea is, to keep your pages you have to make an extra effort. But to automatically remove them just relax and do nothing.
    * Maybe some motivational images could show during the event. I'm thinking on making a reusable image viewer widget that could be embedded in other relevant screens.
* (overlay) Custom workplace with the ability to wrap X11 windows, useful for developing graphical applications. This might be a little bit too much for this project since at this point it could be confused with a virtual/pseudo window manager, which it isn't and shouldn't be.
* (overlay) A plugin in where you see a list of the last 7 days, and the upcoming 7 days, and you can specify a goal for each day, this way you can always have in mind, what "plan" do you have.
* (overlay) Alternatively from being able to specify a custom "task". Allow the creation of "goals", goals are displayed in a list, so, the user can choose to work on a specific goal.
* (overlay) on break screen show an anti eye strain activity, like safeeyes does.
* (overlay) A section where you are shown a series of screens/text one by one, and you have to click next to see the next one. You have to go through all. This screens could be: Email (webview), Birthdays (text file), Calendar, or other reminders. You could open it by yourself or it could pop up randomly sometimes.
* (overlay) Daily planner. A section that emulates the planning I do with my notebook. You can only specify, hour and goal; you could see it hovering the trayicon. And you can select a goal from there instead of writting one for starting a session.


* (tray) Add "tomato break" option to tray icon, this option would end the session and enter a tomato break.
* (sticky) The ability to lock the sticky module in place.
* (sticky) When the work session is about to end. Use visual cues in sticky, like Hyperfocus does. Maybe play a sound too. Use GtkDrawingArea.
* (sticky) Make it less intrusive by having a transparent background.
* (sticky) Each time a minute passes an animation plays, una animación de barrido de izq a der.
* (webext) At night hours make the "close tabs" function automatic


ARCHIVED


* (core) obligatory break time dependent on the amount of time it took to finish the task. So if a 30 minute task is finished in 5 minutes, you would calculate the break time using the 5 minutes, no the 30.
* (core) Require a minimum amount of words for the task description.
* (webext) Open a helpful/motivational webpage when targeted site detected.
* (webext) Close targeted site tabs for webpages there's no way I'm doing something productive there.


* (overlay) Terminal on it's own tab, so that the user has a big area to work with. It's always and ideal scenario if the task can be done on the terminal.
    * The user could continue their work session inside and outside aboutlife's overlay, using terminal multiplexer tools like tmux, screen, tywm.
    * For users that prefer grafical tiling window managers instead of terminal multiplexers a special application/compatibility/translator/state tool could be developed for that use case.
* (overlay) (terminals) Dialog to specify a tmux session and instantly switch all terminals to that session, each terminal should show a different tmux's window.
* (overlay) Put something visually attractive in the tomato break screen, so that you don't look away and ignore the action buttons.
    * I was thinking about a picture a thinking roman statue.


* (sticky) "Discrete" option, in this option the sticky it's only show 3 seconds every minute. So to not disable it entirely.
