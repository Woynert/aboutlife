var PORT = "8080";

document.addEventListener("DOMContentLoaded", function () {
  // load
  browser.storage.local
    .get({
      port: "8080",
      homepage: "",
    })
    .then((result) => {
      document.getElementById("tbx_port").value = result.port;
      document.getElementById("tbx_homepage").value = result.homepage;
    });

  // save
  document.getElementById("btn_save").addEventListener("click", function () {
    PORT = document.getElementById("tbx_port").value;
    const homepage = document.getElementById("tbx_homepage").value;
    browser.storage.local.set({
      port: PORT,
      homepage: homepage,
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
  sleep(1000);
  try {
    const response = await fetch(`http://localhost:${PORT}/state`);
    document.getElementById("lbl_info").innerText = "Connection status: OK";
  } catch (error) {
    document.getElementById("lbl_info").innerText = "Connection status: ERROR";
  }
}
