import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

if "import androidx.compose.foundation.lazy.items" not in content:
    content = content.replace("import androidx.compose.foundation.lazy.grid.items", "import androidx.compose.foundation.lazy.grid.items\nimport androidx.compose.foundation.lazy.items")

content = content.replace("androidx.compose.foundation.lazy.items(books)", "items(books)")

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
