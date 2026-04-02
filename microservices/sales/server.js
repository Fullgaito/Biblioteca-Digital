const express = require('express');
require('dotenv').config();

const app = express();
app.use(express.json());

const salesRoutes = require('./routes/sales');
app.use('/sales', salesRoutes);

app.listen(process.env.PORT, () => {
    console.log(`Sales service running on port ${process.env.PORT}`);
});