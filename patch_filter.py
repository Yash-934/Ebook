import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

state_pattern = r'var showAddBookDialog by remember \{ mutableStateOf\(false\) \}'
state_replacement = r'var showAddBookDialog by remember { mutableStateOf(false) }\n    var selectedFilter by remember { mutableStateOf("Recent") }'
content = re.sub(state_pattern, state_replacement, content)

filter_pattern = r'val books by ebookViewModel.allBooks.collectAsState\(\)'
filter_replacement = r'val booksFlow by ebookViewModel.allBooks.collectAsState(initial = emptyList())'
content = re.sub(filter_pattern, filter_replacement, content)

lazy_pattern = r'items\(books\) \{ book ->'
lazy_replacement = r"""val books = when (selectedFilter) {
                        "Title" -> booksFlow.sortedBy { it.title }
                        "Last Read" -> booksFlow.sortedByDescending { it.lastRead }
                        "Favorites" -> booksFlow.filter { it.isFavorite }
                        "Bookmarks" -> booksFlow.filter { it.progress > 0f && it.progress < 1f }
                        else -> booksFlow.sortedByDescending { it.id } // Recent
                    }
                    items(books) { book ->"""
content = re.sub(lazy_pattern, lazy_replacement, content)

# update all FilterChips
chip1 = r'FilterChip\(\n\s*selected = true,\n\s*onClick = \{\},'
chip1_r = r"""FilterChip(
                        selected = selectedFilter == "Recent",
                        onClick = { selectedFilter = "Recent" },"""

chip2 = r'FilterChip\(\n\s*selected = false,\n\s*onClick = \{\},\n\s*label = \{ Text\("Favorites"\) \},'
chip2_r = r"""FilterChip(
                        selected = selectedFilter == "Favorites",
                        onClick = { selectedFilter = "Favorites" },
                        label = { Text("Favorites") },"""

chip3 = r'FilterChip\(\n\s*selected = false,\n\s*onClick = \{\},\n\s*label = \{ Text\("Bookmarks"\) \},'
chip3_r = r"""FilterChip(
                        selected = selectedFilter == "Bookmarks",
                        onClick = { selectedFilter = "Bookmarks" },
                        label = { Text("Bookmarks") },"""

chip4 = r'FilterChip\(\n\s*selected = false,\n\s*onClick = \{\},\n\s*label = \{ Text\("Last Read"\) \},'
chip4_r = r"""FilterChip(
                        selected = selectedFilter == "Last Read",
                        onClick = { selectedFilter = "Last Read" },
                        label = { Text("Last Read") },"""

chip5 = r'FilterChip\(\n\s*selected = false,\n\s*onClick = \{\},\n\s*label = \{ Text\("Title"\) \},'
chip5_r = r"""FilterChip(
                        selected = selectedFilter == "Title",
                        onClick = { selectedFilter = "Title" },
                        label = { Text("Title") },"""

content = re.sub(chip1, chip1_r, content)
content = re.sub(chip2, chip2_r, content)
content = re.sub(chip3, chip3_r, content)
content = re.sub(chip4, chip4_r, content)
content = re.sub(chip5, chip5_r, content)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
