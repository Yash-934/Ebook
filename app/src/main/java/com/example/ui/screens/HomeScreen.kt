package com.example.ui.screens

import android.content.Intent
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Person
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.navigation.NavController
import com.example.R
import com.example.data.Book
import com.example.ui.AuthViewModel
import com.example.ui.EbookViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    navController: NavController,
    ebookViewModel: EbookViewModel,
    authViewModel: AuthViewModel
) {
    val context = LocalContext.current
    val books by ebookViewModel.allBooks.collectAsState()
    val user by authViewModel.currentUser.collectAsState()
    val serverClientId = stringResource(R.string.default_web_client_id)

    val filePickerLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenDocument()
    ) { uri: Uri? ->
        uri?.let {
            context.contentResolver.takePersistableUriPermission(
                it,
                Intent.FLAG_GRANT_READ_URI_PERMISSION
            )
            val name = it.lastPathSegment ?: "Unknown Book"
            val format = if (name.endsWith(".pdf", ignoreCase = true)) "PDF"
                         else if (name.endsWith(".md", ignoreCase = true)) "MD"
                         else if (name.endsWith(".epub", ignoreCase = true)) "EPUB"
                         else "HTML"
            ebookViewModel.insertBook(
                Book(
                    title = name,
                    format = format,
                    localUri = it.toString()
                )
            )
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Ebook Reader") },
                actions = {
                    if (user == null) {
                        TextButton(onClick = { authViewModel.signInWithGoogle(context, serverClientId) }) {
                            Text("Sign In")
                        }
                    } else {
                        IconButton(onClick = { authViewModel.signOut() }) {
                            Icon(Icons.Default.Person, contentDescription = "Sign Out")
                        }
                    }
                }
            )
        },
        floatingActionButton = {
            FloatingActionButton(onClick = {
                filePickerLauncher.launch(arrayOf("application/pdf", "text/html", "text/markdown", "application/epub+zip", "*/*"))
            }) {
                Icon(Icons.Default.Add, contentDescription = "Import Book")
            }
        }
    ) { padding ->
        if (books.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Text("No books imported yet. Tap + to add one.")
            }
        } else {
            LazyColumn(modifier = Modifier.fillMaxSize().padding(padding)) {
                items(books) { book ->
                    Card(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(8.dp)
                            .clickable {
                                navController.navigate("read/${book.id}")
                            }
                    ) {
                        Column(modifier = Modifier.padding(16.dp)) {
                            Text(text = book.title, style = MaterialTheme.typography.titleMedium)
                            Spacer(modifier = Modifier.height(4.dp))
                            Text(text = "Format: ${book.format}", style = MaterialTheme.typography.bodySmall)
                            LinearProgressIndicator(
                                progress = { book.progress },
                                modifier = Modifier.fillMaxWidth().padding(top = 8.dp)
                            )
                        }
                    }
                }
            }
        }
    }
}
