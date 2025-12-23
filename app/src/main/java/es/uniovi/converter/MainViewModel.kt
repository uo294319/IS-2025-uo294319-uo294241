package es.uniovi.converter

import android.util.Log
import android.widget.Toast
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

// File: MainViewModel.kt
// Asegúrate de que el paquete es el mismo que el de MainActivity.kt

class MainViewModel : ViewModel() {

    // Ahora la tasa de cambio estará en el ViewModel en vez de en la Activity
    var euroToDollar: Double = 1.16
    var yaDescargado: Boolean = false  // Para evitar múltiples descargas

    // Lo que va dentro del bloque init se ejecuta cuando se crea el ViewModel
    // lo que ocurrirá una sola vez, incluso si la Activity se destruye y se crea otra nueva.
    init {
        Log.d("MainViewModel", "ViewModel created! Fetching data...")
    }

    // La función que obtiene la tasa de cambio se mueve aqui
    // en vez de en la Activity.
    fun fetchExchangeRate() {
        // Lo primero, si ya fue descargado, no hacer nada
        if (yaDescargado) return

        // En caso contrario, usar un launch para la tarea asíncrona que descargue
        // la tasa de cambio pero ahora el scope es viewModelScope en vez de lifecycleScope
        // Este scope se cancela automáticamente cuando el ViewModel se destruye
        // lo que ocurre si el usuario cierra la app.
        viewModelScope.launch {
            // El contenido es igual que antes, solo que sin el Toast
            // y recuerda poner yaDescargado a true al finalizar
            try {
                val response = RetrofitClient.api.convert("EUR", "USD", 1.0)
                val exchangeRateResponse = response.body()
                if (!response.isSuccessful || exchangeRateResponse == null) {
                    Log.e("MainActivity", "Error al obtener el cambio: ${response.code()}")
                    return@launch
                }
                euroToDollar = exchangeRateResponse.rates.USD
                /*Toast.makeText(
                    this@MainActivity,
                    "Cambio actualizado: $euroToDollar",
                    Toast.LENGTH_SHORT
                ).show()*/
                Log.d("MainActivity", "Cambio actualizado: $euroToDollar")
                yaDescargado = true;
            } catch (e: Exception) {
                Log.e("MainActivity", "Excepción al obtener el cambio", e)
            }
        }
    }
}