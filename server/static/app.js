async function doPost(url) {
  try {
    const resp = await window.fetch(url, {method: 'POST'});
    alert(await resp.text());
  } catch (e) {
    alert(`Error: ${e}`);
  }
}

async function runScreensaverProgram(program) {
  await doPost(`/screensaver/run/${program}`);
}

async function stopScreensaver() {
  await doPost('/screensaver/stop');
}

async function resetDisplay() {
  await doPost('/display/reset');
}

async function shutdown() {
  if (window.confirm('Are you sure you want to Shutdown?')) {
    await doPost('/shutdown');
  }
}
