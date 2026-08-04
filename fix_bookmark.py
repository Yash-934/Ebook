import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

bookmark_pattern = r'ActionButton\(\n\s*icon = Icons\.Default\.Bookmark,\n\s*tint = Color\(0xFFFFA500\),\n\s*borderColor = textColor\.copy\(alpha = 0\.2f\),\n\s*onClick = \{ scope\.launch \{ snackbarHostState\.showSnackbar\("Bookmark added at current page"\) \} \}\n\s*\)'

new_bookmark = """val isBookmarked = (book?.progress ?: 0f) > 0f && (book?.progress ?: 0f) < 1f
                                    ActionButton(
                                        icon = if (isBookmarked) Icons.Default.Bookmark else Icons.Default.BookmarkBorder,
                                        tint = Color(0xFFFFA500),
                                        borderColor = textColor.copy(alpha = 0.2f),
                                        onClick = { 
                                            book?.let {
                                                ebookViewModel.toggleBookmark(it.id)
                                                scope.launch { snackbarHostState.showSnackbar(if (!isBookmarked) "Bookmark added" else "Bookmark removed") }
                                            }
                                        }
                                    )"""

content = re.sub(bookmark_pattern, new_bookmark, content)

# Make sure we import BookmarkBorder
if "import androidx.compose.material.icons.filled.BookmarkBorder" not in content:
    content = content.replace("import androidx.compose.material.icons.filled.Bookmark", "import androidx.compose.material.icons.filled.Bookmark\nimport androidx.compose.material.icons.filled.BookmarkBorder")

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
