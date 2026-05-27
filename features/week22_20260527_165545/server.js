const express = require('express');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;
const publicDir = path.join(__dirname, 'public');

app.use(express.json({ limit: '1mb' }));
app.use(express.static(publicDir));

function parseIndent(indent) {
  const value = Number(indent);
  if (!Number.isInteger(value)) {
    return 2;
  }
  return Math.min(Math.max(value, 0), 8);
}

function summarizeJson(parsed) {
  return {
    keys: typeof parsed === 'object' && parsed !== null ? Object.keys(parsed).length : 0,
    type: Array.isArray(parsed) ? 'array' : typeof parsed
  };
}

function formatPayload(input, indent) {
  if (typeof input !== 'string' || !input.trim()) {
    const error = new Error('Missing input parameter.');
    error.statusCode = 400;
    throw error;
  }

  const parsed = JSON.parse(input);
  const space = parseIndent(indent);

  return {
    success: true,
    formatted: JSON.stringify(parsed, null, space),
    minified: JSON.stringify(parsed),
    ...summarizeJson(parsed)
  };
}

app.get('/api/format-json', (req, res) => {
  try {
    return res.json(formatPayload(req.query.input, req.query.indent));
  } catch (error) {
    return res.status(error.statusCode || 400).json({
      success: false,
      error: error.message
    });
  }
});

app.post('/api/format-json', (req, res) => {
  try {
    const { input, indent } = req.body || {};
    return res.json(formatPayload(input, indent));
  } catch (error) {
    return res.status(error.statusCode || 400).json({
      success: false,
      error: error.message
    });
  }
});

app.listen(port, () => {
  console.log(`Week 22 JSON formatter running at http://localhost:${port}`);
});
