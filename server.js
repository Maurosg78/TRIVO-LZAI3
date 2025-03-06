require('dotenv').config();
const express = require('express');
const axios = require('axios');
const app = express();
const port = 3000;

const USDA_API_KEY = process.env.USDA_API_KEY;
const USDA_URL = 'https://api.nal.usda.gov/fdc/v1/foods/search';

// Middleware
app.use(express.json());

// Ruta para consultar la API de USDA
app.get('/get-food-data', async (req, res) => {
    try {
        const foodQuery = req.query.query || 'pizza'; // Puedes cambiar esto o tomarlo como parámetro
        const response = await axios.get(USDA_URL, {
            params: {
                query: foodQuery,
                api_key: USDA_API_KEY,
            },
        });
        res.json(response.data);
    } catch (error) {
        console.error('Error fetching data from USDA:', error);
        res.status(500).json({ error: 'Error fetching data' });
    }
});

// Iniciar el servidor
app.listen(port, () => {
    console.log(`Server running on http://localhost:${port}`);
});
