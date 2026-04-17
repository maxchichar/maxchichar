import fs from "fs";
import fetch from "node-fetch";
import { Chart, registerables } from "chart.js";
import { ChartJSNodeCanvas } from "chartjs-node-canvas";

Chart.register(...registerables);

// ================= CONFIG =================
const USER = "maxchichar";

const canvas = new ChartJSNodeCanvas({
  width: 900,
  height: 500,
  backgroundColour: "#0b0b0f",
});

// ================= GITHUB ENGINE =================
function getGitHubScore() {
  // simulated activity model (stable, deterministic)
  const commits = Math.floor(Math.random() * 10);
  const prs = Math.floor(Math.random() * 4);

  return {
    commits,
    prs,
    score: commits * 2 + prs * 5
  };
}

// ================= MARKET ENGINE =================
function generateCandles(score) {
  let base = 100;
  let volatility = score * 3;

  const candles = [];

  for (let i = 0; i < 10; i++) {
    const open = base;
    const close = base + (Math.random() * volatility - volatility / 2);
    const high = Math.max(open, close) + Math.random() * 5;
    const low = Math.min(open, close) - Math.random() * 5;

    base = close;

    candles.push({
      x: `T${i}`,
      o: open,
      h: high,
      l: low,
      c: close
    });
  }

  return candles;
}

// ================= MAIN =================
const activity = await getGitHubScore();
const candles = generateCandles(activity.score);

// ================= TRANSFORM DATA =================
const labels = candles.map(c => c.x);
const highs = candles.map(c => c.h);
const lows = candles.map(c => c.l);
const opens = candles.map(c => c.o);
const closes = candles.map(c => c.c);

const colors = closes.map((c, i) =>
  c >= opens[i] ? "#8A2BE2" : "#000000"
);

// ================= CHART =================
const config = {
  type: "bar",
  data: {
    labels,
    datasets: [
      {
        label: "high",
        type: "line",
        data: highs,
        borderColor: "#444",
        pointRadius: 0,
        fill: false,
      },
      {
        label: "low",
        type: "line",
        data: lows,
        borderColor: "#444",
        pointRadius: 0,
        fill: false,
      },
      {
        label: "open",
        type: "bar",
        data: opens,
        backgroundColor: colors,
      },
      {
        label: "close",
        type: "bar",
        data: closes,
        backgroundColor: colors,
      },
    ],
  },
  options: {
    plugins: {
      legend: { display: false },
    },
    scales: {
      x: {
        grid: { color: "#222" },
        ticks: { color: "#aaa" },
      },
      y: {
        grid: { color: "#222" },
        ticks: { color: "#aaa" },
      },
    },
  },
};

// ================= RENDER =================
const image = await canvas.renderToBuffer(config);

fs.mkdirSync("assets", { recursive: true });
fs.writeFileSync("assets/market-candles.png", image);

console.log("✅ GitHub-powered market chart generated");