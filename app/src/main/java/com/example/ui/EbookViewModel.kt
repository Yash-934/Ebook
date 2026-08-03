package com.example.ui

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.data.Book
import com.example.data.BookRepository
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.firestore.FirebaseFirestore
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class EbookViewModel(private val repository: BookRepository) : ViewModel() {
    private val db: FirebaseFirestore? = try { FirebaseFirestore.getInstance() } catch (e: Exception) { null }
    private val auth: FirebaseAuth? = try { FirebaseAuth.getInstance() } catch (e: Exception) { null }
    
    val allBooks: StateFlow<List<Book>> = repository.allBooks.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = emptyList()
    )

    init {
        // Simple one-way sync down for demo purposes
        auth?.addAuthStateListener { firebaseAuth ->
            val user = firebaseAuth.currentUser
            if (user != null) {
                db?.collection("users")?.document(user.uid)?.collection("books")
                    ?.addSnapshotListener { value, error ->
                        if (error != null) {
                            Log.e("EbookViewModel", "Listen failed.", error)
                            return@addSnapshotListener
                        }
                        value?.documents?.forEach { doc ->
                            val progress = doc.getDouble("progress")?.toFloat() ?: 0f
                            val remoteId = doc.id
                            // In a real app we'd map this properly, for now just update existing books if titles match
                            viewModelScope.launch {
                                val currentBooks = repository.allBooks.stateIn(viewModelScope, SharingStarted.Eagerly, emptyList()).value
                                currentBooks.find { it.remoteId == remoteId }?.let { b ->
                                    if (b.progress < progress) {
                                        repository.update(b.copy(progress = progress))
                                    }
                                }
                            }
                        }
                    }
            }
        }
    }

    fun insertBook(book: Book) {
        viewModelScope.launch {
            val user = auth?.currentUser
            var newBook = book
            if (user != null && db != null) {
                val docRef = db.collection("users").document(user.uid).collection("books").document()
                newBook = book.copy(remoteId = docRef.id)
                val remoteData = hashMapOf(
                    "title" to newBook.title,
                    "progress" to newBook.progress
                )
                docRef.set(remoteData)
            }
            repository.insert(newBook)
        }
    }

    fun updateBookProgress(book: Book, progress: Float) {
        viewModelScope.launch {
            val updatedBook = book.copy(progress = progress, lastRead = System.currentTimeMillis())
            repository.update(updatedBook)
            
            // Sync to firestore if logged in
            val user = auth?.currentUser
            if (user != null && updatedBook.remoteId.isNotEmpty() && db != null) {
                db.collection("users").document(user.uid).collection("books").document(updatedBook.remoteId)
                    .update("progress", progress)
            }
        }
    }
    
    fun deleteBook(id: Int) {
        viewModelScope.launch {
            repository.deleteById(id)
        }
    }
}

class EbookViewModelFactory(private val repository: BookRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(EbookViewModel::class.java)) {
            @Suppress("UNCHECKED_CAST")
            return EbookViewModel(repository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}
