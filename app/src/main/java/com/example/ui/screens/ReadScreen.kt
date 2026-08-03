package com.example.ui.screens

import android.graphics.Bitmap
import android.graphics.pdf.PdfRenderer
import android.net.Uri
import android.os.ParcelFileDescriptor
import android.webkit.WebView
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import com.example.data.Book
import com.example.ui.EbookViewModel
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
    onNavigateBack: () -> Unit
) {
    val context = LocalContext.current
    var book by remember { mutableStateOf<Book?>(null) }
    var content by remember { mutableStateOf<Any?>(null) } // Can be String for MD, or something else
    var pdfRenderer by remember { mutableStateOf<PdfRenderer?>(null) }
    var pdfPageCount by remember { mutableStateOf(0) }
    var currentPageIndex by remember { mutableStateOf(0) }
    var pdfBitmap by remember { mutableStateOf<Bitmap?>(null) }

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
    
    // Save progress when leaving
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

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text(book?.title ?: "Loading...") },
                navigationIcon = {
                    IconButton(onClick = onNavigateBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        },
        bottomBar = {
            if (book?.format == "PDF" && pdfPageCount > 0) {
                BottomAppBar {
                    Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.SpaceBetween) {
                        TextButton(onClick = { if (currentPageIndex > 0) currentPageIndex-- }) { Text("Previous") }
                        Text("Page ${currentPageIndex + 1} of $pdfPageCount")
                        TextButton(onClick = { if (currentPageIndex < pdfPageCount - 1) currentPageIndex++ }) { Text("Next") }
                    }
                }
            }
        }
    ) { padding ->
        Box(modifier = Modifier.fillMaxSize().padding(padding)) {
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
                        AndroidView(
                            factory = { ctx ->
                                WebView(ctx).apply {
                                    settings.javaScriptEnabled = true
                                    loadDataWithBaseURL(null, htmlContent, "text/html", "UTF-8", null)
                                }
                            },
                            modifier = Modifier.fillMaxSize()
                        )
                    }
                    "MD" -> {
                        val mdContent = content as? String ?: ""
                        val scrollState = rememberScrollState()
                        Column(modifier = Modifier.fillMaxSize().verticalScroll(scrollState).padding(16.dp)) {
                            val markwon = Markwon.create(context)
                            val parsed = markwon.toMarkdown(mdContent)
                            // Basic render using AndroidView with TextView for Markwon
                            AndroidView(factory = { ctx ->
                                android.widget.TextView(ctx).apply {
                                    markwon.setMarkdown(this, mdContent)
                                }
                            })
                        }
                    }
                    else -> {
                        Text("Unsupported format", modifier = Modifier.align(Alignment.Center))
                    }
                }
            }
        }
    }
}
