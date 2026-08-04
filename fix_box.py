import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Fix the extra brace
bad_brace = """                    }
                }
                }
                
                Column("""
                
good_brace = """                    }
                }
                
                Column("""
                
content = content.replace(bad_brace, good_brace)

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
