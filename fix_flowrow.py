import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Add import
if "import androidx.compose.foundation.layout.FlowRow" not in content:
    content = content.replace("import androidx.compose.foundation.layout.*", "import androidx.compose.foundation.layout.*\nimport androidx.compose.foundation.layout.FlowRow")
elif "import androidx.compose.foundation.layout.FlowRow" not in content and "import androidx.compose.foundation.layout.Row" in content:
    pass # we'll just add it at the top
else:
    # Just append it below package if we really can't find layout.*
    if "import androidx.compose.foundation.layout.FlowRow" not in content:
        content = content.replace("package com.example.ui.screens", "package com.example.ui.screens\n\nimport androidx.compose.foundation.layout.FlowRow")


# Update Sort row
sort_pattern = r'// Sort row\n\s*Row\(\n\s*modifier = Modifier\n\s*\.fillMaxWidth\(\)\n\s*\.padding\(horizontal = 16\.dp\)\n\s*\.horizontalScroll\(rememberScrollState\(\)\),\n\s*verticalAlignment = Alignment\.CenterVertically,\n\s*horizontalArrangement = Arrangement\.spacedBy\(8\.dp\)\n\s*\) \{\n\s*Text\("Sort:", color = GreyText, fontSize = 18\.sp, modifier = Modifier\.padding\(end = 4\.dp\)\)\n\s*val filters = listOf\(\n\s*"Recent" to "🕐",\n\s*"Last Read" to "📖",\n\s*"Title" to "🔤"\n\s*\)'

new_sort = """// Sort row
                FlowRow(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text("Sort:", color = GreyText, fontSize = 18.sp, modifier = Modifier.padding(end = 4.dp).align(Alignment.CenterVertically))
                    
                    val filters = listOf(
                        "Recent" to "🕐",
                        "Last Read" to "📖",
                        "Title" to "🔤",
                        "Favorites" to "❤️",
                        "Bookmarks" to "🔖"
                    )"""
content = re.sub(sort_pattern, new_sort, content)

# Update Folders row
folders_pattern = r'Row\(\n\s*modifier = Modifier\n\s*\.fillMaxWidth\(\)\n\s*\.padding\(horizontal = 16\.dp, vertical = 8\.dp\)\n\s*\.horizontalScroll\(rememberScrollState\(\)\),\n\s*verticalAlignment = Alignment\.CenterVertically,\n\s*horizontalArrangement = Arrangement\.spacedBy\(8\.dp\)\n\s*\) \{\n\s*Text\("Folder:", color = GreyText, fontSize = 18\.sp, modifier = Modifier\.padding\(end = 4\.dp\)\)'

new_folders = """FlowRow(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    horizontalArrangement = Arrangement.spacedBy(8.dp),
                    verticalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text("Folder:", color = GreyText, fontSize = 18.sp, modifier = Modifier.padding(end = 4.dp).align(Alignment.CenterVertically))"""
content = re.sub(folders_pattern, new_folders, content)

# Update the books variable switch case
books_pattern = r'val filteredBooks = if \(selectedFolder == "All"\) booksFlow else booksFlow\.filter \{ it\.folder == selectedFolder \}\n\s*val books = when \(selectedFilter\) \{\n\s*"Title" -> filteredBooks\.sortedBy \{ it\.title \}\n\s*"Last Read" -> filteredBooks\.sortedByDescending \{ it\.lastRead \}\n\s*else -> filteredBooks\.sortedByDescending \{ it\.id \}\n\s*\}'

new_books = """val filteredBooks = if (selectedFolder == "All") booksFlow else booksFlow.filter { it.folder == selectedFolder }
                val books = when (selectedFilter) {
                    "Title" -> filteredBooks.sortedBy { it.title }
                    "Last Read" -> filteredBooks.sortedByDescending { it.lastRead }
                    "Favorites" -> filteredBooks.filter { it.isFavorite }
                    "Bookmarks" -> filteredBooks.filter { it.progress > 0f && it.progress < 1f }
                    else -> filteredBooks.sortedByDescending { it.id }
                }"""
content = re.sub(books_pattern, new_books, content)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
