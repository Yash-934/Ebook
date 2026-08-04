import re
with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

dialog_pattern = r'Row\(\n\s*verticalAlignment = Alignment.CenterVertically,\n\s*horizontalArrangement = Arrangement.SpaceBetween,\n\s*modifier = Modifier.fillMaxWidth\(\)\n\s*\) \{\n\s*Text\("Cover Image:"\)'
dialog_replacement = r"""
                Text("Format:")
                Row(modifier = Modifier.fillMaxWidth(), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                    listOf("PDF", "HTML", "EPUB", "MD").forEach { f ->
                        FilterChip(
                            selected = format == f,
                            onClick = { format = f },
                            label = { Text(f) },
                            colors = FilterChipDefaults.filterChipColors(
                                selectedContainerColor = MaterialTheme.colorScheme.primary,
                                selectedLabelColor = MaterialTheme.colorScheme.onPrimary
                            )
                        )
                    }
                }
                
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                    modifier = Modifier.fillMaxWidth()
                ) {
                    Text("Cover Image:")
"""

content = re.sub(dialog_pattern, dialog_replacement, content)
with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
