package com.example.data

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "books")
data class Book(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val title: String,
    val author: String = "",
    val format: String, // PDF, MD, HTML, EPUB
    val localUri: String = "",
    val remoteId: String = "",
    val progress: Float = 0f,
    val lastRead: Long = System.currentTimeMillis()
)
