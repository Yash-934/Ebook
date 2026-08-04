import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

pattern = r'(\s*)}(\s*)HorizontalDivider\(color = textColor\.copy\(alpha = 0\.1f\)\)'
replacement = r"""\1}\2if (activeEditTool != null) {
\2    Row(
\2        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
\2        horizontalArrangement = Arrangement.spacedBy(12.dp),
\2        verticalAlignment = Alignment.CenterVertically
\2    ) {
\2        val colors = listOf(Color.Red, Color(0xFFE29578), Color(0xFFFFD700), Color(0xFF87CEEB), Color(0xFF5BA4A4), Color.Black, Color.White)
\2        Text("Color:", fontSize = 12.sp, color = textColor)
\2        colors.forEach { color ->
\2            Box(
\2                modifier = Modifier
\2                    .size(24.dp)
\2                    .clip(androidx.compose.foundation.shape.CircleShape)
\2                    .background(color)
\2                    .border(
\2                        width = 2.dp,
\2                        color = if ((activeEditTool == "highlight" && highlightColor == color) ||
\2                                    (activeEditTool == "underline" && underlineColor == color) ||
\2                                    (activeEditTool == "doodle" && doodleColor == color)) 
\2                                textColor else Color.Transparent,
\2                        shape = androidx.compose.foundation.shape.CircleShape
\2                    )
\2                    .clickable {
\2                        when (activeEditTool) {
\2                            "highlight" -> highlightColor = color
\2                            "underline" -> underlineColor = color
\2                            "doodle" -> doodleColor = color
\2                        }
\2                    }
\2            )
\2        }
\2    }
\2}\2HorizontalDivider(color = textColor.copy(alpha = 0.1f))"""

# Need to only replace the SECOND match (which is around line 339)
# Or I can just match exactly what is there.
# Let's write a python script to find the specific block.
