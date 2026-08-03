package com.example.ui.screens

import android.content.Intent
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.Book
import androidx.compose.material.icons.filled.Person
import androidx.compose.material.icons.filled.Search
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
    var searchQuery by remember { mutableStateOf("") }

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
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 48.dp, start = 16.dp, end = 16.dp, bottom = 8.dp)
            ) {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween,
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    Text(
                        "Library",
                        style = MaterialTheme.typography.headlineLarge.copy(fontWeight = FontWeight.ExtraBold)
                    )
                    Row {
                        IconButton(onClick = { navController.navigate("settings") }) {
                            Icon(Icons.Default.Settings, contentDescription = "Settings", tint = MaterialTheme.colorScheme.onSurface)
                        }
                        if (user == null) {
                            TextButton(onClick = { authViewModel.signInWithGoogle(context, serverClientId) }) {
                                Text("Sign In")
                            }
                        } else {
                            IconButton(onClick = { authViewModel.signOut() }) {
                                Icon(Icons.Default.Person, contentDescription = "Sign Out", tint = MaterialTheme.colorScheme.primary)
                            }
                        }
                    }
                }
                
                Spacer(modifier = Modifier.height(16.dp))
                
                OutlinedTextField(
                    value = searchQuery,
                    onValueChange = { searchQuery = it },
                    modifier = Modifier.fillMaxWidth(),
                    placeholder = { Text("Search your books...") },
                    leadingIcon = { Icon(Icons.Default.Search, contentDescription = "Search") },
                    shape = RoundedCornerShape(24.dp),
                    colors = OutlinedTextFieldDefaults.colors(
                        focusedBorderColor = MaterialTheme.colorScheme.primary,
                        unfocusedBorderColor = MaterialTheme.colorScheme.outline.copy(alpha = 0.3f),
                        focusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f),
                        unfocusedContainerColor = MaterialTheme.colorScheme.surfaceVariant.copy(alpha = 0.3f)
                    ),
                    singleLine = true
                )
            }
        },
        floatingActionButton = {
            FloatingActionButton(
                onClick = {
                    filePickerLauncher.launch(arrayOf("application/pdf", "text/html", "text/markdown", "application/epub+zip", "*/*"))
                },
                containerColor = MaterialTheme.colorScheme.primary,
                contentColor = MaterialTheme.colorScheme.onPrimary,
                modifier = Modifier.padding(16.dp)
            ) {
                Icon(Icons.Default.Add, contentDescription = "Import Book")
            }
        }
    ) { padding ->
        if (books.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize().padding(padding), contentAlignment = Alignment.Center) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Icon(
                        Icons.Default.Book, 
                        contentDescription = null, 
                        modifier = Modifier.size(72.dp), 
                        tint = MaterialTheme.colorScheme.onSurfaceVariant.copy(alpha = 0.5f)
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        "Your library is empty", 
                        style = MaterialTheme.typography.titleLarge,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                    Spacer(modifier = Modifier.height(8.dp))
                    Text(
                        "Tap the + button to import books", 
                        style = MaterialTheme.typography.bodyMedium,
                        color = MaterialTheme.colorScheme.onSurfaceVariant
                    )
                }
            }
        } else {
            val filteredBooks = books.filter { it.title.contains(searchQuery, ignoreCase = true) }
            LazyVerticalGrid(
                columns = GridCells.Adaptive(minSize = 130.dp),
                contentPadding = PaddingValues(16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp),
                verticalArrangement = Arrangement.spacedBy(24.dp),
                modifier = Modifier.fillMaxSize().padding(padding)
            ) {
                items(filteredBooks) { book ->
                    BookCard(book = book, onClick = { navController.navigate("read/${book.id}") })
                }
            }
        }
    }
}

@Composable
fun BookCard(book: Book, onClick: () -> Unit) {
    val cardColors = listOf(
        Color(0xFF5C6BC0), // Indigo
        Color(0xFF26A69A), // Teal
        Color(0xFFEC407A), // Pink
        Color(0xFFFFA726), // Orange
        Color(0xFF66BB6A), // Green
        Color(0xFF7E57C2)  // Deep Purple
    )
    val colorIndex = Math.abs(book.title.hashCode()) % cardColors.size
    val coverColor = cardColors[colorIndex]

    Column(modifier = Modifier.width(130.dp)) {
        Card(
            onClick = onClick,
            modifier = Modifier
                .fillMaxWidth()
                .aspectRatio(0.65f),
            elevation = CardDefaults.cardElevation(defaultElevation = 6.dp),
            colors = CardDefaults.cardColors(containerColor = coverColor)
        ) {
            Box(modifier = Modifier.fillMaxSize()) {
                // Book format badge
                Surface(
                    color = Color.Black.copy(alpha = 0.3f),
                    modifier = Modifier.align(Alignment.TopEnd).padding(8.dp),
                    shape = MaterialTheme.shapes.small
                ) {
                    Text(
                        text = book.format,
                        color = Color.White,
                        style = MaterialTheme.typography.labelSmall.copy(fontWeight = FontWeight.Bold),
                        modifier = Modifier.padding(horizontal = 6.dp, vertical = 2.dp)
                    )
                }

                // Title centered on cover
                Text(
                    text = book.title.substringBeforeLast("."),
                    style = MaterialTheme.typography.titleMedium.copy(fontWeight = FontWeight.Bold),
                    color = Color.White,
                    maxLines = 4,
                    overflow = TextOverflow.Ellipsis,
                    modifier = Modifier
                        .align(Alignment.Center)
                        .padding(16.dp)
                )

                // Progress bar at the bottom of cover
                if (book.progress > 0) {
                    LinearProgressIndicator(
                        progress = { book.progress },
                        modifier = Modifier
                            .fillMaxWidth()
                            .height(4.dp)
                            .align(Alignment.BottomCenter),
                        color = MaterialTheme.colorScheme.primaryContainer,
                        trackColor = Color.Black.copy(alpha = 0.2f)
                    )
                }
            }
        }
        Spacer(modifier = Modifier.height(8.dp))
        Text(
            text = book.title,
            style = MaterialTheme.typography.bodyMedium.copy(fontWeight = FontWeight.Medium),
            maxLines = 2,
            overflow = TextOverflow.Ellipsis
        )
        if (book.progress > 0) {
            val percentage = (book.progress * 100).toInt()
            Text(
                text = "$percentage% read",
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant
            )
        }
    }
}
