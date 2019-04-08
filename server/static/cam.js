const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const canvasCtx = canvas.getContext('2d');

// Not adding `{ audio: true }` since we only want video now
navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
  //video.src = window.URL.createObjectURL(stream);
  video.srcObject = stream;
  video.play();

  window.setInterval(function () {
    canvasCtx.drawImage(video, 0, 0, 640, 480, 0, 0, 15, 15);
  }, 100);
});

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
  const blockHeight = parseInt((HEIGHT - 16) / 15);

  canvasCtx.clearRect(0, 0, WIDTH, HEIGHT);

  const drawAlt = function() {
    requestAnimationFrame(drawAlt);

    analyser.getByteFrequencyData(dataArrayAlt);

    canvasCtx.fillStyle = 'rgb(0, 0, 0)';
    canvasCtx.fillRect(0, 0, WIDTH, HEIGHT);

    const barWidth = parseInt((WIDTH - bufferLengthAlt - 1) / bufferLengthAlt);
    let x = 1;

    const len = 15*15*3;
    const frame = new Uint8Array(new ArrayBuffer(4 + len));
    frame[0] = 0;
    frame[1] = 0;
    frame[2] = (len >> 8) & 0xff;
    frame[3] = len & 0xff;
    for (let i = 4; i < len + 4; i++) {
      frame[i] = 0;
    }

    for (let i = 0; i < bufferLengthAlt; i++) {
      let amp = dataArrayAlt[i] / 255.0;
      let barHeight = amp * HEIGHT;

      let strength = parseInt(15.0 * amp);
      for (let y = 0; y <= strength; y++) {
        const h = 360 * (y / 15.0);
        const s = 100.0 * (1.0 - ((i + 1) / 60.0));
        const v = 100.0 * (0.5 + ((i + 1) / 30.0));
        canvasCtx.fillStyle = `hsl(${h}, ${s}%, ${v}%)`;
        // canvasCtx.fillRect(x, HEIGHT - barHeight, barWidth, barHeight);
        canvasCtx.fillRect(x, HEIGHT - y - (y*blockHeight), barWidth, blockHeight);
        const offset = 4 + 3 * (((15 - y) * 15) + i);
        const {r, g, b} = HSVtoRGB(h / 360.0, s / 100.0, v / 100.0);
        frame[offset] = r;
        frame[offset + 1] = g;
        frame[offset + 2] = b;
      }

      x += barWidth + 1;
    }

    ws.send(frame);
  };

  drawAlt();
}

async function openWebsocket() {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(`ws://${location.host}/ws`);
    ws.onopen = () => resolve(ws);
    ws.onerror = (err) => reject(err);
  });
}

async function init() {
  const stream = await navigator.mediaDevices.getUserMedia(constraints);
  const source = audioCtx.createMediaStreamSource(stream);
  source.connect(gainNode);
  gainNode.connect(analyser);
  // analyser.connect(audioCtx.destination);

  const ws = await openWebsocket();
  ws.onmessage = (event) => {
    console.log('Received message:', event.data);
  };
  ws.send('hello there');

  visualize(ws);
}

