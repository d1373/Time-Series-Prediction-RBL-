const express = require('express');
const mongoose = require('mongoose');
const app = express();
const port = 5000;

// Replace with your MongoDB Atlas connection string
const mongoURI = 'mongodb+srv://d1373:AlZm1029$$@cluster0.t2h8n.mongodb.net/waste_management';

// Connect to MongoDB Atlas using the connection string
mongoose.connect(mongoURI, {
  useNewUrlParser: true,
  useUnifiedTopology: true,
})
.then(() => console.log('Connected to MongoDB Atlas'))
.catch((error) => console.error('Error connecting to MongoDB:', error));

// Define a schema for waste data
const wasteSchema = new mongoose.Schema({
  dustbin_id: Number,
  location: String,
  filled_capacity: Number,
  date: String,
  time: String,
  entry_ID: Number,
  day_of_week: String
});

// Create a model for the waste data, linked to the existing collection 'waste_data'
const Waste = mongoose.model('Waste', wasteSchema, 'waste_data');

// Middleware to parse JSON bodies
app.use(express.json());
function getDayOfWeek(dateString) {
  const daysOfWeek = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
  const date = new Date(dateString);
  return daysOfWeek[date.getUTCDay()];
}
// Function to get the current date and time in IST
function getCurrentDateTimeIST() {
  const currentDate = new Date();

  // Convert to IST using toLocaleString with 'Asia/Kolkata' timezone
  const options = { timeZone: 'Asia/Kolkata', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
  const istDateTimeString = currentDate.toLocaleString('en-IN', options);

  // Extract date and time from the formatted string
  const [datePart, timePart] = istDateTimeString.split(', ');

  // Format the date as YYYY-MM-DD (reorder date parts)
  const [day, month, year] = datePart.split('/');
  const date = `${year}-${month}-${day}`;

  // Time is already in HH:MM:SS format
  const time = timePart;

  // Get the day of the week in IST
  const day_of_week = getDayOfWeek(date);

  return { date, time, day_of_week };
}
// Endpoint to receive waste data
app.post('/api/waste-data', async (req, res) => {
  try {
    // Get the current date and time
    const { date, time, day_of_week } = getCurrentDateTimeIST();
    // Add date and time to the request body
    const newWasteData = {
      ...req.body,
      date: date,
      time: time,
      day_of_week: day_of_week,
    };

    // Find the document with the highest entry_id in the collection
    const highestEntry = await Waste.findOne().sort({ entry_ID: -1 });
    const nextEntryId = highestEntry ? highestEntry.entry_ID + 1 : 1;

    // Add the new incremented entry_id to the data
    newWasteData.entry_ID = nextEntryId;

    // Create a new document using the updated data
    const wasteEntry = new Waste(newWasteData);

    // Save the new document to the MongoDB collection
    await wasteEntry.save();

    console.log('New waste data saved:', newWasteData);
    res.status(201).send('Data received and saved successfully');
  } catch (error) {
    console.error('Error saving waste data:', error);
    res.status(500).send('Error saving waste data');
  }
});

// Start the server and listen on the specified port
app.listen(port, '0.0.0.0', () => {
  console.log(`Server is running on http://0.0.0.0:${port}`);
});
