package com.example.ui.screens

import android.content.Intent
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.AutoStories
import androidx.compose.material.icons.filled.MenuBook
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.navigation.NavController
import com.example.R
import com.example.data.Book
import com.example.ui.AuthViewModel
import com.example.ui.EbookViewModel
import com.example.ui.SettingsViewModel

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    navController: NavController,
    ebookViewModel: EbookViewModel,
    authViewModel: AuthViewModel,
    settingsViewModel: SettingsViewModel
) {
    val context = LocalContext.current
    val books by ebookViewModel.allBooks.collectAsState()
    var sortMode by remember { mutableStateOf("Recent") }
    var showSettings by remember { mutableStateOf(false) }

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
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.MenuBook, contentDescription = null, tint = Color(0xFFE53935))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text("My Library", fontWeight = FontWeight.Bold, fontSize = 20.sp)
                    }
                },
                actions = {
                    IconButton(onClick = { showSettings = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = Color(0xFF4FC3F7))
                    }
                    Button(
                        onClick = {
                            filePickerLauncher.launch(arrayOf("application/pdf", "text/html", "text/markdown", "application/epub+zip", "*/*"))
                        },
                        colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFD89E36)),
                        shape = RoundedCornerShape(8.dp),
                        modifier = Modifier.padding(end = 16.dp)
                    ) {
                        Text("+ Add Book", color = Color.White)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = MaterialTheme.colorScheme.background)
            )
        }
    ) { padding ->
        Column(modifier = Modifier.fillMaxSize().padding(padding)) {
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
            ) {
                Icon(Icons.Default.AutoStories, contentDescription = null, tint = Color.Gray)
                Spacer(modifier = Modifier.width(8.dp))
                Text("Your Bookshelf", fontSize = 24.sp, fontWeight = FontWeight.Medium)
            }
            Row(
                modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Sort:", color = Color.Gray, modifier = Modifier.padding(end = 8.dp))
                val modes = listOf("Recent", "Last Read", "Title")
                modes.forEach { mode ->
                    val isSelected = sortMode == mode
                    Surface(
                        modifier = Modifier.padding(end = 8.dp).clickable { sortMode = mode },
                        color = if (isSelected) Color(0xFFD89E36) else Color.Transparent,
                        shape = RoundedCornerShape(16.dp),
                        border = if (!isSelected) androidx.compose.foundation.BorderStroke(1.dp, Color.LightGray) else null
                    ) {
                        Text(
                            text = mode,
                            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
                            color = if (isSelected) Color.White else Color.Gray,
                            fontSize = 12.sp
                        )
                    }
                }
            }

            if (books.isEmpty()) {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                    Text("Your library is empty", color = Color.Gray)
                }
            } else {
                val sortedBooks = when (sortMode) {
                    "Title" -> books.sortedBy { it.title }
                    else -> books.reversed()
                }
                LazyVerticalGrid(
                    columns = GridCells.Adaptive(minSize = 150.dp),
                    contentPadding = PaddingValues(16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    items(sortedBooks) { book ->
                        BookCard(book = book, onClick = { navController.navigate("read/${book.id}") })
                    }
                }
            }
        }
    }
    
    if (showSettings) {
        // Implement Settings Modal
        SettingsSheet(settingsViewModel, onDismiss = { showSettings = false })
    }
}

@Composable
fun BookCard(book: Book, onClick: () -> Unit) {
    Card(
        onClick = onClick,
        modifier = Modifier
            .fillMaxWidth()
            .aspectRatio(0.6f),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFF1EAD3)),
        shape = RoundedCornerShape(12.dp)
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            Box(
                modifier = Modifier
                    .weight(1f)
                    .fillMaxWidth()
                    .background(Color(0xFFEBE3D0)),
                contentAlignment = Alignment.Center
            ) {
                Icon(
                    Icons.Default.MenuBook,
                    contentDescription = null,
                    tint = Color(0xFFE57373),
                    modifier = Modifier.size(48.dp)
                )
            }
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(Color(0xFFF9F5EC))
                    .padding(12.dp)
            ) {
                Surface(
                    color = Color(0xFFFFECB3),
                    shape = RoundedCornerShape(4.dp)
                ) {
                    Text(
                        text = book.format,
                        color = Color(0xFFF57F17),
                        fontSize = 10.sp,
                        fontWeight = FontWeight.Bold,
                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                    )
                }
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = book.title.substringBeforeLast("."),
                    style = MaterialTheme.typography.titleMedium,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                Text(
                    text = "Unknown Author",
                    style = MaterialTheme.typography.bodySmall,
                    color = Color.Gray
                )
                Spacer(modifier = Modifier.height(12.dp))
                LinearProgressIndicator(
                    progress = { book.progress },
                    modifier = Modifier.fillMaxWidth().height(4.dp),
                    color = Color(0xFFD89E36),
                    trackColor = Color(0xFFE0E0E0)
                )
                Spacer(modifier = Modifier.height(4.dp))
                Text(
                    text = "${(book.progress * 100).toInt()}% read",
                    fontSize = 10.sp,
                    color = Color.Gray
                )
            }
        }
    }
}
