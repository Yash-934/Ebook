import re

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "r") as f:
    content = f.read()

pattern = r'currentLineColor = when \(activeEditTool\) \{.*?\n.*?else -> Color\(0xFF87CEEB\)\n.*?\}'
replacement = """currentLineColor = when (activeEditTool) {
                                        "highlight" -> highlightColor
                                        "underline" -> underlineColor
                                        else -> doodleColor
                                    }"""

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/ReadScreen.kt", "w") as f:
    f.write(content)
