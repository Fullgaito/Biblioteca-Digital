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
    Route::get('/users/me',      [UserController::class, 'me']);

    // Libros
    Route::get('/books',           [GatewayController::class, 'getBooks']);
    Route::get('/books/{id}',      [GatewayController::class, 'getBook']);
    Route::post('/books',          [GatewayController::class, 'createBook']);
    Route::put('/books/{id}',      [GatewayController::class, 'updateBook']);
    Route::delete('/books/{id}',   [GatewayController::class, 'deleteBook']);

    // Categorías
    Route::get('/categories',          [GatewayController::class, 'getCategories']);
    Route::get('/categories/{id}',     [GatewayController::class, 'getCategory']);
    Route::post('/categories',         [GatewayController::class, 'createCategory']);
    Route::put('/categories/{id}',     [GatewayController::class, 'updateCategory']);
    Route::delete('/categories/{id}',  [GatewayController::class, 'deleteCategory']);

    // Préstamos
    Route::get('/loans',                    [GatewayController::class, 'getLoans']);
    Route::get('/loans/{id}',               [GatewayController::class, 'getLoan']);
    Route::get('/loans/user/{userId}',      [GatewayController::class, 'getLoansByUser']);
    Route::post('/loans',                   [GatewayController::class, 'createLoan']);
    Route::put('/loans/{id}/return',        [GatewayController::class, 'returnLoan']);

    // Multas
    Route::get('/fines',                    [GatewayController::class, 'getFines']);
    Route::get('/fines/{id}',               [GatewayController::class, 'getFine']);
    Route::get('/fines/user/{userId}',      [GatewayController::class, 'getFinesByUser']);
    Route::put('/fines/{id}/pay',           [GatewayController::class, 'payFine']);

    // Reseñas
    Route::get('/reviews',                  [GatewayController::class, 'getReviews']);
    Route::get('/reviews/book/{bookId}',    [GatewayController::class, 'getReviewsByBook']);
    Route::post('/reviews',                 [GatewayController::class, 'createReview']);
    Route::delete('/reviews/{id}',          [GatewayController::class, 'deleteReview']);

    // Flujos orquestados
    Route::post('/borrow',           [GatewayController::class, 'borrowBookFlow']);
    Route::put('/return/{loanId}',   [GatewayController::class, 'returnBookFlow']);
});