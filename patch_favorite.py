import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

pattern1 = r'var isFavorite by remember \{ mutableStateOf\(false\) \}'
replacement1 = r'var isFavorite by remember(book) { mutableStateOf(book?.isFavorite ?: false) }'

content = re.sub(pattern1, replacement1, content)

pattern2 = r'isFavorite = !isFavorite\s*\n\s*scope.launch \{ snackbarHostState.showSnackbar\(if \(isFavorite\) "Added to favorites" else "Removed from favorites"\) \}'
replacement2 = r"""isFavorite = !isFavorite
                                            book?.let {
                                                ebookViewModel.addBook(it.copy(isFavorite = isFavorite))
                                            }
                                            scope.launch { snackbarHostState.showSnackbar(if (isFavorite) "Added to favorites" else "Removed from favorites") }"""
                                            
content = re.sub(pattern2, replacement2, content)

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
