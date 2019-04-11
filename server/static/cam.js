const video = document.getElementById('video');
const canvas = document.getElementById('canvas');
const canvasCtx = canvas.getContext('2d');

function visualize(video, ws) {
  const params = new URL(window.location.href).searchParams;
  let fps = parseInt(params.get('fps'));
  if (isNaN(fps) || fps < 1 || fps > 60) {
    fps = 10;
  }
  console.log('fps =', fps);

  const drawAlt = function() {
    canvasCtx.drawImage(video, 0, 0, 640, 480, 0, 0, LEDS_WIDTH, LEDS_HEIGHT);
    const image = canvasCtx.getImageData(0, 0, LEDS_WIDTH, LEDS_HEIGHT);
    const frame = [];
    for (let i = 0; i < LEDS_WIDTH * LEDS_HEIGHT; i++) {
      const offset = i * 4; // RGBA
      const [r, g, b] = image.data.slice(offset, offset + 3);
      frame.push({ r, g, b });
    }

    ws.send(makeFullFrame(frame));
    setTimeout(drawAlt, 1000 / fps);
  };

  drawAlt();
}

async function openWebsocket() {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(`ws://${location.host}/ws`);
    ws.onopen = () => resolve(ws);
    ws.onerror = err => reject(err);
  });
}

async function init() {
  // Not adding `{ audio: true }` since we only want video now
  navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
    video.srcObject = stream;
    video.play();
  });

  const ws = await openWebsocket();
  ws.onmessage = event => {
    console.log('Received message:', event.data);
  };
  ws.send('hello there');

  visualize(video, ws);
}

init();
