package com.example

import android.app.Application
import androidx.room.Room
import com.example.data.AppDatabase
import com.example.data.BookRepository

class MyApplication : Application() {
    val database by lazy {
        Room.databaseBuilder(this, AppDatabase::class.java, "ebook_database").build()
    }
    val repository by lazy {
        BookRepository(database.bookDao())
    }
}
