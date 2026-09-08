// Safari Time - encode the source WAVs to MP3 for the web build.
//
// Pure JavaScript (lamejs), so it runs anywhere Node runs - no ffmpeg needed.
//
//   npm install lamejs@1.2.1
//   node engine/encode_audio.js <wav dir> <out dir> [--lamejs <path>]
//
// Use lamejs's bundled build, e.g. --lamejs node_modules/lamejs/lame.all.js.
// The package's default "src" entry throws "MPEGMode is not defined" under
// Node (a long-standing upstream bug); the bundle does not.
//
// Output names are the source names lowercased: "Lion_Roar.wav" -> "lion_roar.mp3".
// engine/export.py lists whatever lands in web/assets/audio in gamedata.js.

"use strict";
const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);
const inDir = args[0];
const outDir = args[1];
const lameIdx = args.indexOf("--lamejs");
function loadLame(spec) {
  const resolved = require.resolve(spec);
  const mod = require(resolved);
  if (mod && typeof mod.Mp3Encoder === "function") return mod;
  // The bundled build is a plain browser script that declares a top-level
  // `lamejs` instead of exporting it; evaluate it in a function scope and
  // hand the symbol back.
  const src = fs.readFileSync(resolved, "utf8");
  return new Function(src + "\n;return lamejs;")();
}
const lamejs = loadLame(lameIdx >= 0 ? args[lameIdx + 1] : "lamejs/lame.all.js");

if (!inDir || !outDir) {
  console.error("usage: node engine/encode_audio.js <wav dir> <out dir> [--lamejs <path>]");
  process.exit(2);
}

// Music loops get more bits than one-shot effects.
const KBPS = (name) => (/bgm/i.test(name) ? 128 : 96);

function parseWav(buf) {
  if (buf.toString("ascii", 0, 4) !== "RIFF" || buf.toString("ascii", 8, 12) !== "WAVE") {
    throw new Error("not a RIFF/WAVE file");
  }
  let pos = 12;
  let fmt = null;
  let data = null;
  while (pos + 8 <= buf.length) {
    const id = buf.toString("ascii", pos, pos + 4);
    const size = buf.readUInt32LE(pos + 4);
    const body = pos + 8;
    if (id === "fmt ") {
      fmt = {
        format: buf.readUInt16LE(body),
        channels: buf.readUInt16LE(body + 2),
        sampleRate: buf.readUInt32LE(body + 4),
        bits: buf.readUInt16LE(body + 14),
      };
    } else if (id === "data") {
      data = buf.subarray(body, body + size);
    }
    pos = body + size + (size % 2);
  }
  if (!fmt || !data) throw new Error("missing fmt or data chunk");
  if (fmt.format !== 1 || fmt.bits !== 16) throw new Error(`need 16-bit PCM, got format ${fmt.format} / ${fmt.bits}-bit`);
  return { ...fmt, data };
}

function encode(wavPath, mp3Path) {
  const { channels, sampleRate, data } = parseWav(fs.readFileSync(wavPath));
  const frames = data.length / 2 / channels;
  const left = new Int16Array(frames);
  const right = channels === 2 ? new Int16Array(frames) : null;
  for (let i = 0; i < frames; i++) {
    left[i] = data.readInt16LE(i * 2 * channels);
    if (right) right[i] = data.readInt16LE(i * 2 * channels + 2);
  }
  const enc = new lamejs.Mp3Encoder(channels, sampleRate, KBPS(path.basename(wavPath)));
  const parts = [];
  const BLOCK = 1152;
  for (let i = 0; i < frames; i += BLOCK) {
    const l = left.subarray(i, i + BLOCK);
    const r = right ? right.subarray(i, i + BLOCK) : undefined;
    const out = channels === 2 ? enc.encodeBuffer(l, r) : enc.encodeBuffer(l);
    if (out.length) parts.push(Buffer.from(out));
  }
  const tail = enc.flush();
  if (tail.length) parts.push(Buffer.from(tail));
  fs.writeFileSync(mp3Path, Buffer.concat(parts));
  return { seconds: frames / sampleRate, channels, sampleRate };
}

fs.mkdirSync(outDir, { recursive: true });
let total = 0;
for (const file of fs.readdirSync(inDir).filter((f) => f.toLowerCase().endsWith(".wav")).sort()) {
  const name = path.basename(file, path.extname(file)).toLowerCase();
  const out = path.join(outDir, `${name}.mp3`);
  const info = encode(path.join(inDir, file), out);
  const kb = fs.statSync(out).size / 1024;
  total += kb;
  console.log(`${name.padEnd(18)} ${info.seconds.toFixed(2).padStart(6)}s ${info.channels}ch  -> ${kb.toFixed(0).padStart(4)} KB`);
}
console.log(`total ${(total / 1024).toFixed(2)} MB`);
