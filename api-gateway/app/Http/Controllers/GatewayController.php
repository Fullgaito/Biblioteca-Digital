<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

class GatewayController extends Controller
{
    private function headersInternos(Request $request): array
    {
        return [
            'X-Internal-API-Key'    => env('INTERNAL_API_KEY'),
            'X-User-Id'    => $request->user()->id,
            'X-User-Email' => $request->user()->email,
            'Content-Type' => 'application/json',
        ];
    }

    // ── LIBROS ────────────────────────────────────────────

    public function getBooks(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.books') . '/books');

        return response()->json($response->json(), $response->status());
    }

    public function getBook(Request $request, $id)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.books') . "/books/{$id}");

        return response()->json($response->json(), $response->status());
    }

    public function createBook(Request $request)
    {
        $request->validate([
            'title'  => 'required|string|max:255',
            'author' => 'required|string|max:255',
        ]);

        $response = Http::withHeaders($this->headersInternos($request))
            ->post(config('services.microservices.books') . '/books', [
                'title'       => $request->title,
                'author'      => $request->author,
                'isbn'        => $request->isbn,
                'description' => $request->description,
                'category' => $request->category,
                'available'   => $request->available,
                'quantity'    => $request->quantity,
            ]);

        return response()->json($response->json(), $response->status());
    }

    public function updateBook(Request $request, $id)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->put(config('services.microservices.books') . "/books/{$id}", $request->all());

        return response()->json($response->json(), $response->status());
    }

    public function deleteBook(Request $request, $id)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->delete(config('services.microservices.books') . "/books/{$id}");

        return response()->json($response->json(), $response->status());
    }

    // ── PRÉSTAMOS ─────────────────────────────────────────

    public function getLoans(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.loans') . '/loans');

        return response()->json($response->json(), $response->status());
    }

    public function getLoan(Request $request, $id)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.loans') . "/loans/{$id}");

        return response()->json($response->json(), $response->status());
    }

    public function getLoansByUser(Request $request, $userId)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.loans') . "/loans/user/{$userId}");

        return response()->json($response->json(), $response->status());
    }

    public function createLoan(Request $request)
    {
        $request->validate([
            'book_id' => 'required',
        ]);

        $response = Http::withHeaders($this->headersInternos($request))
            ->post(config('services.microservices.loans') . '/loans', [
                'user_id' => $request->user()->id,
                'book_id' => $request->book_id,
            ]);

        return response()->json($response->json(), $response->status());
    }

    public function returnLoan(Request $request, $id)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->put(config('services.microservices.loans') . "/loans/{$id}/return");

        return response()->json($response->json(), $response->status());
    }

    // ── MULTAS ────────────────────────────────────────────

    public function getFines(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.fines') . '/fines');

        return response()->json($response->json(), $response->status());
    }

    public function getFine(Request $request, $id)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.fines') . "/fines/{$id}");

        return response()->json($response->json(), $response->status());
    }

    public function getFinesByUser(Request $request, $userId)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.fines') . "/fines/user/{$userId}");

        return response()->json($response->json(), $response->status());
    }

    public function payFine(Request $request, $id)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->put(config('services.microservices.fines') . "/fines/{$id}/pay", [
                'loan_id' => $request->loan_id,
            ]);

        return response()->json($response->json(), $response->status());
    }

    public function createFine(Request $request)
    {
        $request->validate([
            'user_id' => 'required|integer',
            'loan_id' => 'required',
            'days_late' => 'required|integer|min:1'
        ]);

        $response = Http::withHeaders($this->headersInternos($request))
            ->post(config('services.microservices.fines') . '/fines', [
                'user_id'     => $request->user()->id,
                'loan_id'     => $request->loan_id,
                'days_late'   => $request->days_late,
            ]);

        return response()->json($response->json(), $response->status());
    }

    // ── RESEÑAS ───────────────────────────────────────────

    public function getReviews(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.reviews') . '/reviews');

        return response()->json($response->json(), $response->status());
    }

    public function getReviewsByBook(Request $request, $bookId)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.reviews') . "/reviews/book/{$bookId}");

        return response()->json($response->json(), $response->status());
    }

    public function createReview(Request $request)
    {
        $request->validate([
            'book_id' => 'required',
            'rating'  => 'required|integer|min:1|max:5',
        ]);

        $response = Http::withHeaders($this->headersInternos($request))
            ->post(config('services.microservices.reviews') . '/reviews', [
                'user_id' => $request->user()->id,
                'book_id' => $request->book_id,
                'rating'  => $request->rating,
                'comment' => $request->comment,
            ]);

        return response()->json($response->json(), $response->status());
    }

    public function deleteReview(Request $request, $id)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->delete(config('services.microservices.reviews') . "/reviews/{$id}");

        return response()->json($response->json(), $response->status());
    }

    // ── NOTIFICACIONES ────────────────────────────────────

    public function getNotificationsByUser(Request $request, $userId)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.notifications') . "/notifications/user/{$userId}");

        return response()->json($response->json(), $response->status());
    }

    public function markNotificationRead(Request $request, $id)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->put(config('services.microservices.notifications') . "/notifications/{$id}/read");

        return response()->json($response->json(), $response->status());
    }

    // ── FLUJOS ORQUESTADOS ────────────────────────────────

    public function borrowBookFlow(Request $request)
    {
        $request->validate([
            'book_id' => 'required',
        ]);

        $headers = $this->headersInternos($request);
        $userId  = $request->user()->id;

        // 1. Verificar disponibilidad del libro
        $book = Http::withHeaders($headers)
            ->get(config('services.microservices.books') . "/books/{$request->book_id}");

        if (!$book->successful()) {
            return response()->json(['error' => 'Error al consultar el libro'], 502);
        }

        if (!$book->json('available')) {
            return response()->json(['error' => 'Libro no disponible'], 422);
        }

        // 2. Crear préstamo
        $loan = Http::withHeaders($headers)
            ->post(config('services.microservices.loans') . '/loans', [
                'user_id' => $userId,
                'book_id' => $request->book_id,
            ]);

        if (!$loan->successful()) {
            return response()->json(['error' => 'Error al crear el préstamo'], 502);
        }

        // 3. Marcar libro como no disponible
        Http::withHeaders($headers)
            ->put(config('services.microservices.books') . "/books/{$request->book_id}", [
                'available' => false,
            ]);

        // 4. Notificar al usuario
        Http::withHeaders($headers)
            ->post(config('services.microservices.notifications') . '/notifications', [
                'user_id' => $userId,
                'type'    => 'loan_created',
                'message' => "Préstamo creado para el libro {$request->book_id}",
                'data'    => ['book_id' => $request->book_id, 'loan_id' => $loan->json('id')],
            ]);

        return response()->json($loan->json(), $loan->status());
    }

    public function returnBookFlow(Request $request, $loanId)
    {
        $headers = $this->headersInternos($request);

        // 1. Registrar devolución
        $loan = Http::withHeaders($headers)
            ->put(config('services.microservices.loans') . "/loans/{$loanId}/return");

        if (!$loan->successful()) {
            return response()->json(['error' => 'Error al registrar la devolución'], 502);
        }

        $loanData = $loan->json();

        // 2. Marcar libro como disponible
        Http::withHeaders($headers)
            ->put(config('services.microservices.books') . "/books/{$loanData['book_id']}", [
                'available' => true,
            ]);

        // 3. Notificar devolución
        Http::withHeaders($headers)
            ->post(config('services.microservices.notifications') . '/notifications', [
                'user_id' => $loanData['user_id'],
                'type'    => 'loan_returned',
                'message' => "Devolución registrada para el préstamo {$loanId}",
                'data'    => ['loan_id' => $loanId],
            ]);

        // 4. Si la devolución es tardía, generar multa y notificar
        $today   = now()->toDateString();
        $dueDate = $loanData['due_date'] ?? null;

        if ($dueDate && $today > $dueDate) {
            Http::withHeaders($headers)
                ->post(config('services.microservices.fines') . '/fines', [
                    'user_id'     => $loanData['user_id'],
                    'loan_id'     => $loanId,
                    'due_date'    => $dueDate,
                    'return_date' => $today,
                ]);

            Http::withHeaders($headers)
                ->post(config('services.microservices.notifications') . '/notifications', [
                    'user_id' => $loanData['user_id'],
                    'type'    => 'fine_generated',
                    'message' => "Se generó una multa por devolución tardía del préstamo {$loanId}",
                    'data'    => ['loan_id' => $loanId, 'due_date' => $dueDate],
                ]);
        }

        return response()->json($loanData, $loan->status());
    }
}