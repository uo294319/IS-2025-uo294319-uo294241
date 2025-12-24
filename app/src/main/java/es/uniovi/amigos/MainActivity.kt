package es.uniovi.amigos

import android.Manifest
import android.app.AlertDialog
import android.content.Context
import android.content.pm.PackageManager
import android.os.Bundle
import android.util.Log
import android.widget.EditText
import androidx.activity.result.contract.ActivityResultContracts
import androidx.activity.viewModels
import androidx.preference.PreferenceManager
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.osmdroid.config.Configuration
import org.osmdroid.tileprovider.tilesource.TileSourceFactory
import org.osmdroid.util.GeoPoint
import org.osmdroid.views.MapView
import org.osmdroid.views.overlay.Marker

class MainActivity : AppCompatActivity() {
    private var map: MapView? = null // Referencia al objeto MapView
    private val viewModel: MainViewModel by viewModels()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // 1. Cargar el layout
        setContentView(R.layout.activity_main)

        // 2. Leer la configuración de la aplicación e inicializar mapa
        // Esta es una operación de E/S en disco, para no bloquear el hilo GUI lo lanzamos
        // en un hilo separado, via una corutina
        lifecycleScope.launch {
            // Dentro de la corutina, usamos un hilo del pool de hilos I/O
            withContext(Dispatchers.IO) {
                val ctx: Context = applicationContext
                Configuration.getInstance().load(ctx, PreferenceManager.getDefaultSharedPreferences(ctx))
            }
            // Una vez cargada la configuración, inicializamos el mapa
            map = findViewById(R.id.map)
            map?.setTileSource(TileSourceFactory.MAPNIK)

            centrarMapaEnEuropa()
        }

        viewModel.amigosList.observe(this) { listaDeAmigos ->
            // Este bloque de código se ejecutará automáticamente
            // cada vez que el ViewModel llame a _amigosList.postValue()
            paintAmigosList(listaDeAmigos)

            // Por ahora, solo verificamos que funciona:
            //Log.d("MainActivity", "¡Observer notificado! Amigos: $listaDeAmigos")
        }

        viewModel.getAmigosList()
        checkAndRequestLocationPermissions()
        askUserName()
    }

    override fun onResume() {
        super.onResume()
        map?.onResume()
    }

    override fun onPause() {
        super.onPause()
        map?.onPause()
    }

    fun centrarMapaEnEuropa() {
        // Esta función mueve el centro del mapa a Paris y ajusta el zoom
        // para que se vea Europa
        val mapController = map?.controller
        mapController?.setZoom(5.5)
        val startPoint = GeoPoint(48.8583, 2.2944)
        mapController?.setCenter(startPoint)
    }

    fun paintAmigosList(amigos: List<Amigo>) {
        //map?.getOverlays()?.clear();
        map?.overlays?.clear();
        for (amigo in amigos) {
            val lat = amigo.lati.toDoubleOrNull()
            val lon = amigo.longi.toDoubleOrNull()
            Log.d("Mapa", "Pintando a ${amigo.name} en ($lat, $lon)")
            if (lat != null && lon != null) {
                addMarker(lat, lon, amigo.name)
            }
        }
        map?.invalidate() // Forzamos el repintado del mapa
    }

    private fun addMarker(latitud: Double, longitud: Double, name: String?) {
        map?.let { mapaNoNulo ->
            val coords = GeoPoint(latitud, longitud)
            val startMarker = Marker(mapaNoNulo)
            startMarker.position = coords
            startMarker.setAnchor(Marker.ANCHOR_CENTER, Marker.ANCHOR_CENTER)
            startMarker.title = name
            startMarker.icon = ContextCompat.getDrawable(this, R.drawable.baseline_man_24)
            mapaNoNulo.overlays.add(startMarker)
        }
    }

    private val requestPermissionLauncher =
        registerForActivityResult(
            ActivityResultContracts.RequestMultiplePermissions()
        ) { permissions ->
            // Este bloque se ejecuta cuando el usuario responde al diálogo
            if (permissions[Manifest.permission.ACCESS_FINE_LOCATION] == true) {
                // Permiso concedido
                Log.d("Permissions", "Permiso de GPS CONCEDIDO")
                viewModel.startLocationUpdates() // Solo si ya tenemos permiso
            } else {
                // Permiso denegado
                Log.d("Permissions", "Permiso de GPS DENEGADO")
                // (Opcional: Mostrar un Toast o un diálogo explicando por qué
                // la función de GPS no funcionará)
            }
        }

    private fun checkAndRequestLocationPermissions() {
        val permissionsToRequest = arrayOf(
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        )

        // Comprueba si ya tenemos los permisos
        if (permissionsToRequest.all
            { ContextCompat.checkSelfPermission(this, it) == PackageManager.PERMISSION_GRANTED }
        ) {
            Log.d("Permissions", "Permisos ya concedidos. Iniciando GPS.")
            viewModel.startLocationUpdates() // Solo si ya tenemos permiso
        } else {
            // Si no los tenemos, lanzamos el diálogo para pedirlos
            Log.d("Permissions", "No tenemos permisos. Solicitándolos...")
            requestPermissionLauncher.launch(permissionsToRequest)
        }
    }

    private fun askUserName() {
        // 1. Crear el constructor del diálogo
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Identificación")
        builder.setMessage("Introduce tu nombre de usuario:")

        // 2. Crear un EditText para que el usuario escriba
        val input = EditText(this)
        builder.setView(input)

        // 3. Configurar el botón "OK"
        builder.setPositiveButton("Aceptar") { dialog, which ->
            val name = input.text.toString()
            // 4. ¡LA CONEXIÓN CLAVE!
            // Si el usuario escribió un nombre, se lo pasamos al ViewModel
            if (name.isNotBlank()) {
                viewModel.setUserName(name)
            }
        }

        // 5. Mostrar el diálogo
        builder.show()
    }
}