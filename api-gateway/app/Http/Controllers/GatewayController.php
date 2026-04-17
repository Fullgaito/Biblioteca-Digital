<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Carbon;

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
                'unit_price'  => $request->unit_price,
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

    public function activos(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.loans') . '/loans/activos');

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

    // ── Ventas(sales) ───────────────────────────────────────────

    public function createSale(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->post(config('services.microservices.sales') . '/sales', [
                'user_id' => $request->user_id,
                'book_id' => $request->book_id,
                'quantity' => $request->quantity,
            ]);

        return response()->json($response->json(), $response->status());
    }

    public function getSalesByUser(Request $request, $userId)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.sales') . "/sales/user/{$userId}");

        return response()->json($response->json(), $response->status());
    }

    public function getSale(Request $request, $id)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.sales') . "/sales/{$id}");

        return response()->json($response->json(), $response->status());
    }

    public function getSales(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.sales') . '/sales');

        return response()->json($response->json(), $response->status());
    }

    // ── Reports────────────────────────────────────

    public function getMostBorrowedBooks(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.reports') . '/reports/loans/most-borrowed-books');

        return response()->json($response->json(), $response->status());
    }

    public function getTotalLoans(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.reports') . '/reports/loans/total-loans');

        return response()->json($response->json(), $response->status());
    }

    public function getTopUsersFines(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.reports') . '/reports/fines/top-users-fines');

        return response()->json($response->json(), $response->status());
    }

    public function getTotalFines(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.reports') . '/reports/fines/total-fines');

        return response()->json($response->json(), $response->status());
    }

    public function getTotalFinesAmount(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.reports') . '/reports/fines/total-fines-amount');

        return response()->json($response->json(), $response->status());
    }

    public function getMostSoldBooks(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.reports') . '/reports/sales/most-sold-books');

        return response()->json($response->json(), $response->status());
    }

    public function getTotalSales(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.reports') . '/reports/sales/total-sales');

        return response()->json($response->json(), $response->status());
    }

    public function getTotalRevenue(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.reports') . '/reports/sales/total-revenue');

        return response()->json($response->json(), $response->status());
    }

    public function getDashboard(Request $request)
    {
        $response = Http::withHeaders($this->headersInternos($request))
            ->get(config('services.microservices.reports') . '/reports/dashboard');

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

        // 3. Sincronizar disponibilidad del libro (best effort)
        // El stock real se gestiona en Books (y Loans ya decrementa quantity).
        $bookAfter = Http::withHeaders($headers)
            ->get(config('services.microservices.books') . "/books/{$request->book_id}");

        if ($bookAfter->successful()) {
            $qty = (int) ($bookAfter->json('quantity') ?? 0);
            $available = $qty > 0;

            Http::withHeaders($headers)
                ->put(config('services.microservices.books') . "/books/{$request->book_id}", [
                    'available' => $available,
                ]);
        }

        // 4. Notificaciones (si existe microservicio)
        $notificationsBase = config('services.microservices.notifications');
        if ($notificationsBase) {
            Http::withHeaders($headers)
                ->post($notificationsBase . '/notifications', [
                    'user_id' => $userId,
                    'type'    => 'loan_created',
                    'message' => "Préstamo creado para el libro {$request->book_id}",
                    'data'    => ['book_id' => $request->book_id, 'loan_id' => $loan->json('id')],
                ]);
        }

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

        // 2. Sincronizar disponibilidad del libro (best effort)
        if (!empty($loanData['book_id'])) {
            $bookAfter = Http::withHeaders($headers)
                ->get(config('services.microservices.books') . "/books/{$loanData['book_id']}");

            if ($bookAfter->successful()) {
                $qty = (int) ($bookAfter->json('quantity') ?? 0);
                $available = $qty > 0;

                Http::withHeaders($headers)
                    ->put(config('services.microservices.books') . "/books/{$loanData['book_id']}", [
                        'available' => $available,
                    ]);
            }
        }

        // 3. Notificar devolución (si existe microservicio)
        $notificationsBase = config('services.microservices.notifications');
        if ($notificationsBase) {
            Http::withHeaders($headers)
                ->post($notificationsBase . '/notifications', [
                    'user_id' => $loanData['user_id'] ?? null,
                    'type'    => 'loan_returned',
                    'message' => "Devolución registrada para el préstamo {$loanId}",
                    'data'    => ['loan_id' => $loanId],
                ]);
        }

        // 4. Si la devolución es tardía, generar multa y notificar
        $today = Carbon::now()->startOfDay();
        $dueDateRaw = $loanData['due_date'] ?? null;
        $loanDateRaw = $loanData['loan_date'] ?? null;

        $dueDate = null;
        if ($dueDateRaw) {
            $dueDate = Carbon::parse($dueDateRaw)->startOfDay();
        } elseif ($loanDateRaw) {
            $dueDate = Carbon::parse($loanDateRaw)->addDays(7)->startOfDay();
        }

        if ($dueDate && $today->greaterThan($dueDate)) {
            Http::withHeaders($headers)
                ->post(config('services.microservices.fines') . '/fines', [
                    'user_id'     => $loanData['user_id'] ?? null,
                    'loan_id'     => $loanId,
                    'due_date'    => $dueDate->toDateString(),
                    'return_date' => $today->toDateString(),
                ]);

            if ($notificationsBase) {
                Http::withHeaders($headers)
                    ->post($notificationsBase . '/notifications', [
                        'user_id' => $loanData['user_id'] ?? null,
                        'type'    => 'fine_generated',
                        'message' => "Se generó una multa por devolución tardía del préstamo {$loanId}",
                        'data'    => ['loan_id' => $loanId, 'due_date' => $dueDate->toDateString()],
                    ]);
            }
        }

        return response()->json($loanData, $loan->status());
    }
}