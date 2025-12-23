// Archivo: MainViewModel.kt
package es.uniovi.converter

import android.util.Log
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.launch

class MainViewModel : ViewModel() {

    // 1. Creamos el LiveData privado (para que solo el ViewModel pueda escribir)
    // Inicializamos con valores por defecto (1.16 y fecha desconocida o vacía)
    private val _exchangeInfo = MutableLiveData<ExchangeInfo>(ExchangeInfo(1.16, ""))

    // 2. Exponemos un LiveData público e inmutable para que la Activity lo observe
    val exchangeInfo: LiveData<ExchangeInfo> get() = _exchangeInfo

    var yaDescargado: Boolean = false

    init {
        Log.d("MainViewModel", "ViewModel created! Fetching data...")
    }

    fun fetchExchangeRate() {
        if (yaDescargado) return

        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.convert("EUR", "USD", 1.0)
                val exchangeRateResponse = response.body()

                if (!response.isSuccessful || exchangeRateResponse == null) {
                    Log.e("MainViewModel", "Error al obtener el cambio: ${response.code()}")
                    return@launch
                }

                // 3. Obtenemos los datos del servidor
                val newRate = exchangeRateResponse.rates.USD
                val newDate = exchangeRateResponse.date

                // 4. Actualizamos el LiveData. Esto notificará automáticamente a la Activity.
                // Usamos postValue si estuviéramos en un hilo de fondo, pero dentro de
                // viewModelScope.launch (Main dispatcher) también valdría .value = ...
                _exchangeInfo.postValue(ExchangeInfo(newRate, newDate))

                Log.d("MainViewModel", "Cambio actualizado: $newRate ($newDate)")
                yaDescargado = true

            } catch (e: Exception) {
                Log.e("MainViewModel", "Excepción al obtener el cambio", e)
            }
        }
    }
}