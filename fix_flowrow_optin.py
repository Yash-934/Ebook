import re

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "r") as f:
    content = f.read()

# Add import
if "import androidx.compose.foundation.layout.ExperimentalLayoutApi" not in content:
    content = content.replace("import androidx.compose.foundation.layout.FlowRow", "import androidx.compose.foundation.layout.FlowRow\nimport androidx.compose.foundation.layout.ExperimentalLayoutApi")

# Add OptIn
if "@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)" not in content:
    content = content.replace("@OptIn(ExperimentalMaterial3Api::class)\n@Composable\nfun HomeScreen", "@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)\n@Composable\nfun HomeScreen")

with open("app/src/main/java/com/example/ui/screens/HomeScreen.kt", "w") as f:
    f.write(content)
