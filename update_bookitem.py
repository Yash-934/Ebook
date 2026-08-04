import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Add imports if missing
if "import androidx.compose.material.icons.filled.Favorite" not in content:
    content = content.replace("import androidx.compose.material.icons.Icons", "import androidx.compose.material.icons.Icons\nimport androidx.compose.material.icons.filled.Favorite\nimport androidx.compose.material.icons.filled.Bookmark")
if "import androidx.compose.material3.Icon" not in content:
    content = content.replace("import androidx.compose.material3.*", "import androidx.compose.material3.*\nimport androidx.compose.material3.Icon")

# Update BookItem Box
box_pattern = r'Text\(\n\s*text = "📖",\n\s*fontSize = 64\.sp\n\s*\)\n\s*\}'

new_box = """Text(
                            text = "📖",
                            fontSize = 64.sp
                        )
                    }
                    Row(
                        modifier = Modifier
                            .fillMaxWidth()
                            .align(Alignment.TopEnd)
                            .padding(8.dp),
                        horizontalArrangement = Arrangement.End,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        val isBookmarked = book.progress > 0f && book.progress < 1f
                        if (book.isFavorite) {
                            Box(
                                modifier = Modifier
                                    .padding(end = if (isBookmarked) 4.dp else 0.dp)
                                    .clip(CircleShape)
                                    .background(Color.White.copy(alpha = 0.8f))
                                    .padding(4.dp)
                            ) {
                                Icon(Icons.Default.Favorite, contentDescription = "Favorite", tint = Color(0xFFFF5252), modifier = Modifier.size(16.dp))
                            }
                        }
                        if (isBookmarked) {
                            Box(
                                modifier = Modifier
                                    .clip(CircleShape)
                                    .background(Color.White.copy(alpha = 0.8f))
                                    .padding(4.dp)
                            ) {
                                Icon(Icons.Default.Bookmark, contentDescription = "Bookmark", tint = Color(0xFFFFA500), modifier = Modifier.size(16.dp))
                            }
                        }
                    }
                }"""

content = re.sub(box_pattern, new_box, content)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
