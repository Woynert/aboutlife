const TIMEOUT_MS = 4000;
var PORT = "8080";
var ENDPOINT_QUERY = `http://localhost:${PORT}/state`;
var ENDPOINT_RESET = `http://localhost:${PORT}/close_tabs_reset`;

var previus_state = 0;
const WORKING_STATE_VALUE = 3; // see ../aboutlife/context.py
const TARGET_SITES = [
  "youtube.com",
  "reddit.com",
  "imgur.com",
  "facebook.com",
  "twitter.com",
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
  return TARGET_SITES.some((targeted_url) => {
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

      // Compile tabs to unload

      if (is_targeted && !tab_info.pinned) {
        tabs_to_unload.push(tab.id);
      }
    }

    // Switch to untargeted tab before unloading tabs

    if (is_active_tab_targeted) {
      if (candidate_tab > -1) {
        await browser.tabs.update(candidate_tab, {
          active: true,
        });
      } else browser.tabs.create({});
    }

    tabs_to_unload.forEach((id) => {
      browser.tabs.discard(id);
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
      port: "8080",
      homepage: "",
    });
    if (result.port != "") {
      PORT = result.port;
      ENDPOINT_QUERY = `http://localhost:${PORT}/state`;
      ENDPOINT_RESET = `http://localhost:${PORT}/close_tabs_reset`;
    }
  } catch (error) {}
  loop();
})();
