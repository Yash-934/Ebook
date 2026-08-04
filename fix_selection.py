import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

if "import androidx.compose.foundation.text.selection.SelectionContainer" not in content:
    content = content.replace("import androidx.compose.foundation.verticalScroll", "import androidx.compose.foundation.verticalScroll\nimport androidx.compose.foundation.text.selection.SelectionContainer")

text_content_pattern = r'Column\(\n\s*modifier = Modifier\n\s*\.fillMaxWidth\(\)\n\s*\.padding\(horizontal = margins\.dp, vertical = margins\.dp\)\n\s*\) \{\n\s*Text\(\n\s*text = book\?\.title \?: "Athenaeum — Advanced Web eBook Reader",'

new_content = """SelectionContainer {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(horizontal = margins.dp, vertical = margins.dp)
                    ) {
                    Text(
                        text = book?.title ?: "Athenaeum — Advanced Web eBook Reader","""

content = re.sub(text_content_pattern, new_content, content)

canvas_pattern = r'Canvas\(modifier = Modifier\n\s*\.matchParentSize\(\)'

new_canvas = """}
                    
                    Canvas(modifier = Modifier
                        .matchParentSize()"""

content = re.sub(canvas_pattern, new_canvas, content)


with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
