import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Add selectedFolder state
state_pattern = r'var selectedFilter by remember \{ mutableStateOf\("Recent"\) \}'
new_state = """var selectedFilter by remember { mutableStateOf("Recent") }
    var selectedFolder by remember { mutableStateOf("All") }
    var showNewFolderDialog by remember { mutableStateOf(false) }
    var newFolderName by remember { mutableStateOf("") }"""
content = re.sub(state_pattern, new_state, content)

# Add Folders row below Your Bookshelf
bookshelf_pattern = r'Text\(\n\s*text = "📖 Your Bookshelf",\n\s*fontSize = 32\.sp,\n\s*fontWeight = FontWeight\.Bold,\n\s*color = Color\(0xFF5A4C40\)\n\s*\)\n\s*\}'
new_bookshelf = """Text(
                        text = "📖 Your Bookshelf",
                        fontSize = 32.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF5A4C40)
                    )
                }
                
                val folders = remember(booksFlow) {
                    listOf("All") + booksFlow.map { it.folder }.distinct().filter { it.isNotBlank() && it != "All" }.sorted()
                }

                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 0.dp)
                        .horizontalScroll(rememberScrollState()),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text("Folder:", color = Color(0xFF8B7E74), fontSize = 16.sp)
                    folders.forEach { folderName ->
                        FilterChip(
                            selected = selectedFolder == folderName,
                            onClick = { selectedFolder = folderName },
                            label = { Text(if (folderName == "All") "📂 All" else "📁 $folderName", fontSize = 14.sp) },
                            colors = FilterChipDefaults.filterChipColors(
                                selectedContainerColor = Color(0xFF4A8BAD),
                                selectedLabelColor = Color.White,
                                containerColor = Color.Transparent,
                                labelColor = Color(0xFF5A4C40)
                            ),
                            shape = RoundedCornerShape(16.dp),
                            border = if (selectedFolder == folderName) null else FilterChipDefaults.filterChipBorder(enabled = true, selected = false, borderColor = Color(0xFFE8E0CE))
                        )
                    }
                    
                    // Add new folder chip
                    FilterChip(
                        selected = false,
                        onClick = { showNewFolderDialog = true },
                        label = { Text("➕ New", fontSize = 14.sp) },
                        colors = FilterChipDefaults.filterChipColors(
                            containerColor = Color.Transparent,
                            labelColor = Color(0xFF4A8BAD)
                        ),
                        shape = RoundedCornerShape(16.dp),
                        border = FilterChipDefaults.filterChipBorder(enabled = true, selected = false, borderColor = Color(0xFF4A8BAD))
                    )
                }"""
content = re.sub(bookshelf_pattern, new_bookshelf, content)

# Filter books by folder
filter_pattern = r'val books = when \(selectedFilter\) \{\n\s*"Title" -> booksFlow\.sortedBy \{ it\.title \}\n\s*"Last Read" -> booksFlow\.sortedByDescending \{ it\.lastRead \}\n\s*"Favorites" -> booksFlow\.filter \{ it\.isFavorite \}\n\s*"Bookmarks" -> booksFlow\.filter \{ it\.progress > 0f && it\.progress < 1f \}\n\s*else -> booksFlow\.sortedByDescending \{ it\.id \} // Recent\n\s*\}'
new_filter = """val filteredBooks = if (selectedFolder == "All") booksFlow else booksFlow.filter { it.folder == selectedFolder }
                val books = when (selectedFilter) {
                    "Title" -> filteredBooks.sortedBy { it.title }
                    "Last Read" -> filteredBooks.sortedByDescending { it.lastRead }
                    "Favorites" -> filteredBooks.filter { it.isFavorite }
                    "Bookmarks" -> filteredBooks.filter { it.progress > 0f && it.progress < 1f }
                    else -> filteredBooks.sortedByDescending { it.id } // Recent
                }"""
content = re.sub(filter_pattern, new_filter, content)

# Update the AddBookOptionsDialog call
addbook_pattern = r'AddBookOptionsDialog\(\n\s*onDismiss = \{ showAddBookOptions = false \},\n\s*onAddBook = \{ title, author, format, coverUri ->\n\s*ebookViewModel\.addBook\(Book\(title = title, author = author, format = format, localUri = "mock_path", coverUri = coverUri\)\)\n\s*\}\n\s*\)'
new_addbook = """AddBookOptionsDialog(
                onDismiss = { showAddBookOptions = false },
                onAddBook = { title, author, format, coverUri ->
                    val destFolder = if (selectedFolder == "All") "Main" else selectedFolder
                    ebookViewModel.addBook(Book(title = title, author = author, format = format, localUri = "mock_path", coverUri = coverUri, folder = destFolder))
                }
            )
        }
        
        if (showNewFolderDialog) {
            AlertDialog(
                onDismissRequest = { showNewFolderDialog = false },
                title = { Text("New Folder") },
                text = {
                    OutlinedTextField(
                        value = newFolderName,
                        onValueChange = { newFolderName = it },
                        label = { Text("Folder Name") },
                        singleLine = true
                    )
                },
                confirmButton = {
                    Button(
                        onClick = {
                            if (newFolderName.isNotBlank()) {
                                selectedFolder = newFolderName
                                showNewFolderDialog = false
                                newFolderName = ""
                            }
                        }
                    ) {
                        Text("Create")
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showNewFolderDialog = false }) {
                        Text("Cancel")
                    }
                }
            )"""
content = re.sub(addbook_pattern, new_addbook, content)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
