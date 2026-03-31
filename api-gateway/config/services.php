<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Third Party Services
    |--------------------------------------------------------------------------
    |
    | This file is for storing the credentials for third party services such
    | as Mailgun, Postmark, AWS and more. This file provides the de facto
    | location for this type of information, allowing packages to have
    | a conventional file to locate the various service credentials.
    |
    */

    'mailgun' => [
        'domain' => env('MAILGUN_DOMAIN'),
        'secret' => env('MAILGUN_SECRET'),
        'endpoint' => env('MAILGUN_ENDPOINT', 'api.mailgun.net'),
        'scheme' => 'https',
    ],

    'postmark' => [
        'token' => env('POSTMARK_TOKEN'),
    ],

    'ses' => [
        'key' => env('AWS_ACCESS_KEY_ID'),
        'secret' => env('AWS_SECRET_ACCESS_KEY'),
        'region' => env('AWS_DEFAULT_REGION', 'us-east-1'),
    ],

    'microservices' => [
        'books'      => env('BOOKS_SERVICE_URL',      'http://localhost:5000'), 
        'notifications' => env('NOTIFICATIONS_SERVICE_URL', 'http://localhost:3000'), 
        'loans'      => env('LOANS_SERVICE_URL',       'http://localhost:3002'), 
        'fines'      => env('FINES_SERVICE_URL',        'http://localhost:8001'),
        'reviews'    => env('REVIEWS_SERVICE_URL',      'http://localhost:5002'),
    ],  

];
