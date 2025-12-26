package es.uniovi.amigos

import android.app.Application
import android.util.Log
import androidx.lifecycle.AndroidViewModel
import androidx.lifecycle.LiveData
import androidx.lifecycle.MutableLiveData
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MainViewModel(application: Application) : AndroidViewModel(application) {

    private var userName: String? = null
    var userId: Int? = null

    private val locationFlow = application.createLocationFlow()

    // Privada: Solo el ViewModel puede modificar esta lista
    private val _amigosList = MutableLiveData<List<Amigo>>()

    // Pública: La Activity la "verá", pero no podrá modificarla
    val amigosList: LiveData<List<Amigo>> = _amigosList

    init {
        Log.d("MainViewModel", "MainViewModel created")
        startPolling() // Empezamos el polling
    }

    fun getAmigosList() {
        viewModelScope.launch {
            // Código que usa retrofit para inicializar amigosList
            try {
                val response = RetrofitClient.api.getAmigos()
                if (!response.isSuccessful) {
                    Log.e("MainViewModel", "Error en la petición: ${response.code()}")
                    return@launch
                }

                if (response.body() == null) {
                    Log.e("MainViewModel", "La lista de amigos es nula")
                    return@launch
                }



                //_amigosList.setValue(response.body())
                _amigosList.value = response.body()
                Log.d("MainViewModel", "Amigos: ${amigosList.value}")
            } catch (e: Exception) {
                Log.e("MainViewModel", "Excepción al obtener amigos", e)
            }
        }
    }

    private fun startPolling() {
        viewModelScope.launch {
            while (true) {
                Log.d("Polling", "Timer disparado, pidiendo amigos...")
                getAmigosList()
                delay(5000)
            }
        }
    }

    fun startLocationUpdates() {
        // Lanzamos una corutina para consumir asíncronamente del Flow
        viewModelScope.launch {
            locationFlow.collect { result ->
                // Este bloque se llamará cada vez que el Flow emita un valor
                if (result is LocationResult.NewLocation) {
                    val location = result.location
                    Log.d("GPS", "Nueva ubicación: ${location.latitude}, ${location.longitude}")
                    try {
                        val payload = LocationPayload(
                            lati = location.latitude.toString(),
                            longi = location.longitude.toString()
                        )
                        userId?.let { idNoNulo ->
                            val response = RetrofitClient.api.updateAmigoPosition(idNoNulo, payload)
                            if (response.isSuccessful) {
                                Log.d("API", "Posición actualizada para ID $idNoNulo. Servidor responde: ${response.body()}")
                            } else {
                                Log.e("API", "Error al actualizar posición para ID $idNoNulo: ${response.code()}")
                            }
                        }

                    } catch (e: Exception) {
                        Log.e("API", "Excepción al actualizar posición", e)
                    }
                } else if (result is LocationResult.ProviderDisabled) {
                    Log.w("GPS", "El proveedor de GPS está desactivado.")
                } else if (result is LocationResult.PermissionDenied) {
                    Log.e("GPS", "Permiso de ubicación denegado.")
                    // Esto no debería pasar si la Activity lo hizo bien
                }
            }
        }
    }

    fun setUserName(name: String) {
        userName = name
        Log.d("MainViewModel", "Nombre de usuario establecido: $userName")

        viewModelScope.launch {
            try {
                val response = RetrofitClient.api.getAmigoByName(name)

                if (response.isSuccessful && response.body() != null) {
                    val amigo = response.body()
                    userId = amigo?.id
                    Log.d("MainViewModel", "ID obtenido exitosamente: $userId")
                } else {
                    Log.e("MainViewModel", "Error al obtener ID del usuario: ${response.code()}")
                }
            } catch (e: Exception) {
                Log.e("MainViewModel", "Excepción al buscar usuario por nombre", e)
            }
        }
    }
}

