// Archivo: MainActivity.kt
package es.uniovi.converter

import android.os.Bundle
import android.widget.EditText
import android.widget.TextView // Import necesario
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {

    private val viewModel: MainViewModel by viewModels()
    private val deafultRate = 1.16

    lateinit var editTextEuros: EditText
    lateinit var editTextDollars: EditText
    lateinit var textViewInfo: TextView // Referencia para info (rate + fecha)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)

        // Ajuste de insets (código existente)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }

        // Inicializar las variables para modificar layout
        editTextEuros = findViewById(R.id.editTextEuros)
        editTextDollars = findViewById(R.id.editTextDollars)
        textViewInfo = findViewById(R.id.textViewInfo)

        // LiveData. "this" es el LifecycleOwner (la Activity).
        viewModel.exchangeInfo.observe(this) { info ->
            // Este código se ejecuta automáticamente cada vez que _exchangeInfo cambia en el ViewModel
            textViewInfo.text = "1 € = ${info.rate} $ (Fecha: ${info.date})"
        }

        viewModel.fetchExchangeRate()
    }

    fun onClickToDollars(view: android.view.View) {
        // Obtenemos el factor actual del LiveData.
        val factor = viewModel.exchangeInfo.value?.rate ?: deafultRate
        convert(editTextEuros, editTextDollars, factor)
    }

    fun onClickToEuros(view: android.view.View) {
        // Obtenemos el factor actual del LiveData.
        val factor = viewModel.exchangeInfo.value?.rate ?: deafultRate
        convert(editTextDollars, editTextEuros, 1 / factor)
    }

    private fun convert(source: EditText, destination: EditText, factor: Double) {
        val text = source.text.toString()
        val value = text.toDoubleOrNull()
        if (value == null) {
            destination.setText("")
            return
        }
        destination.setText((value * factor).toString())
    }
}