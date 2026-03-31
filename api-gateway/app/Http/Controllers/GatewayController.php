<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class GatewayController extends Controller
{
    private function headersInternos(Request $request)
    {
        return [
            'X-api-key' => env('INTERNAL_API_KEY'),
            'X-User-Id'     => $request->user()->id,
            'X-User-Email'  => $request->user()->email,
            'Content-Type' => 'application/json',
        ];
    }

    // Libros

    public function getBooks()
    {
        $response = Http::get(config('services.microservices.books') . '/books');
        return response()->json($response->json(), $response->status());
    }

    public function createBook(Request $request)
    {
        $response = Http::post(config('services.microservices.books') . '/books', [
            'title'       => $request->title,
            'author'      => $request->author,
            'description' => $request->description,
        ]);

        return response()->json($response->json(), $response->status());
    }

    // Categorias

    public function getCategories()
    {
        $response = Http::get(config('services.microservices.categories') . '/categories');
        return response()->json($response->json(), $response->status());
    }

    // Prestamos

    public function createLoan(Request $request)
    {
        $response = Http::post(config('services.microservices.loans') . '/loans', [
            'user_id' => $request->user_id,
            'book_id' => $request->book_id,
        ]);

        return response()->json($response->json(), $response->status());
    }

    public function returnLoan($id)
    {
        $response = Http::put(config('services.microservices.loans') . "/loans/{$id}/return");

        return response()->json($response->json(), $response->status());
    }

    // Multas

    public function getFinesByUser($userId)
    {
        $response = Http::get(config('services.microservices.fines') . "/fines/user/{$userId}");

        return response()->json($response->json(), $response->status());
    }

    // ── REVIEWS ───────────────────────────────────────────

    public function createReview(Request $request)
    {
        $response = Http::post(config('services.microservices.reviews') . '/reviews', [
            'user_id' => $request->user_id,
            'book_id' => $request->book_id,
            'rating'  => $request->rating,
            'comment' => $request->comment,
        ]);

        return response()->json($response->json(), $response->status());
    }

    // ── FLUJO ORQUESTADO

    public function borrowBookFlow(Request $request)
    {
        $userId = $request->user()->id;

        // 1. Verificar disponibilidad del libro
        $book = Http::get(config('services.microservices.books') . "/books/{$request->book_id}");

        if (!$book->successful()) {
            return response()->json(['error' => 'Error al consultar el libro'], 502);
        }

        if (!$book->json('available')) {
            return response()->json(['error' => 'Libro no disponible'], 422);
        }

        // 2. Crear préstamo
        $loan = Http::post(config('services.microservices.loans') . '/loans', [
            'user_id' => $userId,
            'book_id' => $request->book_id,
        ]);

        if (!$loan->successful()) {
            return response()->json(['error' => 'Error al crear préstamo'], 502);
        }

        // 3. Marcar libro como no disponible
        $update = Http::put(config('services.microservices.books') . "/books/{$request->book_id}", [
            'available' => false,
        ]);

        if (!$update->successful()) {
            // El préstamo ya se creó — logeamos pero no revertimos en esta entrega
            Log::warning('Préstamo creado pero no se pudo actualizar disponibilidad del libro', [
                'user_id' => $userId,
                'book_id' => $request->book_id,
                'loan'    => $loan->json(),
            ]);
        }

        Log::info('Préstamo realizado correctamente', [
            'user_id' => $userId,
            'book_id' => $request->book_id,
        ]);

        return response()->json($loan->json(), $loan->status());
    }

    
}
