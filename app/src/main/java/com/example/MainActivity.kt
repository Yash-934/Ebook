package com.example

import android.annotation.SuppressLint
import android.net.Uri
import android.os.Bundle
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView

class MainActivity : ComponentActivity() {

    private var filePathCallback: ValueCallback<Array<Uri>>? = null

    private val filePickerLauncher = registerForActivityResult(ActivityResultContracts.OpenMultipleDocuments()) { uris ->
        if (uris != null && uris.isNotEmpty()) {
            filePathCallback?.onReceiveValue(uris.toTypedArray())
        } else {
            filePathCallback?.onReceiveValue(null)
        }
        filePathCallback = null
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                AndroidView(
                    factory = { context ->
                        WebView(context).apply {
                            settings.apply {
                                javaScriptEnabled = true
                                domStorageEnabled = true
                                databaseEnabled = true
                                allowFileAccess = true
                                allowContentAccess = true
                                mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
                            }
                            webViewClient = WebViewClient()
                            webChromeClient = object : WebChromeClient() {
                                override fun onShowFileChooser(
                                    webView: WebView?,
                                    callback: ValueCallback<Array<Uri>>?,
                                    fileChooserParams: FileChooserParams?
                                ): Boolean {
                                    filePathCallback?.onReceiveValue(null) // Cancel previous
                                    filePathCallback = callback
                                    filePickerLauncher.launch(arrayOf("*/*"))
                                    return true
                                }
                            }
                            loadUrl("file:///android_asset/index.html")
                        }
                    },
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(innerPadding)
                )
            }
        }
    }
}
