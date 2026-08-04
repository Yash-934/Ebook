import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

grid_pattern = r'LazyVerticalGrid\(\n\s*columns = GridCells\.Adaptive\(150\.dp\),\n\s*modifier = Modifier\.fillMaxSize\(\),\n\s*contentPadding = PaddingValues\(16\.dp\),\n\s*horizontalArrangement = Arrangement\.spacedBy\(16\.dp\),\n\s*verticalArrangement = Arrangement\.spacedBy\(16\.dp\)\n\s*\) \{\n\s*items\(books\) \{ book ->\n\s*BookItem\(\n\s*book = book,\n\s*onClick = \{ navController\.navigate\("read/\$\{book\.id\}"\) \},\n\s*onDelete = \{ ebookViewModel\.deleteBook\(book\.id\) \},\n\s*onUpdateCover = \{ ebookViewModel\.updateBookCover\(book\.id, it\) \}\n\s*\)\n\s*\}\n\s*\}'

new_layout = """if (selectedFilter == "Bookmarks") {
                    androidx.compose.foundation.lazy.LazyColumn(
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        androidx.compose.foundation.lazy.items(books) { book ->
                            Column(modifier = Modifier.fillMaxWidth().background(Color.White, RoundedCornerShape(12.dp)).border(1.dp, DividerColor, RoundedCornerShape(12.dp)).padding(16.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                                    Box(modifier = Modifier.height(180.dp).width(120.dp)) {
                                        BookItem(
                                            book = book,
                                            onClick = { navController.navigate("read/${book.id}") },
                                            onDelete = { ebookViewModel.deleteBook(book.id) },
                                            onUpdateCover = { ebookViewModel.updateBookCover(book.id, it) }
                                        )
                                    }
                                    Column {
                                        Text(book.title, fontWeight = FontWeight.Bold, fontSize = 18.sp, color = BrownText)
                                        Spacer(modifier = Modifier.height(12.dp))
                                        val bookmarksArray = try { org.json.JSONArray(book.bookmarks) } catch(e:Exception){ org.json.JSONArray() }
                                        for (i in 0 until bookmarksArray.length()) {
                                            val bm = bookmarksArray.getJSONObject(i)
                                            val pos = bm.getInt("position")
                                            val name = bm.optString("name", "Bookmark at $pos")
                                            Row(modifier = Modifier.fillMaxWidth().clickable {
                                                navController.navigate("read/${book.id}?scrollTo=$pos")
                                            }.padding(vertical = 8.dp), verticalAlignment = Alignment.CenterVertically) {
                                                Box(modifier = Modifier.size(24.dp).background(GoldenOrange, CircleShape), contentAlignment = Alignment.Center) {
                                                    Text("${i+1}", color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                                                }
                                                Spacer(modifier = Modifier.width(12.dp))
                                                Text(name, color = BrownText, fontSize = 14.sp)
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                } else {
                    LazyVerticalGrid(
                        columns = GridCells.Adaptive(150.dp),
                        modifier = Modifier.fillMaxSize(),
                        contentPadding = PaddingValues(16.dp),
                        horizontalArrangement = Arrangement.spacedBy(16.dp),
                        verticalArrangement = Arrangement.spacedBy(16.dp)
                    ) {
                        items(books) { book ->
                            BookItem(
                                book = book,
                                onClick = { navController.navigate("read/${book.id}") },
                                onDelete = { ebookViewModel.deleteBook(book.id) },
                                onUpdateCover = { ebookViewModel.updateBookCover(book.id, it) }
                            )
                        }
                    }
                }"""

content = re.sub(grid_pattern, new_layout, content)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
