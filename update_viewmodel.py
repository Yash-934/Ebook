import re

with open("app/src/main/java/com/example/ui/EbookViewModel.kt", "r") as f:
    content = f.read()

# Replace toggleBookmark
old_bookmark = r'fun toggleBookmark\(bookId: Int\) \{\n\s*viewModelScope\.launch \{\n\s*val book = repository\.getBookById\(bookId\)\n\s*if \(book != null\) \{\n\s*val newProgress = if \(book\.progress > 0f && book\.progress < 1f\) 0f else 0\.5f\n\s*repository\.update\(book\.copy\(progress = newProgress\)\)\n\s*\}\n\s*\}\n\s*\}'

new_bookmark = """fun addBookmark(bookId: Int, position: Int, name: String = "Bookmark") {
        viewModelScope.launch {
            val book = repository.getBookById(bookId)
            if (book != null) {
                val array = try { JSONArray(book.bookmarks) } catch(e: Exception) { JSONArray() }
                val obj = JSONObject()
                obj.put("position", position)
                obj.put("name", name)
                array.put(obj)
                repository.update(book.copy(bookmarks = array.toString()))
            }
        }
    }
    
    fun removeBookmark(bookId: Int, index: Int) {
        viewModelScope.launch {
            val book = repository.getBookById(bookId)
            if (book != null) {
                val array = try { JSONArray(book.bookmarks) } catch(e: Exception) { JSONArray() }
                if (index >= 0 && index < array.length()) {
                    array.remove(index)
                    repository.update(book.copy(bookmarks = array.toString()))
                }
            }
        }
    }"""

content = re.sub(old_bookmark, new_bookmark, content)

with open("app/src/main/java/com/example/ui/EbookViewModel.kt", "w") as f:
    f.write(content)
