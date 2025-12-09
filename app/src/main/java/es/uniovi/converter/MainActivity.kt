package es.uniovi.converter

import android.os.Bundle
import android.view.View
import android.widget.EditText
import android.widget.Toast
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat

class MainActivity : AppCompatActivity() {
    val euroToDollar:Double = 1.16;
    lateinit var editTextEuros: EditText;
    lateinit var editTextDollars:EditText;

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContentView(R.layout.activity_main)
        ViewCompat.setOnApplyWindowInsetsListener(findViewById(R.id.main)) { v, insets ->
            val systemBars = insets.getInsets(WindowInsetsCompat.Type.systemBars())
            v.setPadding(systemBars.left, systemBars.top, systemBars.right, systemBars.bottom)
            insets
        }
        editTextEuros = findViewById<EditText>(R.id.editTextEuros)
        editTextDollars = findViewById<EditText>(R.id.editTextDollars)
    }

    fun onClickToDollars(view: View) {
        //Toast.makeText(this, "¡Me han pulsado!", Toast.LENGTH_SHORT).show()
        convert(editTextEuros, editTextDollars, euroToDollar)
    }

    fun onClickToEuros(view: View) {
        //Toast.makeText(this, "¡Me han pulsado!", Toast.LENGTH_SHORT).show()
        convert(editTextDollars, editTextEuros, 1 / euroToDollar)
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