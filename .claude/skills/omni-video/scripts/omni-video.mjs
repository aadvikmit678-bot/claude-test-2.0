#!/usr/bin/env node
// Generate a video clip with Gemini Omni Flash through the Gemini API (Interactions API).
// No dependencies: Node 22+ fetch. Never prints the API key.
//
//   node omni-video.mjs --prompt "..." --out assets/generated/shot.mp4 [options]
//   node omni-video.mjs --prompt "..." --duration 6 --resolution 720p --estimate   # cost only, no call
//
// Key: $GEMINI_API_KEY, else the file named by $GEMINI_API_KEY_FILE, else a placeholder that the
// cloud session's network secret (header x-goog-api-key on generativelanguage.googleapis.com) replaces.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { basename, dirname, extname, join, resolve } from "node:path";
import { parseArgs } from "node:util";

const API = "https://generativelanguage.googleapis.com/v1beta";
// USD per second of output, Gemini Omni 1.2 Flash, from the Gemini API pricing page (Nov 2026).
const RATE_PER_SECOND = { "360p": 0.023, "720p": 0.07, "1080p": 0.104, "4k": 0.209 };
// USD per token, same page: input (text/image/video), output video, output text.
const TOKEN_PRICE = { input: 1.5e-6, video: 12e-6, text: 9e-6 };
const MIME = { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp" };

const HELP = `Usage: omni-video.mjs --prompt <text> --out <file.mp4> [options]

  -p, --prompt <text>       What happens in the shot (required)
  -o, --out <file.mp4>      Where to save the clip (required unless --estimate)
      --duration <s>        3-15 whole seconds (3-10 with --last). Default 8
      --aspect <ratio>      16:9 (default) or 9:16
      --resolution <r>      360p, 720p (default), 1080p, 4k  (1080p and 4k are upscaled)
      --first <image>       Start the shot on this frame (png/jpg/webp)
      --last <image>        End the shot on this frame (needs --first)
      --ref <image>         Subject reference image; repeat up to 6 times
      --task <task>         Force the mode: text_to_video, image_to_video, reference_to_video
      --model <id>          Default gemini-omni-1.2-flash
      --max-cost <usd>      Refuse if the estimate is above this. Default 2
      --estimate            Print the estimated cost and exit without calling the API
      --timeout <s>         Give up waiting after this many seconds. Default 900`;

const { values: a } = parseArgs({
  options: {
    prompt: { type: "string", short: "p" },
    out: { type: "string", short: "o" },
    duration: { type: "string", default: "8" },
    aspect: { type: "string", default: "16:9" },
    resolution: { type: "string", default: "720p" },
    first: { type: "string" },
    last: { type: "string" },
    ref: { type: "string", multiple: true, default: [] },
    task: { type: "string" },
    model: { type: "string", default: "gemini-omni-1.2-flash" },
    "max-cost": { type: "string", default: "2" },
    estimate: { type: "boolean", default: false },
    timeout: { type: "string", default: "900" },
    help: { type: "boolean", short: "h", default: false },
  },
});

const fail = (msg) => {
  console.error(`omni-video: ${msg}`);
  process.exit(1);
};

if (a.help) {
  console.log(HELP);
  process.exit(0);
}
if (!a.prompt) fail("--prompt is required.\n\n" + HELP);
const duration = Number(a.duration);
const maxDuration = a.last ? 10 : 15;
if (!Number.isInteger(duration) || duration < 3 || duration > maxDuration) fail(`--duration must be a whole number from 3 to ${maxDuration}.`);
if (!["16:9", "9:16"].includes(a.aspect)) fail("--aspect must be 16:9 or 9:16.");
if (!(a.resolution in RATE_PER_SECOND)) fail(`--resolution must be one of ${Object.keys(RATE_PER_SECOND).join(", ")}.`);
if (a.last && !a.first) fail("--last needs --first.");
if (a.ref.length > 6) fail("At most 6 --ref images.");
if (a.task && !["text_to_video", "image_to_video", "reference_to_video"].includes(a.task)) fail("Unknown --task.");

const estimate = duration * RATE_PER_SECOND[a.resolution];
const maxCost = Number(a["max-cost"]);
console.log(`Estimate: ${duration}s at ${a.resolution} ≈ $${estimate.toFixed(3)} (${a.model})`);
if (a.estimate) process.exit(0);
if (!a.out) fail("--out is required.");
if (estimate > maxCost) fail(`Estimate $${estimate.toFixed(2)} is above --max-cost $${maxCost.toFixed(2)}. Raise --max-cost to proceed.`);

function apiKey() {
  if (process.env.GEMINI_API_KEY) return process.env.GEMINI_API_KEY.trim();
  if (process.env.GEMINI_API_KEY_FILE) return readFileSync(process.env.GEMINI_API_KEY_FILE, "utf8").trim();
  return "injected-by-network-secret";
}
const headers = { "x-goog-api-key": apiKey(), "content-type": "application/json" };

function imagePart(path) {
  const mime = MIME[extname(path).toLowerCase()];
  if (!mime) fail(`${path}: use a .png, .jpg or .webp image.`);
  return { type: "image", data: readFileSync(path).toString("base64"), mime_type: mime };
}

const input = [];
if (a.first) input.push(imagePart(a.first));
if (a.last) input.push(imagePart(a.last));
for (const r of a.ref) input.push(imagePart(r));
input.push({ type: "text", text: a.prompt });

const body = {
  model: a.model,
  input: input.length === 1 ? a.prompt : input,
  response_format: { type: "video", aspect_ratio: a.aspect, resolution: a.resolution, duration: `${duration}s`, delivery: "uri" },
  background: true,
  store: true,
};
if (a.task) body.generation_config = { video_config: { task: a.task } };

async function api(method, path, payload) {
  const res = await fetch(`${API}/${path}`, { method, headers, body: payload ? JSON.stringify(payload) : undefined });
  const text = await res.text();
  let json;
  try {
    json = JSON.parse(text);
  } catch {
    json = { raw: text.slice(0, 500) };
  }
  if (!res.ok) fail(`${method} ${path} → HTTP ${res.status}: ${json.error?.message ?? text.slice(0, 500)}`);
  return json;
}

const started = Date.now();
let it = await api("POST", "interactions", body);
console.log(`Interaction ${it.id ?? "(no id)"}: ${it.status}`);
const deadline = started + Number(a.timeout) * 1000;
while (it.status === "in_progress") {
  if (Date.now() > deadline) fail(`Still running after ${a.timeout}s. Interaction id: ${it.id}`);
  await new Promise((r) => setTimeout(r, 10_000));
  it = await api("GET", `interactions/${it.id}`);
  process.stdout.write(`  ${Math.round((Date.now() - started) / 1000)}s ${it.status}\n`);
}
if (it.status !== "completed") {
  const errs = [it.error, ...(it.errors ?? [])].filter(Boolean).map((e) => `${e.code ?? e.status ?? "error"}: ${e.message ?? JSON.stringify(e)}`);
  const hint = errs.some((e) => /RESOURCE_EXHAUSTED/.test(e))
    ? "\nRESOURCE_EXHAUSTED: the key's project has no video quota left. Video has no free tier: turn on billing for the project in AI Studio, or wait if a rate limit was hit."
    : "";
  fail(`Interaction ${it.id} ended as "${it.status}": ${errs.join("; ") || JSON.stringify(it).slice(0, 800)}${hint}`);
}

const parts = (it.steps ?? []).flatMap((s) => s.content ?? []);
const video = parts.find((p) => p.type === "video");
const notes = parts.filter((p) => p.type === "text").map((p) => p.text).join("\n").trim();
if (!video) fail(`No video in the response.${notes ? ` Model said: ${notes.slice(0, 600)}` : ""}`);

const out = resolve(a.out);
mkdirSync(dirname(out), { recursive: true });
if (video.data) {
  writeFileSync(out, Buffer.from(video.data, "base64"));
} else if (video.uri) {
  const res = await fetch(video.uri, { headers: { "x-goog-api-key": headers["x-goog-api-key"] }, redirect: "follow" });
  if (!res.ok) fail(`Download failed: HTTP ${res.status}`);
  writeFileSync(out, Buffer.from(await res.arrayBuffer()));
} else {
  fail("Video part has neither data nor uri.");
}

// Cost from the reported usage when present; the per-second estimate otherwise.
const u = it.usage ?? {};
const byModality = (list) =>
  Object.fromEntries((Array.isArray(list) ? list : []).map((m) => [String(m.modality ?? "").toLowerCase(), Number(m.tokens ?? m.token_count ?? 0)]));
const outBy = byModality(u.output_tokens_by_modality);
let cost = null;
if (u.total_input_tokens != null || u.total_output_tokens != null) {
  const videoTokens = outBy.video ?? 0;
  const otherOut = Math.max(0, Number(u.total_output_tokens ?? 0) + Number(u.total_thought_tokens ?? 0) - videoTokens);
  cost = Number(u.total_input_tokens ?? 0) * TOKEN_PRICE.input + videoTokens * TOKEN_PRICE.video + otherOut * TOKEN_PRICE.text;
}

const record = {
  model: a.model,
  interaction_id: it.id,
  prompt: a.prompt,
  duration_s: duration,
  aspect_ratio: a.aspect,
  resolution: a.resolution,
  first_frame: a.first ? basename(a.first) : undefined,
  last_frame: a.last ? basename(a.last) : undefined,
  references: a.ref.map((r) => basename(r)),
  estimate_usd: Number(estimate.toFixed(4)),
  cost_usd: cost == null ? undefined : Number(cost.toFixed(4)),
  usage: it.usage,
  model_notes: notes || undefined,
  seconds_to_generate: Math.round((Date.now() - started) / 1000),
};
const sidecar = join(dirname(out), `${basename(out, extname(out))}.omni.json`);
writeFileSync(sidecar, JSON.stringify(record, null, 2) + "\n");
console.log(`Saved ${out}`);
console.log(`Record ${sidecar}`);
console.log(cost == null ? `Cost: about $${estimate.toFixed(3)} (estimate)` : `Cost: $${cost.toFixed(4)} from reported usage`);
