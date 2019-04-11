const LEDS_WIDTH = 15;
const LEDS_HEIGHT = 15;

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

async function openWebsocket() {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(`ws://${location.host}/ws`);
    ws.onopen = () => resolve(ws);
    ws.onerror = (err) => reject(err);
  });
}

function makeFullFrame(frame) {
  const len = LEDS_WIDTH * LEDS_HEIGHT * 3;
  const msg = new Uint8Array(new ArrayBuffer(4 + len));

  // Header
  msg[0] = 0; // channel
  msg[1] = 0; // command
  msg[2] = (len >> 8) & 0xff;
  msg[3] = len & 0xff;

  for (let [i, {r, g, b}] of frame.entries()) {
    const offset = 4 + i * 3;
    msg[offset + 0] = r;
    msg[offset + 1] = g;
    msg[offset + 2] = b;
  }

  return msg;
}

function makePartialFrame(frame) {
  const len = frame.length * 5;
  const msg = new Uint8Array(new ArrayBuffer(4 + len));

  // Header
  msg[0] = 0; // channel
  msg[1] = 1; // command
  msg[2] = (len >> 8) & 0xff;
  msg[3] = len & 0xff;

  for (let [i, {x, y, r, g, b}] of frame.entries()) {
    const offset = 4 + i * 5;
    msg[offset + 0] = x;
    msg[offset + 1] = y;
    msg[offset + 2] = r;
    msg[offset + 3] = g;
    msg[offset + 4] = b;
  }

  return msg;
}

function diffFrames(oldFrame, newFrame) {
  const partial = [];
  if (newFrame.length != oldFrame.length) {
    console.error(newFrame.length, '!=', oldFrame.length);
    return partial;
  }

  for (let i = 0; i < newFrame.length; i++) {
    const old = oldFrame[i];
    const {r, g, b} = newFrame[i];
    if (old.r !== r || old.g !== g || old.b !== b) {
      const y = parseInt(i / LEDS_WIDTH);
      const x = i % LEDS_WIDTH;
      partial.push({x, y, r, g, b});
    }
  }

  return partial;
}

function newEmptyFrame() {
  return Array(LEDS_WIDTH * LEDS_HEIGHT).fill({ r: 0, g: 0, b: 0 });
}
