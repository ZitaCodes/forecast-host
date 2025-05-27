const express = require("express");
const router = express.Router();
const Pull = require("../models/Pull");

// GET /api/pulls/status?email=user@example.com
router.get("/status", async (req, res) => {
  const email = req.query.email?.toLowerCase();
  if (!email) return res.status(400).json({ error: "Email is required" });

  try {
    let pullData = await Pull.findOne({ email });
    if (!pullData) {
      pullData = await Pull.create({ email });
    }

    res.json({
      email: pullData.email,
      pulls_used: pullData.pulls_used,
      pull_limit: pullData.pull_limit,
      last_reset: pullData.last_reset
    });
  } catch (err) {
    console.error("Error fetching pull status:", err);
    res.status(500).json({ error: "Internal server error" });
  }
});

// POST /api/pulls/increment
router.post("/increment", async (req, res) => {
  const email = req.body.email?.toLowerCase();
  if (!email) return res.status(400).json({ error: "Email is required" });

  try {
    const pullData = await Pull.findOneAndUpdate(
      { email },
      { $inc: { pulls_used: 1 } },
      { new: true, upsert: true }
    );

    res.json({
      success: true,
      pulls_used: pullData.pulls_used,
      pull_limit: pullData.pull_limit
    });
  } catch (err) {
    console.error("Error incrementing pull count:", err);
    res.status(500).json({ error: "Internal server error" });
  }
});

module.exports = router;
