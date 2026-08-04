import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Replace the shelf grid with LazyVerticalGrid
grid_pattern = r'// Bookshelf Grid.*?LazyColumn.*?\n\s*\}\n\s*\}\n\s*\}\n\s*\}'
new_grid = """// Bookshelf Grid
                androidx.compose.foundation.lazy.grid.LazyVerticalGrid(
                    columns = androidx.compose.foundation.lazy.grid.GridCells.Adaptive(120.dp),
                    modifier = Modifier.fillMaxSize(),
                    contentPadding = PaddingValues(16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    androidx.compose.foundation.lazy.grid.items(books) { book ->
                        BookItem(
                            book = book,
                            onClick = { navController.navigate("read/${book.id}") },
                            onDelete = { ebookViewModel.deleteBook(book.id) }
                        )
                    }
                }
            }
        }"""

content = re.sub(grid_pattern, new_grid, content, flags=re.DOTALL)

# Replace BookshelfRow and BookItem3D with just BookItem
row_pattern = r'@Composable\nfun BookshelfRow.*?@OptIn\(ExperimentalFoundationApi::class\)\n@Composable\nfun BookItem3D\('
new_item = """@OptIn(ExperimentalFoundationApi::class)
@Composable
fun BookItem("""

content = re.sub(row_pattern, new_item, content, flags=re.DOTALL)

# Fix Icons.Default.MenuBook deprecation warning in the BookItem/BookItem3D
content = content.replace("Icons.Default.MenuBook", "Icons.AutoMirrored.Filled.MenuBook")

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
