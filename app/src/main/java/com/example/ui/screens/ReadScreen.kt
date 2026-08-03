package com.example.ui.screens

import android.graphics.Bitmap
import android.graphics.pdf.PdfRenderer
import android.net.Uri
import android.webkit.WebView
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Book
import androidx.compose.material.icons.filled.Fullscreen
import androidx.compose.material.icons.filled.Search
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.viewinterop.AndroidView
import com.example.data.Book
import com.example.ui.EbookViewModel
import com.example.ui.SettingsViewModel
import io.noties.markwon.Markwon
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.BufferedReader
import java.io.InputStreamReader
import java.util.zip.ZipInputStream

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReadScreen(
    bookId: Int,
    ebookViewModel: EbookViewModel,
    settingsViewModel: SettingsViewModel,
    onNavigateBack: () -> Unit
) {
    val context = LocalContext.current
    var book by remember { mutableStateOf<Book?>(null) }
    var content by remember { mutableStateOf<Any?>(null) }
    var pdfRenderer by remember { mutableStateOf<PdfRenderer?>(null) }
    var pdfPageCount by remember { mutableStateOf(0) }
    var currentPageIndex by remember { mutableStateOf(0) }
    var pdfBitmap by remember { mutableStateOf<Bitmap?>(null) }
    var showSettings by remember { mutableStateOf(false) }

    val themeIndex by settingsViewModel.themeIndex.collectAsState()
    val fontSize by settingsViewModel.fontSize.collectAsState()
    val lineSpacing by settingsViewModel.lineSpacing.collectAsState()
    val scrollMode by settingsViewModel.scrollMode.collectAsState()

    LaunchedEffect(bookId) {
        book = ebookViewModel.allBooks.value.find { it.id == bookId }
        book?.let { b ->
            withContext(Dispatchers.IO) {
                try {
                    val uri = Uri.parse(b.localUri)
                    if (b.format == "PDF") {
                        val pfd = context.contentResolver.openFileDescriptor(uri, "r")
                        pfd?.let {
                            val renderer = PdfRenderer(it)
                            pdfRenderer = renderer
                            pdfPageCount = renderer.pageCount
                            currentPageIndex = (b.progress * renderer.pageCount).toInt().coerceIn(0, renderer.pageCount - 1)
                        }
                    } else if (b.format == "MD" || b.format == "HTML") {
                        val inputStream = context.contentResolver.openInputStream(uri)
                        val reader = BufferedReader(InputStreamReader(inputStream))
                        content = reader.readText()
                        reader.close()
                    } else if (b.format == "EPUB") {
                        val inputStream = context.contentResolver.openInputStream(uri)
                        val zis = ZipInputStream(inputStream)
                        var entry = zis.nextEntry
                        val sb = java.lang.StringBuilder()
                        while (entry != null) {
                            if (entry.name.endsWith(".html") || entry.name.endsWith(".htm") || entry.name.endsWith(".xhtml")) {
                                val reader = BufferedReader(InputStreamReader(zis))
                                sb.append(reader.readText())
                            }
                            entry = zis.nextEntry
                        }
                        content = sb.toString()
                        zis.close()
                    }
                } catch (e: Exception) {
                    e.printStackTrace()
                    content = "Error loading book: ${e.message}"
                }
            }
        }
    }

    LaunchedEffect(currentPageIndex, pdfRenderer) {
        pdfRenderer?.let { renderer ->
            withContext(Dispatchers.IO) {
                if (renderer.pageCount > 0) {
                    val page = renderer.openPage(currentPageIndex)
                    val bitmap = Bitmap.createBitmap(page.width * 2, page.height * 2, Bitmap.Config.ARGB_8888)
                    page.render(bitmap, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY)
                    page.close()
                    pdfBitmap = bitmap
                }
            }
        }
    }

    DisposableEffect(Unit) {
        onDispose {
            book?.let { b ->
                if (b.format == "PDF" && pdfPageCount > 0) {
                    val p = currentPageIndex.toFloat() / pdfPageCount.toFloat()
                    ebookViewModel.updateBookProgress(b, p)
                }
                pdfRenderer?.close()
            }
        }
    }

    val bgColor = MaterialTheme.colorScheme.background
    val fgColor = MaterialTheme.colorScheme.onBackground

    Scaffold(
        topBar = {
            TopAppBar(
                title = {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(Icons.Default.Book, contentDescription = null, tint = Color(0xFFE53935))
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(book?.title?.substringBeforeLast(".") ?: "Loading...", fontWeight = FontWeight.Bold, fontSize = 20.sp)
                    }
                },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                },
                actions = {
                    Button(
                        onClick = onNavigateBack,
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.surfaceVariant),
                        shape = RoundedCornerShape(8.dp),
                        contentPadding = PaddingValues(horizontal = 8.dp),
                        modifier = Modifier.height(32.dp)
                    ) {
                        Text("<- Library", color = MaterialTheme.colorScheme.onSurface)
                    }
                    Spacer(modifier = Modifier.width(8.dp))
                    IconButton(onClick = { showSettings = true }) {
                        Icon(Icons.Default.Settings, contentDescription = "Settings", tint = Color(0xFF4FC3F7))
                    }
                    IconButton(onClick = {}) {
                        Icon(Icons.Default.Search, contentDescription = "Search", tint = Color.Gray)
                    }
                    IconButton(onClick = {}) {
                        Icon(Icons.Default.Fullscreen, contentDescription = "Fullscreen", tint = Color.Gray)
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(containerColor = bgColor, titleContentColor = fgColor, actionIconContentColor = fgColor)
            )
        },
        bottomBar = {
            if (book?.format == "PDF" && pdfPageCount > 0) {
                BottomAppBar(containerColor = bgColor, contentColor = fgColor) {
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        TextButton(onClick = { if (currentPageIndex > 0) currentPageIndex-- }) { Text("Previous", color = fgColor) }
                        Text("Page ${currentPageIndex + 1} of $pdfPageCount", modifier = Modifier.align(Alignment.CenterVertically))
                        TextButton(onClick = { if (currentPageIndex < pdfPageCount - 1) currentPageIndex++ }) { Text("Next", color = fgColor) }
                    }
                }
            }
        },
        containerColor = bgColor
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize().padding(padding).background(bgColor)) {
            if (book == null) {
                CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
            } else {
                when (book?.format) {
                    "PDF" -> {
                        pdfBitmap?.let { bmp ->
                            Image(
                                bitmap = bmp.asImageBitmap(),
                                contentDescription = "PDF Page",
                                modifier = Modifier.fillMaxSize()
                            )
                        } ?: CircularProgressIndicator(modifier = Modifier.align(Alignment.Center))
                    }
                    "HTML", "EPUB" -> {
                        val htmlContent = content as? String ?: ""
                        
                        val cssBg = String.format("#%06X", 0xFFFFFF and bgColor.value.toInt())
                        val cssFg = String.format("#%06X", 0xFFFFFF and fgColor.value.toInt())
                        
                        val customHtml = """
                            <html>
                            <head>
                                <style>
                                    body {
                                        background-color: $cssBg;
                                        color: $cssFg;
                                        font-size: ${fontSize}px;
                                        line-height: $lineSpacing;
                                        padding: 24px;
                                        font-family: Georgia, serif;
                                    }
                                </style>
                            </head>
                            <body>
                                $htmlContent
                            </body>
                            </html>
                        """.trimIndent()
                        
                        AndroidView(
                            factory = { ctx ->
                                WebView(ctx).apply {
                                    settings.javaScriptEnabled = true
                                    setBackgroundColor(android.graphics.Color.TRANSPARENT)
                                    loadDataWithBaseURL(null, customHtml, "text/html", "UTF-8", null)
                                }
                            },
                            update = { webView ->
                                webView.loadDataWithBaseURL(null, customHtml, "text/html", "UTF-8", null)
                            },
                            modifier = Modifier.fillMaxSize()
                        )
                    }
                    "MD" -> {
                        val mdContent = content as? String ?: ""
                        val scrollState = rememberScrollState()
                        Column(modifier = Modifier.fillMaxSize().verticalScroll(scrollState).padding(24.dp)) {
                            val markwon = Markwon.create(context)
                            AndroidView(
                                factory = { ctx ->
                                    android.widget.TextView(ctx).apply {
                                        markwon.setMarkdown(this, mdContent)
                                        setTextColor(android.graphics.Color.parseColor(String.format("#%06X", 0xFFFFFF and fgColor.value.toInt())))
                                        textSize = fontSize
                                        setLineSpacing(0f, lineSpacing)
                                    }
                                },
                                update = { textView ->
                                    markwon.setMarkdown(textView, mdContent)
                                    textView.setTextColor(android.graphics.Color.parseColor(String.format("#%06X", 0xFFFFFF and fgColor.value.toInt())))
                                    textView.textSize = fontSize
                                    textView.setLineSpacing(0f, lineSpacing)
                                }
                            )
                        }
                    }
                    else -> {
                        Text("Unsupported format", modifier = Modifier.align(Alignment.Center), color = fgColor)
                    }
                }
            }
        }
    }

    if (showSettings) {
        SettingsSheet(settingsViewModel, onDismiss = { showSettings = false })
    }
}
