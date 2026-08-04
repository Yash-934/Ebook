import re
with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

pattern = r'androidx\.compose\.material3\.AlertDialog\(\n\s*onDismissRequest = onDismiss,\n\s*title = \{ Text\("Add New Book"\) \},\n\s*text = \{\n\s*Column\(verticalArrangement = Arrangement\.spacedBy\(8\.dp\)\) \{'
replacement = r"""androidx.compose.material3.AlertDialog(
        onDismissRequest = onDismiss,
        title = { Text("Add New Book") },
        text = {
            Column(
                modifier = Modifier.verticalScroll(rememberScrollState()),
                verticalArrangement = Arrangement.spacedBy(8.dp)
            ) {"""

content = re.sub(pattern, replacement, content)
with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
