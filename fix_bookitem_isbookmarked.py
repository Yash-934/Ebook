import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

old_isb = r'val isBookmarked = book\.progress > 0f && book\.progress < 1f'
new_isb = r'val isBookmarked = try { org.json.JSONArray(book.bookmarks).length() > 0 } catch(e:Exception){ false }'

content = re.sub(old_isb, new_isb, content)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
