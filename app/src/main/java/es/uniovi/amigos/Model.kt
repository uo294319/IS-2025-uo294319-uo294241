package es.uniovi.amigos

import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.PUT
import retrofit2.http.Path

// Data class para mapear la información de un amigo del JSON.
// Se omiten 'id' y 'device' como solicitaste.
data class Amigo(
    val id: Int,
    val name: String,
    val lati: String,
    val longi: String
)

data class LocationPayload(
    val lati: String,
    val longi: String
)

// Interfaz que define el endpoint para obtener la lista de amigos.
interface AmigosApiService {
    @GET("/api/amigos")
    suspend fun getAmigos(): Response<List<Amigo>>

    @GET("/api/amigo/byName/{name}")
    suspend fun getAmigoByName(
        @Path("name") amigoName: String
    ): Response<Amigo>

    @PUT("api/amigo/{id}")
    suspend fun updateAmigoPosition(
        @Path("id") amigoId: Int,
        @Body payload: LocationPayload
    ): Response<Amigo>
}

// Objeto Singleton para gestionar la conexión con Retrofit.
object RetrofitClient {
    // URL base extraída de la dirección ngrok proporcionada.
    private const val BASE_URL = "https://bradyauxetically-misadjusted-kristeen.ngrok-free.dev/"

    private val retrofit by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
    }

    // La instancia de la API que usará la aplicación.
    val api: AmigosApiService by lazy {
        retrofit.create(AmigosApiService::class.java)
    }
}