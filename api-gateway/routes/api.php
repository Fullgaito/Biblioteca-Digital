<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\UserController;
use App\Http\Controllers\GatewayController;

// ── PÚBLICAS ─────────────────────────────────────────────
Route::post('/register',        [UserController::class, 'register']);
Route::post('/login',           [UserController::class, 'login']);
Route::post('/forgot-password', [UserController::class, 'recuperarPassword']);

// ── PROTEGIDAS ────────────────────────────────────────────
Route::middleware('auth:sanctum')->group(function () {

    // Usuarios
    Route::post('/logout', [UserController::class, 'logout']);
    Route::get('/me',      [UserController::class, 'me']);

    // Libros
    Route::get('/books',           [GatewayController::class, 'getBooks']);
    Route::get('/books/{id}',      [GatewayController::class, 'getBook']);
    Route::post('/books',          [GatewayController::class, 'createBook']);
    Route::put('/books/{id}',      [GatewayController::class, 'updateBook']);
    Route::delete('/books/{id}',   [GatewayController::class, 'deleteBook']);

    // Sales(ventas)
    Route::get('/sales',              [GatewayController::class, 'getSales']);
    Route::get('/sales/{id}',         [GatewayController::class, 'getSale']);
    Route::get('/sales/user/{userId}', [GatewayController::class, 'getSalesByUser']);
    Route::post('/sales',              [GatewayController::class, 'createSale']);

    // Préstamos
    Route::get('/loans',                    [GatewayController::class, 'getLoans']);
    Route::get('/loans/{id}',               [GatewayController::class, 'getLoan']);
    Route::get('/loans/user/{userId}',      [GatewayController::class, 'getLoansByUser']);
    Route::post('/loans',                   [GatewayController::class, 'createLoan']);
    Route::put('/loans/{id}/return',        [GatewayController::class, 'returnLoan']);
    Route::get('/loans/activos',            [GatewayController::class, 'activos']);

    // Multas
    Route::get('/fines',                    [GatewayController::class, 'getFines']);
    Route::get('/fines/{id}',               [GatewayController::class, 'getFine']);
    Route::get('/fines/user/{userId}',      [GatewayController::class, 'getFinesByUser']);
    Route::put('/fines/{id}/pay',           [GatewayController::class, 'payFine']);
    Route::post('/fines',                   [GatewayController::class, 'createFine']);

    // Reportes
    Route::get('/reports/most-sold-books', [GatewayController::class, 'getMostSoldBooks']);
    Route::get('/reports/total-sales',     [GatewayController::class, 'getTotalSales']);
    Route::get('/reports/total-revenue',   [GatewayController::class, 'getTotalRevenue']);
    Route::get('/reports/dashboard',       [GatewayController::class, 'getDashboard']);
    Route::get('/reports/most-borrowed-books', [GatewayController::class, 'getMostBorrowedBooks']);
    Route::get('/reports/total-loans',     [GatewayController::class, 'getTotalLoans']);
    Route::get('/reports/top-users-fines', [GatewayController::class, 'getTopUsersFines']);
    Route::get('/reports/total-fines',     [GatewayController::class, 'getTotalFines']);
    Route::get('/reports/total-fines-amount', [GatewayController::class, 'getTotalFinesAmount']);

    // Flujos orquestados
    Route::post('/borrow',           [GatewayController::class, 'borrowBookFlow']);
    Route::put('/return/{loanId}',   [GatewayController::class, 'returnBookFlow']);
});