import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

bookmark_pattern = r'val isBookmarked = \(book\?\.progress \?: 0f\) > 0f && \(book\?\.progress \?: 0f\) < 1f\n\s*ActionButton\(\n\s*icon = if \(isBookmarked\) Icons\.Default\.Bookmark else Icons\.Default\.BookmarkBorder,\n\s*tint = Color\(0xFFFFA500\),\n\s*borderColor = textColor\.copy\(alpha = 0\.2f\),\n\s*onClick = \{ \n\s*book\?\.let \{\n\s*ebookViewModel\.toggleBookmark\(it\.id\)\n\s*scope\.launch \{ snackbarHostState\.showSnackbar\(if \(!isBookmarked\) "Bookmark added" else "Bookmark removed"\) \}\n\s*\}\n\s*\}\n\s*\)'

new_bookmark = """val bookmarksArray = try { org.json.JSONArray(book?.bookmarks ?: "[]") } catch(e:Exception){ org.json.JSONArray() }
                                    val isBookmarked = (0 until bookmarksArray.length()).any { 
                                        try { Math.abs(bookmarksArray.getJSONObject(it).getInt("position") - scrollState.value) < 500 } catch(e:Exception){false} 
                                    }
                                    ActionButton(
                                        icon = if (isBookmarked) Icons.Default.Bookmark else Icons.Default.BookmarkBorder,
                                        tint = Color(0xFFFFA500),
                                        borderColor = textColor.copy(alpha = 0.2f),
                                        onClick = { 
                                            book?.let {
                                                if (!isBookmarked) {
                                                    ebookViewModel.addBookmark(it.id, scrollState.value, "Bookmark at ${scrollState.value}")
                                                    scope.launch { snackbarHostState.showSnackbar("Bookmark added") }
                                                }
                                            }
                                        }
                                    )"""

content = re.sub(bookmark_pattern, new_bookmark, content)

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
