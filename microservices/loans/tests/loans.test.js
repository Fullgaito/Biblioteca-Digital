const request = require('supertest');
const express = require('express');

const loanRoutes = require('../routes/loans');

const Loan = require('../models/loan');

jest.mock('../models/loan');

global.fetch = jest.fn();

beforeEach(() => {
    jest.clearAllMocks();
});

const app = express();

app.use(express.json());

app.use('/loans', loanRoutes);

process.env.INTERNAL_API_KEY = 'testkey';
process.env.FLASK_URL = 'http://fake-flask';
process.env.FINES_URL = 'http://fake-fines';

test('Debe crear un préstamo correctamente', async () => {

    Loan.findOne.mockResolvedValue(null);

    Loan.prototype.save = jest.fn().mockResolvedValue(true);

    global.fetch
        .mockResolvedValueOnce({
            ok: true,
            json: async () => ({
                quantity: 5
            })
        })
        .mockResolvedValueOnce({
            ok: true,
            json: async () => ({})
        });

    const response = await request(app)
        .post('/loans')
        .set('x-internal-api-key', 'testkey')
        .send({
            user_id: '1',
            book_id: '1'
        });

    expect(response.status).toBe(201);

    expect(response.body.message)
        .toBe('Loan created successfully');

    expect(global.fetch).toHaveBeenCalledTimes(2);
});

test('No debe permitir préstamos duplicados', async () => {

    Loan.findOne.mockResolvedValue({
        user_id: '1',
        book_id: '1',
        status: 'active'
    });

    const response = await request(app)
        .post('/loans')
        .set('x-internal-api-key', 'testkey')
        .send({
            user_id: '1',
            book_id: '1'
        });

    expect(response.status).toBe(400);

    expect(response.body.error)
        .toBe('User already has this book');

    expect(global.fetch).not.toHaveBeenCalled();
});

test('Debe retornar libro y crear multa si hay retraso', async () => {

    const mockLoan = {
        _id: 'loan1',
        user_id: '1',
        book_id: '1',
        status: 'active',
        created_at: new Date(Date.now() - 10 * 24 * 60 * 60 * 1000),
        save: jest.fn().mockResolvedValue(true)
    };

    Loan.findById.mockResolvedValue(mockLoan);

    global.fetch
        // incremento stock
        .mockResolvedValueOnce({
            ok: true,
            json: async () => ({})
        })

        // creación multa
        .mockResolvedValueOnce({
            ok: true,
            json: async () => ({})
        });

    const response = await request(app)
        .put('/loans/loan1/return')
        .set('x-internal-api-key', 'testkey');

    expect(response.status).toBe(200);

    expect(response.body.fine_created).toBe(true);

    expect(mockLoan.status).toBe('returned');

    expect(mockLoan.save).toHaveBeenCalled();
});