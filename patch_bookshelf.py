import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Replace Your Bookshelf title
old_bookshelf = r"""                Row\(\n\s*verticalAlignment = Alignment\.CenterVertically,\n\s*modifier = Modifier\.padding\(horizontal = 16\.dp, vertical = 8\.dp\)\n\s*\) \{\n\s*Icon\(\n\s*imageVector = Icons\.Outlined\.LibraryBooks,\n\s*contentDescription = null,\n\s*tint = MaterialTheme\.colorScheme\.secondary,\n\s*modifier = Modifier\.size\(32\.dp\)\n\s*\)\n\s*Spacer\(modifier = Modifier\.width\(8\.dp\)\)\n\s*Text\(\n\s*text = "Your Bookshelf",\n\s*fontSize = 28\.sp,\n\s*fontWeight = FontWeight\.Bold,\n\s*color = MaterialTheme\.colorScheme\.onBackground\n\s*\)\n\s*\}"""

new_bookshelf = """                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp)
                ) {
                    Text(
                        text = "📖 Your Bookshelf",
                        fontSize = 32.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF5A4C40)
                    )
                }"""

content = re.sub(old_bookshelf, new_bookshelf, content)

# Replace Sort Row
old_sort = r"""                // Filter row\n\s*Row\(\n\s*modifier = Modifier\n\s*\.fillMaxWidth\(\)\n\s*\.padding\(horizontal = 16\.dp, vertical = 8\.dp\)\n\s*\.horizontalScroll\(rememberScrollState\(\)\),\n\s*verticalAlignment = Alignment\.CenterVertically,\n\s*horizontalArrangement = Arrangement\.spacedBy\(8\.dp\)\n\s*\) \{\n\s*Text\("Sort:", color = MaterialTheme\.colorScheme\.onSurfaceVariant\)\n\s*val filters = listOf\(\n\s*"Recent" to Icons\.Outlined\.Schedule,\n\s*"Favorites" to Icons\.Default\.FavoriteBorder,\n\s*"Bookmarks" to Icons\.Default\.BookmarkBorder,\n\s*"Last Read" to Icons\.Outlined\.LibraryBooks,\n\s*"Title" to Icons\.Outlined\.SortByAlpha\n\s*\)\n\s*filters\.forEach \{ \(filterName, icon\) ->\n\s*FilterChip\(\n\s*selected = selectedFilter == filterName,\n\s*onClick = \{ selectedFilter = filterName \},\n\s*label = \{ Text\(filterName\) \},\n\s*leadingIcon = \{\n\s*Icon\(icon, contentDescription = null, modifier = Modifier\.size\(16\.dp\)\)\n\s*\},\n\s*colors = FilterChipDefaults\.filterChipColors\(\n\s*selectedContainerColor = MaterialTheme\.colorScheme\.primary,\n\s*selectedLabelColor = MaterialTheme\.colorScheme\.onPrimary,\n\s*selectedLeadingIconColor = MaterialTheme\.colorScheme\.onPrimary\n\s*\),\n\s*shape = RoundedCornerShape\(16\.dp\),\n\s*border = if \(selectedFilter == filterName\) null else FilterChipDefaults\.filterChipBorder\(enabled = true, selected = false, borderColor = MaterialTheme\.colorScheme\.surfaceVariant\)\n\s*\)\n\s*\}\n\s*\}"""

new_sort = """                // Filter row
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 8.dp)
                        .horizontalScroll(rememberScrollState()),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.spacedBy(8.dp)
                ) {
                    Text("Sort:", color = Color(0xFF8B7E74), fontSize = 16.sp)
                    
                    val filters = listOf(
                        "Recent" to "🕒",
                        "Last Read" to "📖",
                        "Title" to "🔤"
                    )
                    
                    filters.forEach { (filterName, emoji) ->
                        FilterChip(
                            selected = selectedFilter == filterName,
                            onClick = { selectedFilter = filterName },
                            label = { Text("$emoji $filterName", fontSize = 14.sp) },
                            colors = FilterChipDefaults.filterChipColors(
                                selectedContainerColor = Color(0xFFB8860B),
                                selectedLabelColor = Color.White,
                                containerColor = Color.Transparent,
                                labelColor = Color(0xFF5A4C40)
                            ),
                            shape = RoundedCornerShape(16.dp),
                            border = if (selectedFilter == filterName) null else FilterChipDefaults.filterChipBorder(enabled = true, selected = false, borderColor = Color(0xFFE8E0CE))
                        )
                    }
                }"""
content = re.sub(old_sort, new_sort, content)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
