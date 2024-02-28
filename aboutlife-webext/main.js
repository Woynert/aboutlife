const TIMEOUT_MS = 4000;
var PORT = "8080";
var ENDPOINT_QUERY = `http://localhost:${PORT}/close_tabs_query`;
var ENDPOINT_RESET = `http://localhost:${PORT}/close_tabs_reset`;

function log(str) {
  console.log(str);
}

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    }, ms);
  });
}

async function close_tabs() {
  log("I: Closing tabs");

  try {
    tabs = await browser.tabs.query({});
    tabs.forEach(function (tab) {
      browser.tabs.remove(tab.id);
    });

    browser.tabs.create({});
  } catch (error) {
    log(error);
  }
}

async function loop() {
  while (true) {
    await sleep(TIMEOUT_MS);

    try {
      const response = await fetch(ENDPOINT_QUERY);

      if (response.status === 200) {
        close_tabs();

        // reset
        const putResponse = await fetch(ENDPOINT_RESET, {
          method: "PUT",
        });
      }
    } catch (error) {}
  }
}

browser.runtime.onInstalled.addListener(async () => {
  try {
    result = await browser.storage.local.get({
      port: "8080",
      homepage: "",
    });
    if (result.port != "") {
      PORT = result.port;
      ENDPOINT_QUERY = `http://localhost:${PORT}/close_tabs_query`;
      ENDPOINT_RESET = `http://localhost:${PORT}/close_tabs_reset`;
    }
  } catch (error) {}

  loop();
});
