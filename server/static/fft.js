/* global LEDS_WIDTH, LEDS_HEIGHT */

const constraints = { audio: true };

const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
console.log(audioCtx.sampleRate);
const analyser = audioCtx.createAnalyser();
const gainNode = audioCtx.createGain();
gainNode.gain = 1;

// https://stackoverflow.com/a/17243070/248948
/* accepts parameters
 * h  Object = {h:x, s:y, v:z}
 * OR
 * h, s, v
 */
function HSVtoRGB(h, s, v) {
  var r, g, b, i, f, p, q, t;
  if (arguments.length === 1) {
    (s = h.s), (v = h.v), (h = h.h);
  }
  i = Math.floor(h * 6);
  f = h * 6 - i;
  p = v * (1 - s);
  q = v * (1 - f * s);
  t = v * (1 - (1 - f) * s);
  switch (i % 6) {
    case 0:
      (r = v), (g = t), (b = p);
      break;
    case 1:
      (r = q), (g = v), (b = p);
      break;
    case 2:
      (r = p), (g = v), (b = t);
      break;
    case 3:
      (r = p), (g = q), (b = v);
      break;
    case 4:
      (r = t), (g = p), (b = v);
      break;
    case 5:
      (r = v), (g = p), (b = q);
      break;
  }
  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255)
  };
}

function visualize(ws) {
  analyser.fftSize = 64;
  const freqStep = audioCtx.sampleRate / analyser.fftSize;
  console.log(freqStep);
  analyser.minDecibels = -90;
  analyser.maxDecibels = -30;
  const bufferLengthAlt = 15; //analyser.frequencyBinCount / 2;
  const dataArrayAlt = new Uint8Array(bufferLengthAlt);

  const canvas = document.querySelector('.visualizer');
  const canvasCtx = canvas.getContext('2d');

  const WIDTH = canvas.width;
  const HEIGHT = canvas.height;
  const blockHeight = parseInt((HEIGHT - (LEDS_HEIGHT + 1)) / LEDS_HEIGHT);

  canvasCtx.clearRect(0, 0, WIDTH, HEIGHT);

  let prevFrame = newEmptyFrame();

  const drawAlt = async function() {
    requestAnimationFrame(drawAlt);

    analyser.getByteFrequencyData(dataArrayAlt);

    canvasCtx.fillStyle = 'rgb(0, 0, 0)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    const barWidth = parseInt((WIDTH - bufferLengthAlt - 1) / bufferLengthAlt);
    let x = 1;
    let frame = newEmptyFrame();

    for (let i = 0; i < LEDS_WIDTH; i++) {
      let amp = dataArrayAlt[i] / 255.0;
      let barHeight = amp * HEIGHT;

      let strength = parseInt((LEDS_HEIGHT-1) * amp);
      for (let y = 0; y <= strength; y++) {
        const h = 360 * (y / 15.0);
        const s = 100.0 * (1.0 - (i + 1) / 60.0);
        const v = 100.0 * (0.5 + (i + 1) / 30.0);
        canvasCtx.fillStyle = `hsl(${h}, ${s}%, ${v}%)`;
        // canvasCtx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);
        canvasCtx.fillRect(x, HEIGHT - y - y * blockHeight, barWidth, blockHeight);
        const offset = (y * LEDS_WIDTH) + i;
        if (offset > LEDS_WIDTH * LEDS_HEIGHT) {
          console.error(i, y);
        }
        frame[y * LEDS_WIDTH + i] = HSVtoRGB(h / 360.0, s / 100.0, v / 100.0);
      }

      x += barWidth + 1;
    }

    const partial = diffFrames(prevFrame, frame);
    prevFrame = frame;
    await ws.send(makePartialFrame(partial));
  };

  drawAlt();
}

async function init() {
  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  const source = audioCtx.createMediaStreamSource(stream);
  source.connect(gainNode);
  gainNode.connect(analyser);
  // analyser.connect(audioCtx.destination);

  const ws = await openWebsocket();
  ws.onmessage = event => {
    console.log('Received message:', event.data);
  };
  ws.send('hello there');

  visualize(ws);
}

init();
