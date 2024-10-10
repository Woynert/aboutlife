var PORT = "8080";

document.addEventListener("DOMContentLoaded", function () {
  // load
  browser.storage.local
    .get({
      port: "8080",
      help_page_url: "",
    })
    .then((result) => {
      document.getElementById("tbx_port").value = result.port;
      document.getElementById("tbx_help_page_url").value = result.help_page_url;
    });

  // save
  document.getElementById("btn_save").addEventListener("click", function () {
    PORT = document.getElementById("tbx_port").value;
    const help_page_url = document.getElementById("tbx_help_page_url").value;
    browser.storage.local.set({
      port: PORT,
      help_page_url: help_page_url,
    });
  });

  loop();
});

function sleep(ms) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve();
    }, ms);
  });
}

async function loop() {
  while (true) {
    console.log("I: Checking connection");
    await sleep(1000);
    try {
      const response = await fetch(`http://localhost:${PORT}/state`);
      document.getElementById("lbl_info").innerText = "Connection status: OK";
    } catch (error) {
      document.getElementById("lbl_info").innerText =
        "Connection status: UNREACHABLE";
    }
  }
}
