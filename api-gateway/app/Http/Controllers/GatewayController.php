<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;

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
}
