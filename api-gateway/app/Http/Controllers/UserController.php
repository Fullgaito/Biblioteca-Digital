<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\User;

class UserController extends Controller
{
    public function register(Request $request){
        // Validaciones
        $validatedData = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|string|email|max:255|unique:users',
            'password' => 'required|string|min:8|confirmed',
            'cuestion' => 'required|string|max:255',
            'answer' => 'required|string|max:255',
        ]);
        //crear usuario
        $user = User::create([
            'name' => $validatedData['name'],
            'email' => $validatedData['email'],
            'password' => bcrypt($validatedData['password']),
            'cuestion' => $request->cuestion,
            'answer' => $request->answer,
        ]);
        // Respuesta
        return response()->json(['message' => 'User registered successfully', 'user' => $user], 201);
    }

    public function login(Request $request)
    {
        $user = User::where('email', $request->email)->first(); ##busca el usuario por email en la base de datos

        if(!$user || !password_verify($request->password, $user->password)){ ##la que llega del request no coincide con la que esta en la base de datos
            return response()->json(['message' => 'Credenciales incorrectas'], 401); ##401 es el codigo de error para no autorizado
        }

        $token=$user->createToken('auth_token')->plainTextToken; ##crea un token de autenticacion para el usuario y lo devuelve como texto plano
        return response()->json(['access_token' => $token, 'token_type' => 'Bearer']); ##devuelve el token de acceso y el tipo de token (Bearer es un tipo de token que se utiliza para la autenticacion)

    }

    public function logout(Request $request)
    {
        $request->user()->currentAccessToken()->delete(); ##elimina el token de acceso actual del usuario que hizo la solicitud
        return response()->json(['message' => 'Cierre de sesión exitoso']); ##devuelve un mensaje de cierre de sesión exitoso
    }
    
    //function me devuelve la informacion del usuario autenticado
    public function me(Request $request)
    {
        return response()->json($request->user());
    }

    public function recuperarPassword(Request $request)
    {
        $request->validate([
            'email' => 'required|email',
            'new_password' => 'required|string|min:8',
        ]);

        $user = User::where('email', $request->email)->first(); ##busca el usuario por email en la base de datos

        if(!$user){ ##si no encuentra el usuario
            return response()->json(['message' => 'Usuario no encontrado'], 404); ##404 es el codigo de error para no encontrado
        }

        //Logica para pregunta de seguridad y respuesta
        $question = $request->input('cuestion', $request->input('pregunta'));
        $answer   = $request->input('answer', $request->input('respuesta'));

        if (!$question || !$answer) {
            return response()->json(['message' => 'Pregunta o respuesta requerida'], 400);
        }

        $preguntaValida = $question === $user->cuestion;
        $respuestaValida = $answer === $user->answer;

        if (!$preguntaValida || !$respuestaValida) {
            return response()->json(['message' => 'Pregunta o respuesta incorrecta'], 400);
        }

        // Actualizar contraseña
        $user->password = bcrypt($request->new_password);
        $user->save();

        return response()->json(['message' => 'Contraseña actualizada correctamente']);
    }
}
