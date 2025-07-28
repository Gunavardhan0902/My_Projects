const express = require('express');
const app = express();
const PORT = process.env.PORT || 5000;

app.use(express.json());

app.get('/', (req, res) => {
  res.send('API Running');
});
const User = require('./models/User');
const bcrypt = require('bcryptjs');

app.post('/api/register', async (req, res) => {
  try {
    const { username, email, password } = {
      username: 'admin',
      email: 'admin@example.com',
      password: 'password123'
    };
    
    const hashedPassword = await bcrypt.hash(password, 10);
    const user = new User({ username, email, password: hashedPassword });
    await user.save();
    
    res.status(201).send('User created');
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
});

app.listen(PORT, () => {
  console.log(`Server started on port ${PORT}`);
});