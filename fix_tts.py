import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

# Make sure TextToSpeech and LocalContext are imported
if "import android.speech.tts.TextToSpeech" not in content:
    content = content.replace("import androidx.compose.ui.Alignment", "import androidx.compose.ui.Alignment\nimport android.speech.tts.TextToSpeech\nimport androidx.compose.ui.platform.LocalContext")

# Replace isPlayingTTS remember with full TTS setup
tts_pattern = r'var isPlayingTTS by remember \{ mutableStateOf\(false\) \}'

new_tts = """var isPlayingTTS by remember { mutableStateOf(false) }
    val context = LocalContext.current
    var tts by remember { mutableStateOf<TextToSpeech?>(null) }
    
    DisposableEffect(context) {
        val textToSpeech = TextToSpeech(context) { status ->
            if (status == TextToSpeech.SUCCESS) {
                // Initialized
            }
        }
        tts = textToSpeech
        onDispose {
            textToSpeech.stop()
            textToSpeech.shutdown()
        }
    }
    
    val ttsContent = "Folio. A single-file, offline-capable eBook reader. Everything is stored locally. Quickest way to run it is to just open index.html in a browser."
    """

content = re.sub(tts_pattern, new_tts, content)

# Find the button to add the play/stop logic
btn_pattern = r'isPlayingTTS = !isPlayingTTS\n\s*scope\.launch \{ snackbarHostState\.showSnackbar\(if \(isPlayingTTS\) "TTS started" else "TTS stopped"\) \}'

new_btn = """isPlayingTTS = !isPlayingTTS
                                            if (isPlayingTTS) {
                                                tts?.speak(ttsContent, TextToSpeech.QUEUE_FLUSH, null, "TTS_ID")
                                            } else {
                                                tts?.stop()
                                            }
                                            scope.launch { snackbarHostState.showSnackbar(if (isPlayingTTS) "TTS started" else "TTS stopped") }"""

content = re.sub(btn_pattern, new_btn, content)

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
