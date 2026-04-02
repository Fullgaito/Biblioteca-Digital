const express = require('express');
const router = express.Router();
const db = require('../firebase');

const authInternal = (req, res, next) => {
    const apiKey = req.headers['x-internal-api-key'];
    if (apiKey !== process.env.INTERNAL_API_KEY) {
        return res.status(401).json({ error: 'Unauthorized' });
    }
    next();
};

// ── POST /sales ─────────────────────────────
router.post('/', authInternal, async (req, res) => {
    try {
        const { user_id, book_id, quantity } = req.body;

        if (!user_id || !book_id || !quantity) {
            return res.status(400).json({ error: 'Missing fields' });
        }

        //Obtener libro desde Flask
        const bookResponse = await fetch(`${process.env.FLASK_URL}/books/${book_id}`, {
            headers: {
                'X-Internal-API-Key': process.env.INTERNAL_API_KEY
            }
        });

        if (!bookResponse.ok) {
            return res.status(404).json({ error: 'Book not found' });
        }

        const book = await bookResponse.json();

        if (book.quantity < quantity) {
            return res.status(400).json({ error: 'Not enough stock' });
        }

        const decrementResponse = await fetch(
            `${process.env.FLASK_URL}/books/${book_id}/decrement`,
            {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Internal-API-Key': process.env.INTERNAL_API_KEY
                },
                body: JSON.stringify({ quantity })
            }
        );

        if (!decrementResponse.ok) {
            return res.status(500).json({ error: 'Error updating stock' });
        }

        const saleRef = db.ref('sales').push();

        const total_price = book.unit_price * quantity;

        const saleData = {
            id: saleRef.key,
            user_id,
            book_id,
            quantity,
            total_price,
            created_at: new Date().toISOString()
        };

        await saleRef.set(saleData);

        return res.status(201).json({
            message: 'Sale completed',
            id: saleRef.key,
            total_price: total_price
        });

    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
});

// ── GET /sales ─────────────────────────────
router.get('/', authInternal, async (req, res) => {
    try {
        const salesSnapshot = await db.ref('sales').once('value');
        const sales = salesSnapshot.val() || {};
        const salesList = Object.values(sales);

        return res.json({ data: salesList });
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
});

// ── GET /sales/:id ─────────────────────────
router.get('/:id', authInternal, async (req, res) => {
    try {
        const saleId = req.params.id;
        const saleSnapshot = await db.ref(`sales/${saleId}`).once('value');

        if (!saleSnapshot.exists()) {
            return res.status(404).json({ error: 'Sale not found' });
        }

        return res.json({ data: saleSnapshot.val() });
    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
});

// ── GET /sales/user/:user_id ────────────────
router.get('/user/:user_id', authInternal, async (req, res) => { // Obtener ventas por usuario
    try {
        const userId = Number(req.params.user_id); // Convertir a número para coincidir con Firebase
        const salesSnapshot = await db.ref('sales').orderByChild('user_id').equalTo(userId).once('value');
        const sales = salesSnapshot.val() || {};
        const salesList = Object.values(sales);

        if (salesList.length === 0) {
            return res.status(404).json({ error: 'No sales found for this user' });
        }

        return res.status(200).json(salesList);

    } catch (error) {
        return res.status(500).json({ error: error.message });
    }
});

module.exports = router;