const express = require('express') // Rutas para manejar los préstamos
const router = express.Router()
const Loan = require('../models/Loan') // Modelo de préstamo

const authInternal = function (req, res, next) {
    const apiKey = req.headers['x-internal-api-key'];
    const internalKey = process.env.INTERNAL_API_KEY;

    if (!apiKey || apiKey !== internalKey) {
        return res.status(401).json({ error: 'Unauthorized' });
    }

    next();
};

// ── GET /loans/activos ───────────────────────────────────────
router.get('/activos', authInternal, async (req, res) => { // Obtener préstamos activos
    try {
        const loans = await Loan.find({ status: 'active' })
        return res.status(200).json(loans)
    } catch (error) {
        return res.status(500).json({ error: error.message })
    }
})

// ── GET /loans/user/:user_id ───────────────────────────
router.get('/user/:user_id', authInternal, async (req, res) => { // Obtener préstamos por usuario
    try {
        const loans = await Loan.find({ user_id: req.params.user_id })

        if (loans.length === 0) {
            return res.status(404).json({ error: 'No loans found for this user' })
        }

        return res.status(200).json(loans)

    } catch (error) {
        return res.status(500).json({ error: error.message })
    }
})
// ── POST /loans ───────────────────────────────────────────────
router.post('/', authInternal, async (req, res) => { // Registrar un nuevo préstamo
    let stockDecremented = false;
    let book_id;
    try {
        const { user_id, book_id } = req.body

        if (!user_id || !book_id) {
            return res.status(400).json({ error: 'Missing fields' })
        }
        const existingLoan = await Loan.findOne({
            user_id,
            book_id,
            status: 'active'
        });

        if (existingLoan) {
            return res.status(400).json({ error: 'User already has this book' });
        }
        
        //Llamar a flask
        const response = await fetch(`${process.env.FLASK_URL}/books/${book_id}`, {
            headers: {
                'Content-Type': 'application/json',
                'X-Internal-API-Key': process.env.INTERNAL_API_KEY
            },
            timeout: 5000 // 5 segundos de timeout
        });

        if (!response.ok) {
            return res.status(404).json({ error: 'Book not found' });
        }

        const book = await response.json();

        if (!book.quantity  || book.quantity <= 0) {
            return res.status(400).json({ error: 'Not Stock available' })
        }

        // 1. descontar stock
        const decrementResponse = await fetch(`${process.env.FLASK_URL}/books/${book_id}/decrement`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-Internal-API-Key': process.env.INTERNAL_API_KEY
            },
            body: JSON.stringify({ quantity: 1 })
        });

        if (!decrementResponse.ok) {
            const errorData = await decrementResponse.json();
            return res.status(decrementResponse.status).json(errorData);
        }
        stockDecremented = true;
        

        const newLoan = new Loan({ user_id, book_id })
        await newLoan.save()

        return res.status(201).json({
            message: 'Loan created successfully',
            id: newLoan._id
        })

    } catch (error) {
        // rollback (devolver stock)
        await fetch(`${process.env.FLASK_URL}/books/${book_id}/increment`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-Internal-API-Key': process.env.INTERNAL_API_KEY
            }
        });
        return res.status(500).json({ error: error.message })
    }
})

// ── GET /loans ───────────────────────────────────────────────
router.get('/',authInternal, async (req, res) => { // Obtener todos los préstamos
    try {
        const loans = await Loan.find()
        return res.status(200).json(loans)
    } catch (error) {
        return res.status(500).json({ error: error.message })
    }
})

// ── PUT /loans/:id/return ────────────────────────────────────
router.put('/:id/return', authInternal, async (req, res) => { // Devolver un libro
    try {
        const loan = await Loan.findById(req.params.id);

        if (!loan) {
            return res.status(404).json({ error: 'Loan not found' })
        }

        if (loan.status === 'returned') {
            return res.status(400).json({ error: 'Loan already returned' });
        }
        // devolver stock
        const incrementResponse = await fetch(`${process.env.FLASK_URL}/books/${loan.book_id}/increment`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-Internal-API-Key': process.env.INTERNAL_API_KEY
            }
        });

        if (!incrementResponse.ok) {
            return res.status(500).json({ error: 'Error updating stock' });
        }

        //calcular retraso
        const daysLate=calculateDaysLate(loan.created_at);

        function calculateDaysLate(createdAt) {
            const loanDate = new Date(createdAt);
            const now = new Date();

            const diffDays = Math.floor((now - loanDate) / (1000 * 60 * 60 * 24));

            const limitDays = 7;

            return diffDays > limitDays ? diffDays - limitDays : 0;
        }

        //crear multa si aplica

        if(daysLate>0){
            try {
                await fetch(`${process.env.FINES_URL}/fines`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Internal-API-Key': process.env.INTERNAL_API_KEY
                    },
                    body: JSON.stringify({
                        user_id: loan.user_id,
                        loan_id: loan._id,
                        days_late: daysLate
                    })
                });
            } catch (error) {
                console.error('Error creating fine:', error);
            }
        }

        //cerrar préstamo
        loan.status = 'returned';
        loan.return_date = new Date();
        await loan.save();

        return res.status(200).json({
            message: 'Book returned successfully',
            loan,
            fine_created: daysLate > 0
        })
        

    } catch (error) {
        return res.status(500).json({ error: error.message })
    }
})

// ── GET /loans/:id ───────────────────────────
router.get('/:id', authInternal, async (req, res) => { // Obtener préstamos por id
    try {
        const loans = await Loan.findById(req.params.id)

        if (!loans) {
            return res.status(404).json({ error: 'No loans found for this user' })
        }

        return res.status(200).json(loans)

    } catch (error) {
        return res.status(500).json({ error: error.message })
    }
})


module.exports = router