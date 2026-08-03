package com.example.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import androidx.lifecycle.viewModelScope
import com.example.data.Book
import com.example.data.BookRepository
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch

class EbookViewModel(private val repository: BookRepository) : ViewModel() {
    val allBooks: StateFlow<List<Book>> = repository.allBooks.stateIn(
        scope = viewModelScope,
        started = SharingStarted.WhileSubscribed(5000),
        initialValue = emptyList()
    )

    fun addBook(book: Book) {
        viewModelScope.launch {
            repository.insert(book)
        }
    }

    fun updateProgress(bookId: Int, progress: Float) {
        viewModelScope.launch {
            val book = repository.getBookById(bookId)
            if (book != null) {
                repository.update(book.copy(progress = progress))
            }
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
