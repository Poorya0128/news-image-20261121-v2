// make.fun news-image-20261121 entry (Node 22+, standard library only).
// Same behaviour as main.py: validates the pre-rendered entry.png and copies it
// to /output/entry.png (or $MAKEFUN_OUTPUT_DIR). No network, clock or randomness.
const fs = require("fs");
const path = require("path");
const crypto = require("crypto");

const src = path.join(__dirname, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const data = fs.readFileSync(src);
const sig = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!data.subarray(0, 8).equals(sig) || data.toString("latin1", 12, 16) !== "IHDR") {
  throw new Error("entry.png is not a valid PNG");
}
const width = data.readUInt32BE(16);
const height = data.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  throw new Error(`entry.png is ${width}x${height}, expected 1024x1024`);
}
fs.mkdirSync(outDir, { recursive: true });
const dst = path.join(outDir, "entry.png");
fs.writeFileSync(dst, data);
const sha = crypto.createHash("sha256").update(data).digest("hex");
console.log(`wrote ${dst} ${width}x${height} ${data.length} bytes sha256=${sha}`);
