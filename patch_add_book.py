import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Add dialog state to HomeScreen
pattern_state = r'val books by ebookViewModel\.books\.collectAsStateWithLifecycle\(\)'
replacement_state = """val books by ebookViewModel.books.collectAsStateWithLifecycle()
    var showAddBookDialog by remember { mutableStateOf(false) }"""
content = re.sub(pattern_state, replacement_state, content)

# Modify button onClick
pattern_button = r'Button\(\n\s*onClick = \{\n\s*ebookViewModel\.addBook\(\n\s*Book\(\n\s*title = "Sample Book \$\{books\.size \+ 1\}",\n\s*author = "Author Name",\n\s*localUri = "mock_path",\n\s*format = listOf\("PDF", "HTML", "MARKDOWN"\)\.random\(\)\n\s*\)\n\s*\)\n\s*\}'
replacement_button = """Button(
                        onClick = { showAddBookDialog = true }"""
content = re.sub(pattern_button, replacement_button, content)

# Add AddBookDialog definition and call
pattern_bottom = r'(\s*)if \(showSettingsSheet\) \{'
replacement_bottom = r"""\1if (showAddBookDialog) {
\1    AddBookDialog(
\1        onDismiss = { showAddBookDialog = false },
\1        onAddBook = { title, author, format, coverUri ->
\1            ebookViewModel.addBook(Book(title = title, author = author, format = format, localUri = "mock_path", coverUri = coverUri))
\1            showAddBookDialog = false
\1        }
\1    )
\1}
\1if (showSettingsSheet) {"""
content = re.sub(pattern_bottom, replacement_bottom, content)


dialog_code = """
@Composable
fun AddBookDialog(
    onDismiss: () -> Unit,
    onAddBook: (String, String, String, String) -> Unit
) {
    var title by remember { mutableStateOf("") }
    var author by remember { mutableStateOf("") }
    var format by remember { mutableStateOf("HTML") }
    var coverUri by remember { mutableStateOf<android.net.Uri?>(null) }
    
    val launcher = androidx.activity.compose.rememberLauncherForActivityResult(
        contract = androidx.activity.result.contract.ActivityResultContracts.GetContent()
    ) { uri: android.net.Uri? ->
        coverUri = uri
    }

    androidx.compose.material3.AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Add New Book") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(8.dp)) {
                androidx.compose.material3.OutlinedTextField(
                    value = title,
                    onValueChange = { title = it },
                    label = { Text("Title") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                androidx.compose.material3.OutlinedTextField(
                    value = author,
                    onValueChange = { author = it },
                    label = { Text("Author") },
                    singleLine = true,
                    modifier = Modifier.fillMaxWidth()
                )
                
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Cover Image:")
                    Button(onClick = { launcher.launch("image/*") }) {
                        Text(if (coverUri == null) "Select Image" else "Image Selected")
                    }
                }
            }
        },
        confirmButton = {
            Button(
                onClick = {
                    if (title.isNotBlank()) {
                        onAddBook(title, author, format, coverUri?.toString() ?: "")
                    }
                },
                enabled = title.isNotBlank()
            ) {
                Text("Add")
            }
        },
        dismissButton = {
            androidx.compose.material3.TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}
"""
content = content + dialog_code

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
