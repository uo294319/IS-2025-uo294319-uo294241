package es.uniovi.amigos

import android.annotation.SuppressLint
import android.content.Context
import android.location.Location
import android.location.LocationListener
import android.location.LocationManager
import androidx.core.content.ContextCompat.getSystemService
import kotlinx.coroutines.channels.awaitClose
import kotlinx.coroutines.flow.callbackFlow

// Un objeto 'LocationResult' para manejar también los errores
sealed class LocationResult {
    data class NewLocation(val location: Location) : LocationResult()
    object PermissionDenied : LocationResult()
    object ProviderDisabled : LocationResult()
}

@SuppressLint("MissingPermission") // Los permisos se piden en la Activity
fun Context.createLocationFlow(): kotlinx.coroutines.flow.Flow<LocationResult> {
    val locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager

    // Comprueba si el GPS está activado
    val isGpsEnabled = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)
    if (!isGpsEnabled) {
        return kotlinx.coroutines.flow.flowOf(LocationResult.ProviderDisabled)
    }

    // callbackFlow es la magia: convierte un listener en un Flow
    return callbackFlow {
        val locationListener = object : LocationListener {
            override fun onLocationChanged(location: Location) {
                // Ofrece la nueva ubicación al Flow
                trySend(LocationResult.NewLocation(location))
            }
            override fun onProviderDisabled(provider: String) {
                trySend(LocationResult.ProviderDisabled)
            }
        }

        // 1. Registra el listener (solo enviará actualizaciones si el teléfono
        //    se mueve más de 10 metros y aún en ese caso, no más a menudo
        //    que cada 5 segundos)
        locationManager.requestLocationUpdates(
            LocationManager.GPS_PROVIDER,
            5000L, // 5 segundos
            10f,   // 10 metros
            locationListener
        )

        // 2. awaitClose se ejecuta cuando el Flow se cancela
        //    (ej. cuando el viewModelScope se destruye)
        awaitClose {
            // 3. Limpia el listener
            locationManager.removeUpdates(locationListener)
        }
    }
}