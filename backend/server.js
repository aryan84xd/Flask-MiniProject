// backend/server.js
const express = require('express');
const mongoose = require('mongoose');
const multer = require('multer');
const cors = require('cors');
const path = require('path');

const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());
app.use('/uploads', express.static(path.join(__dirname, 'uploads')));

mongoose.connect('mongodb+srv://aryanhule84:pass123@cluster0.osgouxt.mongodb.net/', { useNewUrlParser: true, useUnifiedTopology: true });

const dogSchema = new mongoose.Schema({
  name: String,
  breed: String,
  age: Number,
  image: String,
});

const Dog = mongoose.model('Dog', dogSchema);

const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    cb(null, Date.now() + '-' + file.originalname);
  },
});

const upload = multer({ storage: storage });

app.get('/api/dogs', async (req, res) => {
  const dogs = await Dog.find();
  res.json(dogs);
});

app.post('/api/dogs', upload.single('image'), async (req, res) => {
  const { name, breed, age } = req.body;
  const image = req.file ? req.file.filename : null;

  const newDog = new Dog({ name, breed, age, image });
  await newDog.save();

  res.json(newDog);
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
