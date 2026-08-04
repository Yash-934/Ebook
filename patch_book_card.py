import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# I want to replace the whole BookItem function.
pattern = r'@Composable\nfun BookItem\(book: Book, onClick: \(\) -> Unit\) \{.*?\n\}'
replacement = """@Composable
fun BookItem(book: Book, onClick: () -> Unit) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .height(280.dp)
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFFFF8E7)),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.fillMaxSize()) {
            // Cover part
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(0.6f)
                    .background(Color(0xFFE8E0CE)),
                contentAlignment = Alignment.Center
            ) {
                if (book.coverUri.isNotEmpty()) {
                    coil.compose.AsyncImage(
                        model = book.coverUri,
                        contentDescription = "Book Cover",
                        modifier = Modifier.fillMaxSize(),
                        contentScale = androidx.compose.ui.layout.ContentScale.Crop
                    )
                } else {
                    Icon(
                        imageVector = Icons.Default.MenuBook,
                        contentDescription = null,
                        modifier = Modifier.size(64.dp),
                        tint = Color(0xFFE29578) 
                    )
                }
            }
            
            // Details part
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(0.4f)
                    .padding(12.dp)
            ) {
                // Format Badge
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(Color(0xFFFDF3D0))
                        .padding(horizontal = 8.dp, vertical = 4.dp)
                ) {
                    Text(
                        text = book.format,
                        color = Color(0xFFB8860B),
                        fontSize = 11.sp,
                        fontWeight = FontWeight.Bold
                    )
                }
                
                Spacer(modifier = Modifier.height(8.dp))
                
                Text(
                    text = book.title,
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp,
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis,
                    lineHeight = 20.sp,
                    color = Color(0xFF5A4C40)
                )
                
                Spacer(modifier = Modifier.height(2.dp))
                
                Text(
                    text = book.author.ifEmpty { "Unknown Author" },
                    fontSize = 13.sp,
                    color = Color(0xFF8B7E74),
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
                
                Spacer(modifier = Modifier.weight(1f))
                
                LinearProgressIndicator(
                    progress = { book.progress },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(6.dp)
                        .clip(RoundedCornerShape(3.dp)),
                    color = Color(0xFFB8860B),
                    trackColor = Color(0xFFE8E0CE)
                )
                
                Spacer(modifier = Modifier.height(6.dp))
                
                Text(
                    text = "${(book.progress * 100).toInt()}% read",
                    fontSize = 12.sp,
                    color = Color(0xFF8B7E74),
                    fontWeight = FontWeight.Medium
                )
            }
        }
    }
}"""

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
