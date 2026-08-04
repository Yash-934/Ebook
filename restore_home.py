import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Restore TopBar to its former glory
topbar_pattern = r'Scaffold\(\n\s*topBar = \{\n.*?\},\n\s*containerColor = MaterialTheme\.colorScheme\.background'
new_topbar = """Scaffold(
            topBar = {
                Row(
                    modifier = Modifier
                        .fillMaxWidth()
                        .padding(horizontal = 16.dp, vertical = 12.dp)
                        .statusBarsPadding(),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            text = "📚 My Library",
                            fontSize = 24.sp,
                            fontWeight = FontWeight.Bold,
                            color = Color(0xFF5A4C40)
                        )
                    }
                    Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        Box(
                            modifier = Modifier
                                .size(40.dp)
                                .clip(RoundedCornerShape(12.dp))
                                .background(Color(0xFFF4E8D3))
                                .border(1.dp, Color(0xFFE8E0CE), RoundedCornerShape(12.dp))
                                .clickable { scope.launch { drawerState.open() } },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                imageVector = Icons.Default.Settings,
                                contentDescription = "Settings",
                                tint = Color(0xFF4A8BAD),
                                modifier = Modifier.size(20.dp)
                            )
                        }
                        Button(
                            onClick = { showAddBookOptions = true },
                            shape = RoundedCornerShape(12.dp),
                            colors = ButtonDefaults.buttonColors(
                                containerColor = Color(0xFFB8860B),
                                contentColor = Color.White
                            ),
                            contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                            modifier = Modifier.height(40.dp)
                        ) {
                            Text("+ Add Book", fontSize = 16.sp, fontWeight = FontWeight.Bold)
                        }
                    }
                }
            },
            containerColor = MaterialTheme.colorScheme.background"""
content = re.sub(topbar_pattern, new_topbar, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
