// config vars
var PORT = "13005";
var HELP_SITE = "";
var ENDPOINT_QUERY = `http://localhost:${PORT}/state`;
var ENDPOINT_RESET = `http://localhost:${PORT}/close_tabs_reset`;

const LATE_HOUR_LOWER = 20;
const LATE_HOUR_UPPER = 5;
const TIMEOUT_MS = 4000;
const WORKING_STATE_VALUE = 3; // see ../aboutlife/context.py
var previus_state = 0;

const SITES_TO_CLOSE = [
  "facebook.com",
  "twitter.com",
  "x.com",
  "newgrounds.com",
  "steampowered.com",
  "itch.io",
];
const SITES_TO_UNLOAD = [
  "youtube.com",
  "reddit.com",
  "imgur.com",
  "github.com",
  ...SITES_TO_CLOSE,
];

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    }, ms);
  });
}

async function close_tabs() {
  console.log("I: Closing tabs");

  try {
    tabs = await browser.tabs.query({});
    tabs.forEach(function (tab) {
      browser.tabs.remove(tab.id);
    });

    browser.tabs.create({});
  } catch (error) {
    console.error(error);
  }
}

function is_url_targeted(url) {
  return SITES_TO_UNLOAD.some((targeted_url) => {
    return url.includes(targeted_url);
  });
}

function is_url_unproductive(url) {
  return SITES_TO_CLOSE.some((targeted_url) => {
    return url.includes(targeted_url);
  });
}

// Unloads all tabs that are considered "targeted"

async function unload_tabs() {
  console.log("I: Unloading tabs");

  try {
    const active_tab = (await browser.tabs.query({ active: true }))[0];
    const is_active_tab_targeted = is_url_targeted(active_tab.url);
    const tabs_to_unload = [];
    const tabs_to_close = [];

    var perfect_candidate_tab_found = false;
    var candidate_tab = -1;

    tabs = await browser.tabs.query({});
    for (const tab of tabs) {
      const tab_info = await browser.tabs.get(tab.id);
      const is_targeted = is_url_targeted(tab_info.url);

      // Pick a tab to switch to if the current tab is targeted
      // Try to pick one that isn't discarded (unloaded)

      if (
        !perfect_candidate_tab_found &&
        is_active_tab_targeted &&
        !is_targeted
      ) {
        candidate_tab = tab.id;

        if (!tab_info.discarded) perfect_candidate_tab_found = true;
      }

      // Compile tabs to unload / close

      if (!tab_info.pinned) {
        if (is_url_unproductive(tab_info.url)) tabs_to_close.push(tab.id);
        else if (is_targeted) tabs_to_unload.push(tab.id);
      }
    }

    // Switch to untargeted tab before unloading tabs
    // Prefer to open the help site based on edge cases

    const hour = new Date().getHours();
    if (
      hour >= LATE_HOUR_LOWER ||
      hour <= LATE_HOUR_UPPER ||
      tabs_to_close.length
    ) {
      if (HELP_SITE != "") {
        browser.tabs.create({ url: HELP_SITE });
      } else {
        browser.tabs.create();
      }
    } else if (is_active_tab_targeted) {
      if (candidate_tab > -1) {
        await browser.tabs.update(candidate_tab, {
          active: true,
        });
      } else browser.tabs.create({});
    }

    tabs_to_unload.forEach((id) => {
      browser.tabs.discard(id);
    });

    tabs_to_close.forEach((id) => {
      browser.tabs.remove(id);
    });
  } catch (error) {
    console.error(error);
  }
}

async function loop() {
  while (true) {
    await sleep(TIMEOUT_MS);

    try {
      const query = await fetch(ENDPOINT_QUERY);
      if (query.status !== 200) continue;

      const body = await query.json();

      // unload if working state ended
      if (
        previus_state == WORKING_STATE_VALUE &&
        body.state != WORKING_STATE_VALUE
      ) {
        unload_tabs();
      }

      // close and reset
      if (body.close_tabs) {
        close_tabs();
        const putResponse = await fetch(ENDPOINT_RESET, {
          method: "PUT",
        });
      }

      previus_state = body.state;
    } catch (error) {
      console.error(error);
    }
  }
}

(async () => {
  console.log("I: Background script started");
  try {
    result = await browser.storage.local.get({
      port: PORT,
      help_page_url: "",
    });
    if (result.port != "") {
      PORT = result.port;
      ENDPOINT_QUERY = `http://localhost:${PORT}/state`;
      ENDPOINT_RESET = `http://localhost:${PORT}/close_tabs_reset`;
    }
    HELP_SITE = result.help_page_url;
    console.log(
      `Loaded config.\nport: ${result.port}, help_page_url: ${result.help_page_url}`,
    );
  } catch (error) {}
  loop();
})();
