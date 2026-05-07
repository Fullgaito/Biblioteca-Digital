const request = require('supertest');
const express = require('express');

const salesRoutes = require('../routes/sales');

jest.mock('../firebase', () => ({
    ref: jest.fn()
}));

const db = require('../firebase');

global.fetch = jest.fn();

const app = express();

app.use(express.json());
app.use('/sales', salesRoutes);

process.env.INTERNAL_API_KEY = 'testkey';
process.env.FLASK_URL = 'http://fake-flask';

beforeEach(() => {
    jest.clearAllMocks();
});

test('Debe crear una venta correctamente', async () => {

    global.fetch
        // Obtener libro desde microservicio books
        .mockResolvedValueOnce({
            ok: true,
            json: async () => ({
                quantity: 10,
                unit_price: 60000
            })
        })

        // Decrementar stock
        .mockResolvedValueOnce({
            ok: true,
            json: async () => ({})
        });

    const mockSet = jest.fn().mockResolvedValue(true);

    const mockPush = jest.fn(() => ({
        key: 'sale123',
        set: mockSet
    }));

    db.ref.mockImplementation(() => ({
        push: mockPush
    }));

    const response = await request(app)
        .post('/sales')
        .set('x-internal-api-key', 'testkey')
        .send({
            user_id: 1,
            book_id: 1,
            quantity: 4
        });

    expect(response.status).toBe(201);

    expect(response.body.message)
        .toBe('Sale completed');

    expect(response.body.total_price)
        .toBe(240000);

    expect(mockSet).toHaveBeenCalled();

    expect(mockPush).toHaveBeenCalled();

    expect(global.fetch).toHaveBeenCalledTimes(2);
});

test('No debe permitir ventas sin stock suficiente', async () => {

    global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => ({
            quantity: 1,
            unit_price: 50
        })
    });

    const response = await request(app)
        .post('/sales')
        .set('x-internal-api-key', 'testkey')
        .send({
            user_id: 1,
            book_id: 10,
            quantity: 5
        });

    expect(response.status).toBe(400);

    expect(response.body.error)
        .toBe('Not enough stock');

    expect(db.ref).not.toHaveBeenCalled();

    expect(global.fetch).toHaveBeenCalledTimes(1);
});

test('Debe obtener ventas por usuario', async () => {

    const mockSales = {
        sale1: {
            id: 'sale1',
            user_id: 1,
            book_id: 10,
            quantity: 2
        }
    };

    db.ref.mockReturnValue({
        orderByChild: () => ({
            equalTo: () => ({
                once: jest.fn().mockResolvedValue({
                    val: () => mockSales
                })
            })
        })
    });

    const response = await request(app)
        .get('/sales/user/1')
        .set('x-internal-api-key', 'testkey');

    expect(response.status).toBe(200);

    expect(response.body.length).toBe(1);

    expect(response.body[0].user_id).toBe(1);
});