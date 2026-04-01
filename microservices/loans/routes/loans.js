const express = require('express') // Rutas para manejar los préstamos
const router = express.Router()
const Loan = require('../models/Loan') // Modelo de préstamo

// ── POST /loans ───────────────────────────────────────────────
router.post('/', async (req, res) => { // Registrar un nuevo préstamo
    try {
        const { usuario_id, libro_id } = req.body

        if (!usuario_id || !libro_id) {
            return res.status(400).json({ error: 'Missing fields' })
        }

        const newLoan = new Loan({ usuario_id, libro_id })
        await newLoan.save()

        return res.status(201).json({
            message: 'Loan created successfully',
            id: newLoan._id
        })

    } catch (error) {
        return res.status(500).json({ error: error.message })
    }
})

// ── GET /loans ───────────────────────────────────────────────
router.get('/', async (req, res) => { // Obtener todos los préstamos
    try {
        const loans = await Loan.find()
        return res.status(200).json(loans)
    } catch (error) {
        return res.status(500).json({ error: error.message })
    }
})

// ── PUT /loans/:id/return ────────────────────────────────────
router.put('/:id/return', async (req, res) => { // Devolver un libro
    try {
        const loan = await Loan.findByIdAndUpdate(
            req.params.id,
            {
                estado: 'devuelto',
                fecha_devolucion: new Date()
            },
            { new: true }
        )

        if (!loan) {
            return res.status(404).json({ error: 'Loan not found' })
        }

        return res.status(200).json({
            message: 'Book returned successfully',
            loan
        })

    } catch (error) {
        return res.status(500).json({ error: error.message })
    }
})

// ── GET /loans/usuario/:usuario_id ───────────────────────────
router.get('/usuario/:usuario_id', async (req, res) => { // Obtener préstamos por usuario
    try {
        const loans = await Loan.find({ usuario_id: req.params.usuario_id })

        if (!loans.length) {
            return res.status(404).json({ error: 'No loans found for this user' })
        }

        return res.status(200).json(loans)

    } catch (error) {
        return res.status(500).json({ error: error.message })
    }
})

// ── GET /loans/activos ───────────────────────────────────────
router.get('/activos', async (req, res) => { // Obtener préstamos activos
    try {
        const loans = await Loan.find({ estado: 'activo' })
        return res.status(200).json(loans)
    } catch (error) {
        return res.status(500).json({ error: error.message })
    }
})

module.exports = router