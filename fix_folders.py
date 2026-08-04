import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# 1. Add customFolders state
state_pattern = r'var newFolderName by remember \{ mutableStateOf\(""\) \}'
new_state = """var newFolderName by remember { mutableStateOf("") }
    var customFolders by remember { mutableStateOf(setOf<String>()) }"""
content = re.sub(state_pattern, new_state, content)

# 2. Update folders computation
folders_pattern = r'val folders = remember\(booksFlow\) \{\n\s*listOf\("All"\) \+ booksFlow\.map \{ it\.folder \}\.distinct\(\)\.filter \{ it\.isNotBlank\(\) && it != "All" \}\.sorted\(\)\n\s*\}'
new_folders = """val folders = remember(booksFlow, customFolders) {
                    val dbFolders = booksFlow.map { it.folder }
                    val allFolders = (dbFolders + customFolders).filter { it.isNotBlank() && it != "All" }.distinct().sorted()
                    listOf("All") + allFolders
                }"""
content = re.sub(folders_pattern, new_folders, content)

# 3. Update confirmButton onClick
onclick_pattern = r'onClick = \{\n\s*if \(newFolderName\.isNotBlank\(\)\) \{\n\s*selectedFolder = newFolderName\n\s*showNewFolderDialog = false\n\s*newFolderName = ""\n\s*\}\n\s*\},'
new_onclick = """onClick = {
                            if (newFolderName.isNotBlank()) {
                                customFolders = customFolders + newFolderName
                                selectedFolder = newFolderName
                                showNewFolderDialog = false
                                newFolderName = ""
                            }
                        },"""
content = re.sub(onclick_pattern, new_onclick, content)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
