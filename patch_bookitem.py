import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Update BookItem arguments
old_args = r"""fun BookItem\(
    book: Book,
    onClick: \(\) -> Unit,
    onDelete: \(\) -> Unit
\) \{
    var showDeleteButton by remember \{ mutableStateOf\(false\) \}"""

new_args = """fun BookItem(
    book: Book,
    onClick: () -> Unit,
    onDelete: () -> Unit,
    onUpdateCover: (String) -> Unit
) {
    var showEditOptions by remember { mutableStateOf(false) }
    
    val coverLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri ->
        if (uri != null) {
            onUpdateCover(uri.toString())
            showEditOptions = false
        }
    }"""

content = re.sub(old_args, new_args, content)

# Update combinedClickable
old_click = r"""combinedClickable\(
                    onClick = \{ 
                        if \(showDeleteButton\) showDeleteButton = false
                        else onClick\(\)
                    \},
                    onLongClick = \{ showDeleteButton = true \}
                \)"""

new_click = """combinedClickable(
                    onClick = { 
                        if (showEditOptions) showEditOptions = false
                        else onClick()
                    },
                    onLongClick = { showEditOptions = true }
                )"""

content = re.sub(old_click, new_click, content)

# Replace the delete button with edit options
old_delete = r"""        if \(showDeleteButton\) \{
            Box\(
                modifier = Modifier
                    \.size\(36\.dp\)
                    \.align\(Alignment\.TopEnd\)
                    \.offset\(x = 8\.dp, y = \(-8\)\.dp\)
                    \.clip\(CircleShape\)
                    \.background\(Color\.White\)
                    \.border\(2\.dp, Color\.Red, CircleShape\)
                    \.clickable \{ onDelete\(\) \},
                contentAlignment = Alignment\.Center
            \) \{
                Icon\(
                    imageVector = Icons\.Default\.Delete,
                    contentDescription = "Delete Book",
                    tint = Color\.Red,
                    modifier = Modifier\.size\(20\.dp\)
                \)
            \}
        \}"""

new_delete = """        if (showEditOptions) {
            Row(
                modifier = Modifier
                    .align(Alignment.TopEnd)
                    .offset(x = 8.dp, y = (-8).dp),
                horizontalArrangement = Arrangement.spacedBy(4.dp)
            ) {
                // Add Cover Button
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .clip(CircleShape)
                        .background(Color.White)
                        .border(2.dp, Color.Blue, CircleShape)
                        .clickable { coverLauncher.launch("image/*") },
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.Add,
                        contentDescription = "Add Cover",
                        tint = Color.Blue,
                        modifier = Modifier.size(20.dp)
                    )
                }
                
                // Delete Button
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .clip(CircleShape)
                        .background(Color.White)
                        .border(2.dp, Color.Red, CircleShape)
                        .clickable { onDelete() },
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.Delete,
                        contentDescription = "Delete Book",
                        tint = Color.Red,
                        modifier = Modifier.size(20.dp)
                    )
                }
            }
        }"""

content = re.sub(old_delete, new_delete, content)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
