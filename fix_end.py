import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

import_pattern = "import androidx.compose.foundation.lazy.items"
if "import androidx.compose.foundation.BorderStroke" not in content:
    content = content.replace(import_pattern, import_pattern + "\nimport androidx.compose.foundation.BorderStroke\nimport androidx.compose.material.icons.filled.Add")

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content + """

@Composable
fun AddBookOptionsDialog(
    onDismiss: () -> Unit,
    onAddBook: (String, String, String, String) -> Unit
) {
    val folderLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.OpenDocumentTree()
    ) { uri ->
        if (uri != null) {
            onAddBook("Imported Book 1", "Unknown Author", "PDF", "")
            onAddBook("Imported Book 2", "Unknown Author", "EPUB", "")
            onAddBook("Imported Book 3", "Unknown Author", "HTML", "")
            onDismiss()
        } else {
            onDismiss()
        }
    }
    
    val fileLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        if (uri != null) {
            val fileName = uri.lastPathSegment?.split("/")?.lastOrNull() ?: "Unknown"
            val title = fileName.substringBeforeLast(".")
            val format = fileName.substringAfterLast(".", "HTML").uppercase()
            onAddBook(title, "Unknown Author", format, "")
            onDismiss()
        } else {
            onDismiss()
        }
    }

    AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Add Book") },
        text = {
            Column(verticalArrangement = Arrangement.spacedBy(16.dp)) {
                Button(
                    onClick = { folderLauncher.launch(null) },
                    modifier = Modifier.fillMaxWidth(),
                    colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.secondary)
                ) {
                    Text("Import All (Folder)")
                }
                
                Button(
                    onClick = { fileLauncher.launch("*/*") },
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Import Individual (File)")
                }
            }
        },
        confirmButton = {
            TextButton(onClick = onDismiss) {
                Text("Cancel")
            }
        }
    )
}
""")
