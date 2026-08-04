import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

# Modify ReadScreen signature
sig_pattern = r'fun ReadScreen\(\n\s*bookId: Int,\n\s*ebookViewModel: EbookViewModel,\n\s*settingsViewModel: SettingsViewModel,\n\s*onNavigateBack: \(\) -> Unit\n\)'

new_sig = """fun ReadScreen(
    bookId: Int,
    ebookViewModel: EbookViewModel,
    settingsViewModel: SettingsViewModel,
    scrollTo: Int? = null,
    onNavigateBack: () -> Unit
)"""

content = re.sub(sig_pattern, new_sig, content)

# Add scrolling logic
scroll_pattern = r'val scrollState = rememberScrollState\(\)'

new_scroll = """val scrollState = rememberScrollState()
    
    LaunchedEffect(scrollTo) {
        if (scrollTo != null) {
            delay(100)
            scrollState.scrollTo(scrollTo)
        }
    }"""

content = re.sub(scroll_pattern, new_scroll, content)

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
