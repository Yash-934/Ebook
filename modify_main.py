import re

with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

old_route = r'composable\("read/\{bookId\}"\) \{ backStackEntry ->\n\s*val bookId = backStackEntry\.arguments\?\.getString\("bookId"\)\?\.toIntOrNull\(\) \?: 0\n\s*ReadScreen\(\n\s*bookId = bookId,\n\s*ebookViewModel = ebookViewModel,\n\s*settingsViewModel = settingsViewModel,\n\s*onNavigateBack = \{ navController\.popBackStack\(\) \}\n\s*\)\n\s*\}'

new_route = """composable("read/{bookId}?scrollTo={scrollTo}") { backStackEntry ->
                            val bookId = backStackEntry.arguments?.getString("bookId")?.toIntOrNull() ?: 0
                            val scrollTo = backStackEntry.arguments?.getString("scrollTo")?.toIntOrNull()
                            ReadScreen(
                                bookId = bookId,
                                ebookViewModel = ebookViewModel,
                                settingsViewModel = settingsViewModel,
                                scrollTo = scrollTo,
                                onNavigateBack = { navController.popBackStack() }
                            )
                        }"""

content = re.sub(old_route, new_route, content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
