import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Fix the Bookmarks filter logic
old_filter = r'"Bookmarks" -> filteredBooks\.filter \{ it\.progress > 0f && it\.progress < 1f \}'
new_filter = r'"Bookmarks" -> filteredBooks.filter { try { org.json.JSONArray(it.bookmarks).length() > 0 } catch(e: Exception) { false } }'

content = re.sub(old_filter, new_filter, content)

# Make sure org.json.JSONArray is imported if not already
if "import org.json.JSONArray" not in content:
    content = content.replace("import androidx.compose.ui.Alignment", "import androidx.compose.ui.Alignment\nimport org.json.JSONArray\nimport org.json.JSONObject")

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
