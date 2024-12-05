const express = require("express");
const bodyParser = require("body-parser");
const { MongoClient } = require("mongodb");
const path = require("path");
const app = express();
const port = 3000;

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, "public")));
// POST endpoint to receive estimated times
app.post("/api/estimated_times", (req, res) => {
  const estimatedTimes = req.body.estimated_times;
  console.log("Received estimated times:", estimatedTimes);
  // Process the received data as needed

  res.status(200).send("Estimated times received successfully.");
});

app.get("/login", (req, res) => {
  console.log("Login page");
});
// MongoDB connection URL
const mongoURL = "mongodb://127.0.0.1:27017";
const dbName = "RBL";
const client = new MongoClient(mongoURL, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

// Serve HTML file
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

// Endpoint to get latest data and fill percentages for all dustbins
app.get("/getLatestData", async (req, res) => {
  try {
    await client.connect();
    const db = client.db(dbName);
    const collection = db.collection("dustbin_entries");

    const fillPercentages = [];

    // Loop through each dustbin ID
    for (let i = 1; i <= 6; i++) {
      // Query MongoDB to find the latest data for the current dustbin ID
      const latestData = await collection
        .find({ Dustbin_ID: i })
        .sort({ Date: -1, Time: -1 })
        .limit(1)
        .toArray();

      // If data is found, calculate fill percentage and add it to the array
      if (latestData.length > 0) {
        const { Total_amount } = latestData[0];
        const fillPercentage = Total_amount;
        fillPercentages.push({ dustbinId: i, fillPercentage });
      }
    }

    res.json(fillPercentages);
  } catch (error) {
    console.error("Error:", error);
    res.status(500).send("Internal Server Error");
  }
});
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
