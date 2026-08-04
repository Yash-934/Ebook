import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Replace TopBar
old_topbar = r"""                Row\(\n\s*modifier = Modifier\n\s*\.fillMaxWidth\(\)\n\s*\.padding\(horizontal = 16\.dp, vertical = 12\.dp\)\n\s*\.statusBarsPadding\(\),\n\s*verticalAlignment = Alignment\.CenterVertically,\n\s*horizontalArrangement = Arrangement\.SpaceBetween\n\s*\) \{\n\s*Row\(verticalAlignment = Alignment\.CenterVertically\) \{\n\s*Box\(\n\s*modifier = Modifier\n\s*\.size\(40\.dp\)\n\s*\.clip\(CircleShape\)\n\s*\.background\(Color\(0xFFf4e8d3\)\)\n\s*\.clickable \{ scope\.launch \{ drawerState\.open\(\) \} \},\n\s*contentAlignment = Alignment\.Center\n\s*\) \{\n\s*Icon\(\n\s*imageVector = Icons\.Default\.Settings,\n\s*contentDescription = "Settings",\n\s*tint = Color\(0xFF6b5540\),\n\s*modifier = Modifier\.size\(20\.dp\)\n\s*\)\n\s*\}\n\s*\}\n\s*Button\(\n\s*onClick = \{ showAddBookOptions = true \},\n\s*shape = RoundedCornerShape\(8\.dp\),\n\s*colors = ButtonDefaults\.buttonColors\(\n\s*containerColor = MaterialTheme\.colorScheme\.primary,\n\s*contentColor = MaterialTheme\.colorScheme\.onPrimary\n\s*\),\n\s*contentPadding = PaddingValues\(horizontal = 12\.dp, vertical = 8\.dp\),\n\s*modifier = Modifier\.height\(36\.dp\)\n\s*\) \{\n\s*Text\("\+ Add Book", fontWeight = FontWeight\.Bold\)\n\s*\}\n\s*\}"""
new_topbar = """                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 12.dp)
                        .statusBarsPadding(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = "📚 My Library",
                        fontSize = 24.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF5A4C40)
                    )
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(RoundedCornerShape(8.dp))
                                .background(Color(0xFFf4e8d3))
                                .border(1.dp, Color(0xFFE8E0CE), RoundedCornerShape(8.dp))
                                .clickable { scope.launch { drawerState.open() } },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Settings,
                                contentDescription = "Settings",
                                tint = Color(0xFF4A8BAD),
                                modifier = Modifier.size(24.dp)
                            )
                        }
                        Button(
                            onClick = { showAddBookOptions = true },
                            shape = RoundedCornerShape(8.dp),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Color(0xFFB8860B),
                                contentColor = Color.White
                            ),
                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                            modifier = Modifier.height(40.dp)
                        ) {
                            Text("+ Add Book", fontSize = 16.sp)
                        }
                    }
                }"""
content = re.sub(old_topbar, new_topbar, content)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
