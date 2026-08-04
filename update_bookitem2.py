import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Replace BookItem
item_pattern = r'fun BookItem\(.*'
new_item = """fun BookItem(
    book: Book,
    onClick: () -> Unit,
    onDelete: () -> Unit,
    onUpdateCover: (String) -> Unit
) {
    var showEditOptions by remember { mutableStateOf(false) }
    
    val coverLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        if (uri != null) {
            onUpdateCover(uri.toString())
            showEditOptions = false
        }
    }

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(260.dp)
    ) {
        Card(
            modifier = Modifier
                .fillMaxSize()
                .combinedClickable(
                    onClick = { 
                        if (showEditOptions) showEditOptions = false
                        else onClick()
                    },
                    onLongClick = { showEditOptions = true }
                ),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = Color(0xFFFFF8E7)),
            border = BorderStroke(1.dp, Color(0xFFD6C8A1)),
            elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
        ) {
            Column(modifier = Modifier.fillMaxSize()) {
                Box(
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1.4f)
                        .background(Color(0xFFE8E0CE)),
                    contentAlignment = Alignment.Center
                ) {
                    if (book.coverUri.isNotEmpty()) {
                        coil.compose.AsyncImage(
                            model = book.coverUri,
                            contentDescription = "Book Cover",
                            modifier = Modifier.fillMaxSize(),
                            contentScale = ContentScale.Crop
                        )
                    } else {
                        Text(
                            text = "📖",
                            fontSize = 64.sp
                        )
                    }
                }
                
                Column(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(12.dp)
                        .weight(1f),
                    verticalArrangement = Arrangement.SpaceBetween
                ) {
                    Column {
                        Box(
                            modifier = Modifier
                                .background(Color(0xFFFdf3d7), RoundedCornerShape(8.dp))
                                .padding(horizontal = 6.dp, vertical = 2.dp)
                        ) {
                            Text(
                                text = book.format,
                                fontSize = 10.sp,
                                fontWeight = FontWeight.Bold,
                                color = Color(0xFFB8860B)
                            )
                        }
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = book.title,
                            fontWeight = FontWeight.Bold,
                            fontSize = 14.sp,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            color = Color(0xFF5A4C40)
                        )
                        Text(
                            text = book.author,
                            fontSize = 12.sp,
                            maxLines = 1,
                            overflow = TextOverflow.Ellipsis,
                            color = Color(0xFF8B7E74)
                        )
                    }
                    
                    Column {
                        LinearProgressIndicator(
                            progress = { book.progress },
                            modifier = Modifier
                                .fillMaxWidth()
                                .height(4.dp)
                                .clip(RoundedCornerShape(2.dp)),
                            color = Color(0xFFB8860B),
                            trackColor = Color(0xFFE8E0CE)
                        )
                        Spacer(modifier = Modifier.height(4.dp))
                        Text(
                            text = "${(book.progress * 100).toInt()}% read",
                            fontSize = 11.sp,
                            color = Color(0xFF8B7E74),
                            fontWeight = FontWeight.Medium
                        )
                    }
                }
            }
        }

        if (showEditOptions) {
            Row(
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .padding(8.dp),
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                Box(
                    modifier = Modifier
                        .size(32.dp)
                        .clip(CircleShape)
                        .background(Color(0xFFE8E0CE))
                        .border(2.dp, Color.Blue, CircleShape)
                        .clickable { coverLauncher.launch("image/*") },
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.Add,
                        contentDescription = "Add Cover",
                        tint = Color.Blue,
                        modifier = Modifier.size(16.dp)
                    )
                }
                
                Box(
                    modifier = Modifier
                        .size(32.dp)
                        .clip(CircleShape)
                        .background(Color(0xFFE8E0CE))
                        .border(2.dp, Color.Red, CircleShape)
                        .clickable { onDelete() },
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.Delete,
                        contentDescription = "Delete Book",
                        tint = Color(0xFF4A8BAD),
                        modifier = Modifier.size(16.dp)
                    )
                }
            }
        }
    }
}
"""

content = re.sub(item_pattern, new_item, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
