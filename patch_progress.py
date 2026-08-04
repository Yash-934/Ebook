import re
with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

pattern = r'LinearProgressIndicator\(\n\s*progress = \{ book.progress \},\n\s*modifier = Modifier\n\s*\.fillMaxWidth\(\)\n\s*\.height\(4\.dp\),\n\s*color = Color\(0xFFB8860B\),\n\s*trackColor = Color\.LightGray\n\s*\)'

replacement = r"""Column(modifier = Modifier.padding(8.dp)) {
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
                }"""

content = re.sub(pattern, replacement, content)
with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
